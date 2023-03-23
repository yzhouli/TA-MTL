import math
import os

import librosa as librosa
import numpy as np
from util.data_util.data_convert.data_util import time_util


class to_audio(object):

    def __init__(self, num, path, class_num, hz=4800, audio_size=20):
        self.__num = num
        self.__path = path
        self.__class_num = class_num
        self.__hz = hz
        self.audio_size = audio_size

    def key(self, data):
        return data[0]

    def compute_entropy(self, data_li, re=False):
        temp = dict()
        for i in range(self.__class_num):
            temp[f'{i}'] = 0.00000001
        for data in data_li:
            temp[data[2]] += 1
        entropy = 0.0
        good_emo, value = -1, -1
        for i in range(self.__class_num):
            rate = temp[f'{i}'] / self.__num
            entropy -= rate * math.log(rate, math.e)
            if value < temp[f'{i}']:
                value = temp[f'{i}']
                good_emo = i * rate
        if re:
            return entropy, good_emo, temp
        return entropy, good_emo

    def compute_correlation(self, current_li, next_li):
        temp = []
        for item in next_li:
            temp.append(item[1])
        value = 0.0
        for item in current_li:
            if item[1] in temp:
                value += 1
        correlation = value / len(current_li)
        return correlation

    def compute_1(self, current_li, next_li, emo_rate):
        entropy, good_emo, temp = self.compute_entropy(data_li=current_li, re=True)
        good_emo *= 10
        correlation = self.compute_correlation(current_li=current_li, next_li=next_li)
        for i in range(len(emo_rate)):
            emo_rate[i] += temp[f'{i}']
        return entropy, good_emo, correlation

    def spilt(self, data_li):
        temp, temp_li = [], []
        for data in data_li:
            temp.append(data)
            if len(temp) >= self.__num:
                temp_li.append(temp)
                temp = []
        return temp_li

    def compute_audio(self, entropy, good_emo, correlation, temp_li):
        value_li = [i / self.__hz for i in range(self.__hz)]
        for value in value_li:
            temp = math.cos(math.pi * 2 * entropy * value + correlation)
            temp *= good_emo
            temp_li.append(temp)
        return temp_li

    def compute_audio_1(self, emo_rate):
        value_li = [i / self.__hz for i in range(self.__hz * self.audio_size)]
        total = sum(emo_rate)
        entropy = 0.0
        good_emo, value = 0, emo_rate[0]
        for i in range(len(emo_rate)):
            rate = emo_rate[i] / total
            entropy -= rate * math.log(rate, math.e)
            if value < emo_rate[i]:
                value = emo_rate[i]
                good_emo = i
        good_emo *= emo_rate[good_emo] / total * 10
        temp_li = []
        for value in value_li:
            temp = math.cos(math.pi * 2 * entropy * value)
            temp *= good_emo
            temp_li.append(temp)
        return temp_li

    def build_audio(self):
        spec_li = []
        for file_name in os.listdir(self.__path):
            if file_name.__contains__('.D'):
                continue
            source_path = f'{self.__path}/{file_name}'
            print(f'build audio: source path : {source_path}')
            spec_image, spec_image1 = self.topic_to_1(path=source_path)
            if len(spec_image) > 0:
                spec_li.append([spec_image, spec_image1])
        return spec_li

    def topic_to_1(self, path):
        result = []
        with open(path) as f:
            line = f.readline()
            while line:
                line = line.replace('\n', '')
                att_li = line.split('\t')
                time_att = time_util.normal_to_stamp(att_li[0])
                result.append([time_att, att_li[1], att_li[2]])
                line = f.readline()
        if len(result) <= 70:
            return [], []
        result.sort(key=self.key)
        if self.audio_size != 0:
            self.__num = len(result) / self.audio_size
        data_li = self.spilt(data_li=result)
        audio_value = []
        emo_rate = [0.0, 0.0, 0.0]
        for index, current_li in enumerate(data_li):
            if index + 1 < len(data_li):
                next_li = data_li[index + 1]
            else:
                next_li = []
            if index >= self.audio_size:
                break
            entropy, good_emo, correlation = self.compute_1(current_li=current_li, next_li=next_li, emo_rate=emo_rate)
            self.compute_audio(entropy=entropy, good_emo=good_emo, correlation=correlation, temp_li=audio_value)
        audio_value1 = self.compute_audio_1(emo_rate=emo_rate)
        size = self.audio_size * self.__hz
        while len(audio_value) < size:
            audio_value.append(0.0)
        while len(audio_value1) < size:
            audio_value1.append(0.0)
        audio_value = np.asarray(audio_value)
        audio_value1 = np.asarray(audio_value1)
        spec_image = librosa.feature.mfcc(y=audio_value, sr=self.__hz)
        spec_image1 = librosa.feature.mfcc(y=audio_value1, sr=self.__hz)
        return spec_image, spec_image1
