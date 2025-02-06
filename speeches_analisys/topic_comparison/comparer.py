"""
This module consists on a class to compare to sets of topics.
The class Comparer uses gensim in order to use word embedding \
    to set similarity between topics.
"""

import pathlib
import typing
import gensim.downloader as api
from gensim import models as gensim_models
from sklearn.metrics import pairwise
import numpy as np

from . import model as models


class Comparer():
    """
    This class is made to compare different topics in the speeches.
    This class will use word embedding in order to do so"""
    wv: gensim_models.KeyedVectors
    topics: list[list[list[str]]]
    embeddings: typing.Any
    cosine_matrixes: list
    correlated_topics: models.SimilarTopic

    def __init__(self, topics: list[list[list[str]]]):
        if len(topics) > 2:
            raise ValueError("There should not be more than 2 \
                             topic sets when comparing")
        self.topics = topics

    def load_model_api(self,
                       model: str = "word2vec-google-news-300",
                       return_path: bool = False):
        """Loads a gensim model from the gensim API

        Consult the available options on: \
            https://github.com/piskvorky/gensim-data"""
        self.wv = api.load(model, return_path=return_path)

    def load_model_word2vec(self,
                            model: pathlib.Path,
                            binary: bool = False):
        """Loads a gensim model from word2vec file"""
        wv = gensim_models.KeyedVectors.load_word2vec_format(model,
                                                             binary=binary)
        self.wv = wv

    def string_to_vector(self, s: str):
        """Converts the given string into a Word2Vec vector"""
        vector = self.wv[s]
        return vector

    def extract_embeddings_single(self, topics):
        """Extracts the embeddings for a single topics set"""
        if self.wv is None or self.topics is None:
            raise KeyError("Either model or topics were not set")
        embeddings = [[self.string_to_vector(s)
                       for s in topic]
                      for topic in topics]
        return embeddings

    def extract_embeddings(self):
        """Extracts the embeddings for all the data on the topics"""
        embeddings = []
        for topics in self.topics:
            embeddings.append(self.extract_embeddings_single(topics))
        self.embeddings = embeddings

    def calculate_cosine_pair(self, topic1, topic2) -> np.ndarray:
        """Calculates the cosine similarity matrix given 2 topics.
        This function is made to use with calculate_cosine"""
        cosine_matrix = pairwise.cosine_similarity(topic1, topic2)
        return cosine_matrix

    def calculate_cosine(self):
        """
        This function calculates all matrix of cosine similarity
        """
        cosine_matrixes = []
        for topic in self.embeddings[0]:
            topic_matrixes = []
            for topic2 in self.embeddings[1]:
                topic_matrixes.append(self.calculate_cosine_pair(topic,
                                                                 topic2))
            cosine_matrixes.append(topic_matrixes)
        self.cosine_matrixes = cosine_matrixes

    def find_similar_topics(self,
                            limit: float = 0
                            ) -> models.SimilarTopic:
        """Calculates the correlated topics.

        The function creates a list of tuples which have the most correlated topics.
        The function returns the list of tuples if necessary.

        It also sets an attribute on the class which contains the data.

        # Attributes
        - limit: float.
        Defines the threshold for considering a topic similar. [0,1].
        By default the value is 0, considering any diference between topics.
        In this case, every topic will have a similar topic,
        which may be very similar or not.
        """
        correlated_topics = []
        similarity: list[float | None] = []
        for i, topic_matrixes in enumerate(self.cosine_matrixes):
            # Calculates the mean of the matrix of cosine similarity between the topics
            mean = [np.mean(topic_matrix) for topic_matrix in topic_matrixes]
            # Finds the position of the most similar topic to the topic we are looking at
            highest_index = np.argmax(mean)
            # If the mean of the matrix is greater than the threshold
            # Sets it on the correlated topics
            if mean[highest_index] >= limit:
                similarity.append(mean[highest_index])
                topic1 = self.topics[0][i]
                topic2 = self.topics[1][highest_index]
                correlated_topics.append(tuple([topic1, topic2]))
            else:
                similarity.append(None)
                correlated_topics.append(tuple())
        self.correlated_topics = models.SimilarTopic(topics=correlated_topics,
                                                     similarity=similarity)
        return self.correlated_topics

    def calculate(self, threshold: float = 0):
        """Calculates the similarity between topics

        # Attibutes:
        - threshold: float [0,1]. Used to set the threshold difference between topics.
        Filters some not so similar topics."""
        self.extract_embeddings()
        self.calculate_cosine()
        return self.find_similar_topics(limit=threshold)
