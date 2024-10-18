import preprocess.preprocess as preprocess
import extract_topics.process.processer as processer
import spacy


class Extractor():
    discursos: list[list[str]]

    def __init__(self, discursos, partidos, n_components) -> None:
        self.discursos = [preprocess.preprocess(discurso)
                          for discurso in discursos]
        self.n_components = n_components
        self.treated = False
        self.partidos = partidos
        self.treated_discursos: list[list[str]]
        self.nlp: spacy.language.Language
        self.processer = processer.Processer(
            self.discursos)

    def process_text(self,
                     allowed_postags: list[str] | None = None) -> None:
        treated_discursos = self.processer.process_text(
            allowed_postags=allowed_postags)
        self.treated_discursos = treated_discursos
