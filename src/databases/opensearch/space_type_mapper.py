from src.databases.dto.distance import Distance


def get_space_type(distance: Distance):
    if distance == Distance.COSINE:
        return "cosinesimil"

    raise Exception("Not supported distance metric")
