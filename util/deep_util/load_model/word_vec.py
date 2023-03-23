from gensim.models import Word2Vec


class Wvc_Util(object):

    @staticmethod
    def load(model_path):
        return Word2Vec.load(model_path)
