from src.file_downloader.interface import FileDownloader
import os
import requests
from tqdm import tqdm
import re
import tempfile



class FileDownloaderImpl(FileDownloader):
    def download_to_path(self, url: str) -> str:
        tmp_root = tempfile.gettempdir()

        safe = re.sub(r'[^A-Za-z0-9._-]', '_', url)

        local_path = os.path.join('datas', safe)
        temp_path = os.path.join(tmp_root, safe)


        os.makedirs('datas', exist_ok=True)

        if not os.path.exists(local_path):
            with requests.get(url, stream=True) as response:
                response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))

                with open(temp_path, 'wb') as f:
                    with tqdm(total=total_size, unit='B', unit_scale=True,
                              desc=url) as pbar:
                        for chunk in response.iter_content(chunk_size=1024*8):
                            f.write(chunk)
                            pbar.update(len(chunk))
            os.rename(temp_path, local_path)
        return local_path

