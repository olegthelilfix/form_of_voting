from concurrent.futures import ThreadPoolExecutor

__author__ = 'vladthelittleone'


class TokenContainer:
    __container = {}

    @classmethod
    def add(cls, uid, token):
        if uid not in cls.__container:
            cls.__container[uid] = []
        cls.__container[uid].append(token)

    @classmethod
    def get(cls, uid):
        if uid in cls.__container:
            return cls.__container[uid]
        return []

    @classmethod
    def remove(cls, uid, token):
        if uid in cls.__container:
            return cls.__container[uid].remove(token)
        return []
