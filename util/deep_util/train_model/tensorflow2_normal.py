import random

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, optimizers, datasets, models


class tensorflow2_normal(object):

    def __init__(self, data_list, normal_data, select_rate=0.2):
        self.__data_list = data_list
        self.__normal_data = normal_data
        self.__select_rate = select_rate
        self.__class_num = len(data_list)
        self.__one_hot = []

    def one_hot(self):
        for i in range(self.__class_num):
            temp = np.zeros([self.__class_num], dtype=np.int32)
            temp[i] = 1
            self.__one_hot.append(temp)

    def select_index(self, data_li):
        test_size = len(data_li) * self.__select_rate
        index_li = [i for i in range(len(data_li))]
        test_index = set()
        while len(test_index) <= test_size:
            index = random.choice(index_li)
            test_index.add(index)
        return test_index

    def select(self):
        train_li, test_li, train_label, test_label = [], [], [], []
        for label, data_li in enumerate(self.__data_list):
            test_index = self.select_index(data_li=data_li)
            for i in range(len(data_li)):
                if i in test_index:
                    test_li.append(data_li[i])
                    test_label.append(self.__one_hot[label])
                else:
                    train_li.append(data_li[i])
                    train_label.append(self.__one_hot[label])
        return train_li, test_li, train_label, test_label

    def build(self):
        self.one_hot()
        train_li, test_li, train_label, test_label = self.select()
        train_db = self.__normal_data(train_li, train_label)
        test_db = self.__normal_data(test_li, test_label)
        return train_db, test_db

# if __name__ == '__main__':
#     data1 = [
#         [1.2, 2.3, 343, 3.5],
#         [1.2, 2.3, 343, 3.5],
#         [1.2, 2.3, 343, 3.5]]
#     data_li = [[data1, data1, data1, data1, data1, data1, data1, data1], [data1, data1]]
#     tf_normal = tensorflow2(data_li)
#     train_li, test_li, train_label, test_label = tf_normal.build()
#     print(np.shape(train_li))
#     print(train_label)
#     print(test_li)
#     print(test_label)
