import pathlib
import sklearn.feature_extraction.text as sklearntext
import sklearn.decomposition as decomposition
import numpy as np
import pandas as pd
from . import base_extractor


class BowLda(base_extractor.Extractor):
    def __init__(self, discursos, partidos, n_components) -> None:
        super().__init__(discursos, partidos, n_components)
        self.vectorizer = sklearntext.CountVectorizer(analyzer="word",
                                                      stop_words=None,
                                                      lowercase=True)
        self.topics_keywords: list[pd.DataFrame]
        self.lda_models: list[decomposition.LatentDirichletAllocation]
        self.data_vectorized: list
        self.feature_names: list

    def topic_extraction(self, n_words):
        self.lda_models = [self.__lda_transform_fit(data_vectorized_)
                           for data_vectorized_ in self.data_vectorized]
        topics_keywords_lst = [
            self.__transform_topics(feature_name,
                                    self.lda_models[i].components_,
                                    n_words) for i, feature_name in enumerate(
                                        self.feature_names
                                    )
        ]
        self.topics_keywords = [pd.DataFrame(topics_keywords)
                                for topics_keywords in topics_keywords_lst]

    def to_csv(self, path: pathlib.Path | str):
        """The path must be a directory"""
        if isinstance(path, str):
            save_path = pathlib.Path(path)
        elif (isinstance(path, pathlib.Path)) \
            or (isinstance(path, pathlib.PosixPath)) \
                or (isinstance(path, pathlib.WindowsPath)):
            save_path = path
        else:
            raise TypeError()
        save_path.mkdir(parents=True, exist_ok=True)
        for i, df in enumerate(self.topics_keywords):
            topics_path = save_path.joinpath(f"topics_{self.partidos[i]}.csv")
            df.columns = pd.Index(["Word " + str(i)
                                   for i in range(df.shape[1])])
            df.index = pd.Index(["Topic " + str(i)
                                 for i in range(df.shape[0])])
            df.to_csv(topics_path)

    def data_vectorizer(self):
        """Vectorize the data in the class to create a Bow Matrix of each party."""
        data_vectorized = []
        feature_names = []
        for discursos_ in self.treated_discursos:
            data, feature_name = self.__data_vectorizer(self.vectorizer,
                                                        discursos=discursos_)
            data_vectorized.append(data)
            feature_names.append(feature_name)
        self.data_vectorized = data_vectorized
        self.feature_names = feature_names

    def __data_vectorizer(self,
                          vectorizer: sklearntext.CountVectorizer,
                          discursos: list):
        matrix_discursos = vectorizer.fit_transform(discursos)
        feature_names = vectorizer.get_feature_names_out()
        return matrix_discursos, feature_names

    def __lda_transform_fit(self,
                            data_vectorized: np.ndarray
                            ) -> decomposition.LatentDirichletAllocation:

        lda_model = decomposition.LatentDirichletAllocation(
            learning_method="online",
            random_state=100,
            batch_size=128,
            evaluate_every=-1,
            n_jobs=-1,
            n_components=self.n_components
        )
        # Applies the data to the model before saving it
        # The result is not captured once it's not used
        lda_model.fit_transform(data_vectorized)
        return lda_model

    def __transform_topics(self,
                           feature_names: np.ndarray,
                           lda_model_components: np.ndarray,
                           n_words=20) -> list:

        keywords = np.array(feature_names)
        topic_keywords = []
        for topic_weights in lda_model_components:
            top_keyword_locs = (-topic_weights).argsort()[:n_words]
            topic_keywords.append(keywords.take(top_keyword_locs))
        return topic_keywords
