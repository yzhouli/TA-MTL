import jieba


class txt_opera(object):

    @staticmethod
    def load(path, replace='\n'):
        result_li = []
        with open(path) as f:
            line = f.readline()
            while line:
                line = line.replace(replace, '')
                result_li.append(line)
                line = f.readline()
        return result_li

    @staticmethod
    def copy(source_path, target_path, renew=False, process=False):
        model = 'a+'
        if renew:
            model = 'w+'
        with open(source_path) as fr:
            with open(target_path, model) as fw:
                line = fr.readline()
                while line:
                    if process:
                        line = process(line)
                    fw.write(line)
                    line = fr.readline()

    @staticmethod
    def cut_to_word(line):
        line = jieba.cut(line)
        return '\t'.join(line)
