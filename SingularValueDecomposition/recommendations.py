import dataproc as dt


def similarity(prefs, person1, person2):
    """ Compute how similar two movie critics are in their tastes,
    based on their critics.
    You do this by comparing each person with every other person
    and calculating a similarity score.

    :param prefs: dict - critics as defined in data.py
    :param person1: str - movie critic's name
    :param person2: str - movie critic's name

    :return: float - similarity score
    """
    svd = dt.train_svd(prefs)
    similarity_score = svd.similarity(person2, person1)
    return similarity_score


def top_matches(prefs, person, n=5):
    """ Rank movie critics matches for `person` from `perfs`.

    :param prefs: dict - critics as defined in data.py
    :param person: str - movie critic's name to compare others to
    :param n: int - number of movie critics to rank

    :return: list[tuple(float, str)] - ranking of (score, critic's name)
    """
    svd = dt.train_svd(prefs)
    result = svd.similar(person, n)
    return dt.format_data(result)


def get_recommendations(prefs, person):
    """ Recommend movies to `person` matching others' ratings with his.

    :param prefs: dict - critics as defined in data.py
    :param person: str - movie critic's name to advise

    :return: list[tuple(float, str)] - ranking of (score, film's title)

    Note that in this function, only movie which user has not rated
    will be recommended
    """
    n = 3
    svd = dt.train_svd(prefs)
    result = svd.recommend(person, n, only_unknowns=True, is_row=True)
    return dt.format_data(result)
