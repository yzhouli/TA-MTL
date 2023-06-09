from tensorflow.keras import layers, optimizers, datasets, models, losses
from keras import backend as K


class rnn_model(object):

    @staticmethod
    def lstm(h_dim, line_size):
        K.clear_session()
        model = models.Sequential()
        model.add(
            layers.LSTM(h_dim, activation='tanh', dropout=0.5, input_shape=(line_size, 100), return_sequences=True))
        # model.add(layers.LSTM(h_dim, activation='tanh', dropout=0.5, return_sequences=True))
        model.add(layers.LSTM(h_dim, activation='tanh', dropout=0.5))
        model.add(layers.Dense(3))
        return model
