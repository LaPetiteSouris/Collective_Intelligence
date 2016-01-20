import re


def getwords(text):
    word_list = re.compile('\w+').findall(text)
    uniqe_word_list = []
    for word in word_list:
        if word not in uniqe_word_list:
            uniqe_word_list.append(word)
    # return a dictionary with all unique words and repetition
    # freq, here it is 1
    return dict([(w, 1) for w in uniqe_word_list])
