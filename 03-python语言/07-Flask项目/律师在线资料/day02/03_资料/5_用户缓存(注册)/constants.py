"""

USER_CACHE_DATA_TTL+random.randint(0, USER_CACHE_DATA_MAX_DELTA)
"""
import random


class DataTTLBase(object):
    TTL = 60 * 60 * 2
    MAX_DELTA = 60 * 10

    @classmethod
    def get_value(cls):
        return cls.TTL + random.randint(0, cls.MAX_DELTA)


class UserCacheDataTTL(DataTTLBase):
    pass


class UserNotExistsTTL(DataTTLBase):
    TTL = 60 * 5
    MAX_DELTA = 60 * 1


class QustCacheDataTTL(DataTTLBase):
    pass


class QustNotExistsTTL(DataTTLBase):
    TTL = 60 * 5
    MAX_DELTA = 60 * 1


class LawyerCacheDataTTL(DataTTLBase):
    TTL = 60 * 60 * 1
    MAX_DELTA = 60 * 8


class LawyerNotExistsTTL(DataTTLBase):
    TTL = 60 * 4
    MAX_DELTA = 60 * 1


class UserIDCacheDataTTL(DataTTLBase):
    TTL = 60 * 60 * 1
    MAX_DELTA = 60 * 10


class UserIDNotExistsTTL(DataTTLBase):
    TTL = 60 * 4
    MAX_DELTA = 60 * 1


class UserSearchingHistoryCacheDataTTL(DataTTLBase):
    TTL = 60 * 60 * 24 * 30     # 搜索历史保存1个月
    MAX_DELTA = 60 * 50


class UserSearchingHistoryNotExistsTTL(DataTTLBase):
    TTL = 60 * 60 * 5
    MAX_DELTA = 60 * 1