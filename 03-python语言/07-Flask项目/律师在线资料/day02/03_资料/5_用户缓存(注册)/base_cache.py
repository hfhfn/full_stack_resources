from flask import current_app
import json


from redis import RedisError
from sqlalchemy.exc import DatabaseError

from common.cache.constants import UserCacheDataTTL, UserNotExistsTTL


class BaseCache(object):
    """
    类属性    类属性在每个对象之间共享
    实例属性   每个对象之间互相独立，互不干扰

    实例方法： 一般操作对象的属性，也可操作类属性
    类方法： 操作类属性
    静态方法：   也可以操作类属性
    """

    def __init__(self, id):
        self.key = "xxx:{}".format(id)
        self.id = id
        self.CacheDataTTL = UserCacheDataTTL.get_value()
        self.NotExistsTTL = UserNotExistsTTL.get_value()

    def get(self):
        """
        获取用户的数据

        # 查询缓存redis集群
        # redis中有记录
        #     如果值是-1   返回None
        #     不是-1   返回数据
        #
        # redis中没有记录
        #     查询数据库 mysql
        #     如果数据库有：
                    设置到redis中(回填)
        #         返回
        #     数据库没有：
        #         返回None， 在redis中设置值 "-1"(解决缓存穿透问题)
        :return:
        """
        # 查询缓存redis集群
        rc = current_app.redis_cluster
        try:
            ret = rc.get(self.key)  # 查询出来的结果是bytes类型
        except RedisError as e:
            # 记录日志
            current_app.logger.error(e)
            ret = None  # 为了能够在下面的代码中查询mysql数据库

        # redis中有记录
        if False:
        # if ret is not None:

            #     如果值是-1   返回None
            if ret == b'-1':
                return None
            #     不是-1   返回数据
            else:
                # print(ret.decode())
                # python3.6之后的json.loads()才支持传bytes类型字符串
                # python3.5只能传json字符串
                data_dict = json.loads(ret.decode())
                return data_dict
        #
        # redis中没有记录
        else:
            #     查询数据库 mysql
            try:
                obj = self.get_data_obj()

            except DatabaseError as e:
                current_app.logger.error(e)
                raise e  # 抛出异常，抛给调用者，让调用者决定

            # 在Flask-SQLAlchemy中，查询不到是数据的时候，会返回一个None
            #     如果数据库有：
            if obj is not None:
                obj_dict = self.create_obj_dict(obj)
                try:
                    rc.setex(self.key, self.CacheDataTTL, json.dumps(obj_dict))
                except RedisError as e:
                    current_app.logger.error(e)

                # 返回
                return obj_dict
            #   数据库没有：
            else:
                # 返回None， 在redis中设置值 "-1"(解决缓存穿透问题)
                try:
                    rc.setex(self.key, self.NotExistsTTL, "-1")
                except RedisError as e:
                    current_app.logger.error(e)

                return None

    def clear(self):
        """
        删除某一个键"user:{}:profile".format(user_id)
        :return:
        """
        try:
            rc = current_app.redis_cluster
            rc.delete(self.key)
        except RedisError as e:
            current_app.logger.error(e)

    def exists(self):
        """
        通过缓存来判断用户存不存在         不是这种：  查询缓存存不存在这个用户(没有意义)

        查询缓存
        查询缓存如果有记录
            如果是-1  返回  False
            不是-1  返回  True
        查询缓存没有记录
            查询数据库mysql
            如果在mysql
                返回   True
            如果不在
                返回   False  设置-1

        :return:  True  False
        """
        ret = self.get()
        if ret is not None:
            return True
        else:
            return False

