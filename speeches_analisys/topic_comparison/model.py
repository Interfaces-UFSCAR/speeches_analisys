"""
This module has a class to retain the most similar topics and it's similarities.
"""


class SimilarTopic():
    """
    This class is a model to store the similar topics and its similarities.
    This class should usually be saved using pickle methods"""
    topics: list[tuple[list[str], list[str]]]
    similarity: list[float | None]

    def __init__(self, topics, similarity):
        self.topics = topics
        self.similarity = similarity

    def __str__(self):
        final = []
        for similar_topics, similarity in zip(self.topics, self.similarity):
            line = []
            for topic in similar_topics:
                line.append(str(topic))
            line.append(str(similarity))
            line = " ".join(line)
            final.append(line)
        return "\n".join(final)

    def __eq__(self, value):
        for self_topics, self_similarity, value_topics, value_similarity in \
                zip(self.topics,
                    self.similarity,
                    value.topics,
                    value.similarity):
            if self_topics != value_topics:
                return False
            if self_similarity != value_similarity:
                return False
        return True
