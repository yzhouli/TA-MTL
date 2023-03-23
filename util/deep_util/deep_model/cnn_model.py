import tensorflow as tf
from tensorflow.keras import layers, optimizers, datasets, models
from tensorflow import keras


class cnn_model(keras.Model):

    def __init__(self, out_size=0, input_shape=0):
        super(cnn_model, self).__init__()
        self.cnn1 = layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape)
        self.cnn1_1 = layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape)
        self.cnn2 = layers.Conv2D(64, (3, 3), activation='relu')
        self.cnn2_1 = layers.Conv2D(64, (3, 3), activation='relu')
        self.cnn3 = layers.Conv2D(64, (3, 3), activation='relu')
        self.cnn3_1 = layers.Conv2D(64, (3, 3), activation='relu')
        self.mp = layers.MaxPooling2D((2, 2))
        self.flatten = layers.Flatten()
        self.fc1 = layers.Dense(256, activation='relu')
        self.fc1_1 = layers.Dense(256, activation='relu')
        self.fc2 = layers.Dense(128, activation='relu')
        self.fc3 = layers.Dense(out_size)

    def call(self, inputs_0, inputs_1, training=None):
        out_0 = self.cnn1(inputs_0)
        out_0 = self.mp(out_0)
        # out_0 = self.cnn2(out_0)
        out_0 = self.flatten(out_0)
        # out_0 = self.fc1(out_0)

        out_1 = self.cnn1(inputs_1)
        out_1 = self.mp(out_1)
        # out_1 = self.cnn2(out_1)
        out_1 = self.flatten(out_1)
        # out_1 = self.fc1_1(out_1)

        out = tf.concat([out_0, out_1], 1)
        out = self.fc2(out)
        out = self.fc3(out)
        return out
