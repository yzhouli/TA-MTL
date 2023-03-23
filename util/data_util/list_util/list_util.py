class list_util(object):

    @staticmethod
    def max_index(data_li):
        temp, result = data_li[0], 0
        for index, item in enumerate(data_li):
            if temp < item:
                temp = item
                result = index
        return result

