from concurrent.futures import ThreadPoolExecutor

__author__ = 'vladthelittleone'


class UploadManager:
    __executor = ThreadPoolExecutor(max_workers=1)

    @classmethod
    def submit(cls, fn, *args, **kwargs):
        return cls.__executor.submit(fn, *args, **kwargs)
