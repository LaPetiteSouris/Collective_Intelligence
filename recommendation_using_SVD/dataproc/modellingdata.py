__author__ = 'Tung Hoang'

"""
This class handling data processing tasks, including convert raw data to compatible matrix, train Singular Value Decomposition (SVD) model

"""

from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data


def get_data_model_matrix(data):
    """
    This method process raw data and store rating/users/movies in a matrix <value/row/column> respectively
    using recsys library
    :return: data object (recsys.datamodel.Data()) )
    """
    processed_data = Data()
    for user, review in data.items():
        for mov, rat in review.items():
            processed_data.add_tuple((rat, user, mov))
    return processed_data


def train_svd(data):
    """
    This method load processed data and modelling data using Singular Value Decomposition
    :return: SVD model
    """
    svd = SVD()
    svd.set_data(get_data_model_matrix(data))
    k = 30
    svd.compute(k=k, min_values=0, pre_normalize=None, mean_center=True, post_normalize=True)
    return svd


def format_data(list_tuple):
    """ Format recommendation from SVD model into correct format for unit test

   :param prefs: return value from SVD model

   :return: list[tuple(float, str)]
   """
    list_correct_format = []
    for tuple_item in list_tuple:
        new_tuple = tuple_item[::-1]
        list_correct_format.append(new_tuple)
    return list_correct_format
