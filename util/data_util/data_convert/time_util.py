import datetime
import time


class time_util(object):

    @staticmethod
    def os_normal():
        """
        获取当前时刻
        :return: 当前时刻（2022-08-22 08:19:23）
        """
        return str(datetime.datetime.now()).split('.')[0]

    @staticmethod
    def os_stamp():
        """
        获取当前时刻
        :return: 当前时刻（1661127563）
        """
        return str(time.time()).split('.')[0]

    @staticmethod
    def stamp_to_normal(time_stamp):
        """
        时间戳类型（1661127563）转化为标准时间类型（2022-08-22 08:19:23）
        :param time_stamp: 时间戳类型（1661127563）
        :return: 标准时间类型（2022-08-22 08:19:23）
        """
        time_stamp = time.localtime(time_stamp / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S", time_stamp)

    @staticmethod
    def weibo_to_normal(time_weibo, type='+0800'):
        """
        微博时间类型（Mon Aug 22 08:19:23 +0800 2022）转化为标准型（2022-08-22 08:19:23）
        :param time_weibo:微博时间类型（Mon Aug 22 08:19:23 +0800 2022）
        :return:标准型（2022-08-22 08:19:23）
        """
        return str(datetime.datetime.strptime(time_weibo, f'%a %b %d %H:%M:%S {type} %Y'))

    @staticmethod
    def normal_to_stamp(time_normal):
        """
        标准时间类型（2022-08-22 08:19:23）转化为时间戳类型（1661127563）
        :param time_normal:标准时间类型（2022-08-22 08:19:23）
        :return:时间戳类型（1661127563）
        """
        return int(time.mktime(time.strptime(time_normal, "%Y-%m-%d %H:%M:%S")))

    @staticmethod
    def weibo_convert(time_weibo, stamp=False):
        """
        微博时间类型（Mon Aug 22 08:19:23 +0800 2022）转化方法
        :param time_weibo: 微博时间类型（Mon Aug 22 08:19:23 +0800 2022）
        :param stamp: 是否转化为时间戳类型（1661127563），默认转化标准时间类型（2022-08-22 08:19:23）
        :return: 标准型（2022-08-22 08:19:23）或 时间戳类型（1661127563）
        """
        time_result = time_util.weibo_to_normal(time_weibo)
        if stamp:
            time_result = time_util.normal_to_stamp(time_result)
        return time_result
