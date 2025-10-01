import inspect
from typing import Type

from dishka import Provider, Scope


def get_provided_classes(*providers: Provider) -> set[Type]:
    """
    Provider에 등록된 모든 Class를 반환합니다.
    :param providers:
    :return: Class(type) Set
    """
    all_classes = []

    for provider in providers:
        for factory in provider.factories:
            if isinstance(factory.source, type):
                all_classes.append(factory.source)

    return set(all_classes)

def get_interfaces(classes: set) -> set[type]:
    """
    입력된 Class들의 추상 클래스를 모두 추출합니다. 상속된 추상 클래스도 함께 반환됩니다.
    :param classes:
    :return:
    """
    interfaces: set[type] = set()
    for i in classes:
        for base_class in inspect.getmro(i)[1:-1]:
            if inspect.isabstract(base_class): # 추상 클래스만 수집
                interfaces.add(base_class)

    return interfaces


def get_list_provider(*providers: Provider) -> Provider:
    """
    기존 Provider에서 인터페이스를 인식하고 list[인터페이스] 를 호환하는 Provider를 반환합니다.
    :param providers:
    :return:
    """
    classes = get_provided_classes(*providers)
    interfaces = get_interfaces(classes)
    list_provider = Provider(Scope.APP)
    for interface in interfaces:
        implementations = set()
        for _class in classes:
            if issubclass(_class, interface):
                implementations.add(_class)

        if not implementations:
            continue

        list_provider.provide_all(*classes)
        list_provider.provide(lambda: [], provides=list[interface])
        for cls in implementations:
            @list_provider.decorate
            def aggregate_classes(many: list[interface], one: cls) -> list[interface]:
                return many + [one]

    return list_provider