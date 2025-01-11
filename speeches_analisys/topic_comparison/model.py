import pickle
import pathlib


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

    def calculate_diff_topics(self):
        diff_topics = set()
        for topic in self.topics:
            diff_topics.add(topic[1])
        num_diff = len(diff_topics)
        return num_diff

    def to_pickle(self, file: pathlib.Path):
        with open(file, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
