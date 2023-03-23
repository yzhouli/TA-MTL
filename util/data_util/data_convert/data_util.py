import datetime
import time


class weibo_util(object):
    __ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @staticmethod
    def base62_encode(num):
        """
        62进制编码方法
        :param num 代编码数值
        """
        if (num == 0):
            return weibo_util.__ALPHABET[0]
        arr = []
        base = len(weibo_util.__ALPHABET)
        while num:
            rem = num % base
            num = num // base
            arr.append(weibo_util.__ALPHABET[rem])
        arr.reverse()
        return ''.join(arr)

    @staticmethod
    def base62_decode(string):
        """
        62进制解码方法
        :param string 代解码字符串
        """
        base = len(weibo_util.__ALPHABET)
        strlen = len(string)
        num, idx = 0, 0
        for char in string:
            power = (strlen - (idx + 1))
            num += weibo_util.__ALPHABET.index(char) * (base ** power)
            idx += 1

        return num

    @staticmethod
    def topic_id_convert(topic_id):
        """
        将微博话题id转化为mid
        :param topic_id 微博话题id
        :return 微博话题mid
        """
        topic_id = str(topic_id)[::-1]
        size = int(len(topic_id) / 7 if len(topic_id) % 7 == 0 else len(topic_id) / 7 + 1)
        result = []
        for i in range(size):
            s = topic_id[i * 7: (i + 1) * 7][::-1]
            s = weibo_util.base62_encode(int(s))
            s_len = len(s)
            if i < size - 1 and len(s) < 4:
                s = '0' * (4 - s_len) + s
            result.append(s)
        result.reverse()
        return ''.join(result)

    @staticmethod
    def topic_mid_convert(topic_mid):
        """
        将微博话题mid转化为id
        :param topic_mid 微博话题mid
        :return 微博话题id
        """
        topic_mid = str(topic_mid)[::-1]
        size = len(topic_mid) / 4 if len(topic_mid) % 4 == 0 else len(topic_mid) // 4 + 1
        result = []
        for i in range(size):
            s = topic_mid[i * 4: (i + 1) * 4][::-1]
            s = str(weibo_util.base62_decode(str(s)))
            s_len = len(s)
            if i < size - 1 and s_len < 7:
                s = (7 - s_len) * '0' + s
            result.append(s)
        result.reverse()
        return int(''.join(result))


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
