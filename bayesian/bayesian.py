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
        """ This function take the text and category of the text to train
        classifier
        :param: text entry
        :param: category of the text
        :return: None
        """
        words = getwords(text)
        for feature in words:
            self.addfeature(feature, cat)
            self.addcatcount(cat)

    def prob_cal(self, f, cat):
        if self.cat_count(cat) == 0:
            return 0
        # Prob of a feature = feature count in a cat / total count of a cat
        return self.features_count(f, cat) / self.cat_count(cat)

    def weightedprob(self, f, cat, weight=1.0, ap=0.5):
        """ Calculate weighted probablity
        """
        # Calculate current probability
        basicprob = self.prob_cal(f, cat)

        # Count the number of times this feature has appeared in
        # all categories
        totals = sum([self.features_count(f, c) for c in self.catlist()])

        # Calculate the weighted average
        bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
        return bp

    def probdocument(self, text, cat):
        """ Assuming each word in a category is independent from the rest,
        which is the base of naive bayesian classifier, we calcluate
        probability of a string flux
        :param: text flux
        :param: category
        :return: probablity P(text|cat)
        """
        p = 1
        words = getwords(text)
        for feature in words:
            p *= self.weightedprob(feature, cat)
        return p

    def prob_cat_given_doc(self, text, cat):
        """ Pr(cat|doc)=Pr(doc|cat)*Pr(cat)/Pr(doc)
        Pr(cat|doc): posteriori, Pr(doc|cat) conditional,
        Pr(cat) priori, Pr(doc) evidence-leave out
        of Bayesian algo
        """
        pro_cat = self.cat_count(cat) / self.count_total_cat
        prodoc = self.probdocument(text, cat)
        return pro_cat * prodoc
