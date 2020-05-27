#!/usr/bin/env python3
import requests
from .utils import cprint


class GoogleDriveDownloader:
    CHUNK_SIZE: int = 32768
    DOWNLOAD_URL: str = 'https://docs.google.com/uc?export=download'
    psize: bool

    def __init__(self, file_id: str, dest: str, psize=False):
        self.file_id: str = file_id
        self.dest: str = dest
        self.session = requests.Session()
        self.curent_size = 0
        self.psize = psize

    @staticmethod
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return '{:.1f} {}{}'.format(num, unit, suffix)
            num /= 1024.0
        return '{:.1f} {}{}'.format(num, 'Yi', suffix)

    def download(self):
        response = self.session.get(self.DOWNLOAD_URL, params={'id': self.file_id}, stream=True)
        token = self.get_confirm_token(response)
        if token:
            params = {'id': self.file_id, 'confirm': token}
            response = self.session.get(self.DOWNLOAD_URL, params=params, stream=True)
        self.save(response)

    def save(self, response):
        with open(self.dest, 'wb') as f:
            for chunk in response.iter_content(self.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    if self.psize:
                        cprint('\r' + self.__repr__(), color="green", end=' ')
                    self.curent_size += self.CHUNK_SIZE

    def __repr__(self):
        return "<GoogleDriveDownloader>::download --> {} destination={}".format(
            self.sizeof_fmt(self.curent_size),
            self.dest
        )


if __name__ == '__main__':
    pass
