import extract_topics.models.base_extractor as base_extractor
import sklearn.feature_extraction.text as sklearntext
import pandas as pd
import pathlib

import pbg


class TfidfPbg(base_extractor.Extractor):
    def __init__(self, discursos, partidos, n_components) -> None:
        super().__init__(discursos, partidos, n_components)
        self.vectorizer = sklearntext.TfidfVectorizer()
        self.data_vectorized: list
        self.feature_names: list
        self.pbg: list[pbg.PBG]
        self.topics_keywords: list[pd.DataFrame]

    def data_vectorizer(self):
        """Vectorize data to create a TF-IDF matrix that will be used to extract topics.
        Parameters:
            None.
        Returns:
            None."""
        data_vectorized = []
        feature_names = []
        for discursos_ in self.treated_discursos:
            data, feature_name = self.__data_vectorizer(
                self.vectorizer,
                discursos=discursos_)
            data_vectorized.append(data)
            feature_names.append(feature_name)
        self.data_vectorized = data_vectorized
        self.feature_names = feature_names

    def __data_vectorizer(self, vectorizer, discursos):
        matrix_discursos = vectorizer.fit_transform(discursos)
        feature_names = vectorizer.get_feature_names_out()
        return matrix_discursos, feature_names

    def topic_extraction(self, n_words):
        """Extracts the topics from a corpus utilizing PBG algorithm.
        Parameters:
            n_words: Number of words to be extracted at each topic
        Returns:
            None.
            Saves the topics at self.topics_keywords as a list of Dataframes
        """
        self.pbg = [pbg.PBG(n_components=self.n_components,
                            feature_names=feature_name,
                            save_interval=1)
                    for feature_name in self.feature_names]
        topics_discursos = []
        for i, data_vectorized in enumerate(self.data_vectorized):
            self.pbg[i].fit(data_vectorized)
            topics_discursos.append(
                self.pbg[i].get_topics(n_top_words=n_words))

        self.topics_keywords = [pd.DataFrame(topics_keywords)
                                for topics_keywords in topics_discursos]

    def to_csv(self, path: pathlib.Path | str):
        """The path must be a directory"""
        if isinstance(path, str):
            save_path = pathlib.Path(path)
        elif isinstance(path, (pathlib.Path,
                               pathlib.PosixPath,
                               pathlib.WindowsPath)):
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
