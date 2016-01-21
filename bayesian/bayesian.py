import re


def getwords(text):
    word_list = re.compile('\w+').findall(text)
    unique_word_list = []
    for word in word_list:
        if word not in unique_word_list:
            unique_word_list.append(word)
    # return a dictionary with all unique words and repetition
    # freq, here it is 1
    return dict([(w, 1) for w in unique_word_list])


class classifier:
    def __init__(self):
        # Example of training data fc {'python':{'pos':0,'neg':1}....}
        # cc: category count {cat: 0}
        self.fc = {}
        self.cc = {}

    def addfeature(self, feature, cat):
        """ This function add a feature to the dict and increase it cat counting
        :param: feature
        :param: category of the feature
        :return: None
        """
        self.fc.setdefault(feature, {})
        self.fc[feature].setdefault(cat, 0)
        self.fc[feature][cat] += 1

    def addcatcount(self, cat):
        """ This function later serve as counting for calculationg probability
        :param: category of the feature
        :return: None
        """
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    def features_count(self, feature, cat):
        if feature in self.fc and cat in self.fc[feature]:
            return self.fc[feature][cat]
        return 0

    def cat_count(self, cat):
        if cat in self.cc:
            return self.cc[cat]
        return 0

    def count_total_cat(self):
        return sum(self.cc.values())

    def catlist(self):
        return self.cc.keys()

    def train(self, text, cat):
        words = getwords(text)
        for feature in words:
            self.addfeature(feature, cat)
            self.addcatcount(cat)
