import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, optimizers, datasets, models

from to_audio.process import to_audio
from util.deep_util.deep_model.cnn_model import cnn_model
from util.deep_util.train_model.tensorflow2_normal import tensorflow2_normal


class train(object):

    def __init__(self, batch_size, source_path, train_epochs):
        self.__batch_size = batch_size
        self.__source_path = source_path
        self.__train_epochs = train_epochs

    def data_preprocess(self):
        path = f'{self.__source_path}/non'
        td = to_audio(path=path, num=20, class_num=3)
        non_li = td.build_audio()
        path = f'{self.__source_path}/rumor'
        td = to_audio(path=path, num=20, class_num=3)
        rumor_li = td.build_audio()
        return non_li, rumor_li

    @staticmethod
    def process(data_0, data_1, label):
        '''
        转换数据类型
        :param x: train_x 或者 test_x
        :param y: train_y 或者 test_y
        '''
        data_0 = tf.cast(data_0, tf.float32)
        data_1 = tf.cast(data_1, tf.float32)
        label = tf.cast(label, tf.int32)
        return data_0, data_1, label

    def data_normal(self, data_li, data_label):
        image_0, image_1 = [], []
        for data in data_li:
            image_0.append(data[0])
            image_1.append(data[1])
        image_0 = np.asarray(image_0, dtype=np.float32)
        image_0 = np.reshape(image_0, [len(image_0), len(image_0[0]), len(image_0[0][0]), 1])
        image_1 = np.asarray(image_1, dtype=np.float32)
        image_1 = np.reshape(image_1, [len(image_1), len(image_1[0]), len(image_1[0][0]), 1])
        data_label = np.asarray(data_label, dtype=np.int64)
        data_db = tf.data.Dataset.from_tensor_slices((image_0, image_1, data_label))
        data_db = data_db.map(self.process).shuffle(100000).batch(self.__batch_size)
        return data_db

    def list_max_index(self, data_li):
        max_value = max(data_li)
        for index, value in enumerate(data_li):
            if max_value == value:
                return index

    def run(self, lr):
        optimizer = optimizers.Adam(lr)
        data_li = self.data_preprocess()
        tf_normal = tensorflow2_normal(data_list=data_li, normal_data=self.data_normal)
        train_db, test_db = tf_normal.build()

        model = cnn_model(out_size=2, input_shape=(20, 188, 1))
        acc_li = []
        with tf.device('/gpu:0'):
            for epoch in range(self.__train_epochs):
                loss_total = 0
                for step, (image_0, image_1, y) in enumerate(train_db):
                    with tf.GradientTape() as tape:
                        out = model(image_0, image_1)
                        loss = tf.losses.categorical_crossentropy(y, out, from_logits=True)
                        loss = tf.reduce_mean(loss)
                        loss_total += loss
                        grads = tape.gradient(loss, model.trainable_variables)
                        optimizer.apply_gradients(zip(grads, model.trainable_variables))
                print(f'epoch: {epoch}, loss: {loss_total}')
                total_sum, total_true = 0.0, 0.0
                for (image_0, image_1, y) in test_db:
                    out = model(image_0, image_1)
                    for index, out_type in enumerate(out):
                        predict_type = self.list_max_index(out_type)
                        real_type = self.list_max_index(y[index])
                        if predict_type == real_type:
                            total_true += 1
                        total_sum += 1
                acc = total_true / total_sum
                acc_li.append(acc)
                print(f'epoch: {epoch}, accuracy: {acc}')
        print(f'max acc: {acc}')


if __name__ == '__main__':
    source_path = '../database'
    batch_size = 128
    train_epochs = 10
    model_train = train(source_path=source_path, batch_size=batch_size, train_epochs=train_epochs)
    model_train.run(lr=0.004)
