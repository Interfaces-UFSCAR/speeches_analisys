class SimilarTopic():
    topics: list[tuple[list[str], list[str]]]
    similarity: list[float | None]

    def __init__(self, topics, similarity):
        self.topics = topics
        self.similarity = similarity

    def __str__(self):
        final = []
        for topic, similarity in zip(self.topics, self.similarity):
            final.append(" ".join([topic, similarity]))
        return "\n".join(final)

    def calculate_diff_topics(self):
        diff_topics = set()
        for topic in self.topics:
            diff_topics.add(topic[1])
        num_diff = len(diff_topics)
        return num_diff
