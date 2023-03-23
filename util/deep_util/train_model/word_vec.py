import os

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

from util.data_util.file_opera.txt_opera import txt_opera


class Word_Vec(object):

    def __init__(self, file_path, path_list=False, save_path=False, path=False, remove_file=True, vector_size=100,
                 tab='&'):
        """
        Word2Vec 自定义训练方法
        :param path_list: 源数据存放地址（多个地址）
        :param save_path: 训练好的模型存放地址
        :param path: 源数据存放地址（单个txt文件）
        :param remove_file: 是否删除模型训练时创建的分词文件
        :param vector_size: 向量长度
        :param file_path 分词文件存放地址
        """
        self.__path_list = path_list
        self.__save_path = save_path
        self.__path = path
        self.__remove_file = remove_file
        self.__vector_size = vector_size
        self.__file_path = file_path
        self.__tab = tab

    def __copy_text_item(self, path):
        """
        有多个数据地址时，构建分词文件
        :param path: 分词文件地址
        """
        for file_name in os.listdir(path):
            if file_name.__contains__('.D'):
                continue
            file_path = f'{path}/{file_name}'
            if os.path.isdir(file_path):
                self.__copy_text_item(path=file_path)
                continue
            renew = False
            if not os.path.exists(self.__file_path):
                renew = True
            txt_opera.copy(source_path=file_path, target_path=self.__file_path, renew=renew,
                           process=txt_opera.cut_to_word)

    def __build_file(self):
        """
        构建分词文件
        """
        print('build word2vev train cut file:')
        if self.__path:
            txt_opera.copy(source_path=self.__path, target_path=self.__file_path, renew=True,
                           process=txt_opera.cut_to_word)
        else:
            for dir_path in self.__path_list:
                self.__copy_text_item(path=dir_path)
        with open(self.__file_path, 'a+') as f:
            f.write(f'{self.__tab}\n')

    def __train_model(self):
        """
        模型训练
        """
        print('train word2vev model')
        model = Word2Vec(
            LineSentence(open(self.__file_path, 'r', encoding='utf8')),
            sg=0,
            window=3,
            min_count=0,
            workers=8,
            vector_size=self.__vector_size
        )
        if self.__save_path:
            # 模型保存
            print(f'model path: {self.__save_path}')
            model.save(self.__save_path)
        print('train word2vev model finish')
        return model

    def build(self):
        """
        自定义数据集的Word2Vec模型训练方法
        :return: 训练好的Word2Vec模型
        """
        self.__build_file()
        wvc_model = self.__train_model()
        if self.__remove_file:
            print('remove cut file')
            os.remove(self.__file_path)
        return wvc_model


if __name__ == '__main__':
    source_path_list = ['../../../database/emotion/classify_3']
    wvc_model = Word_Vec(path_list=source_path_list)
    wvc = wvc_model.build()
    print(wvc)
