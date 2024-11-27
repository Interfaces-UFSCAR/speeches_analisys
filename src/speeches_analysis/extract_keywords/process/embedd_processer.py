from nltk.corpus import stopwords
import re


class EmbeddProcesser():
    discursos: list[list[str]] | None
    stop_words: set[str]

    def __init__(self, discursos: list[list[str]] | None = None,
                 added_stop_words: list[str] | None = None,
                 *args, **kwargs):
        if discursos is not None and discursos != []:
            self.discursos = discursos
        stop_words = set(stopwords.words("portuguese"))
        if added_stop_words is not None:
            stop_words.update(added_stop_words)
        self.stop_words = stop_words

    def sep_phrases(self, discursos: list[list[str]]) -> list[list[list[str]]]:
        sep_discursos = [self.__sep_phrases(discurso)
                         for discurso in discursos]
        return sep_discursos

    def __sep_phrases(self, discursos: list[str]) -> list[list[str]]:
        sep_discursos = []
        for discurso in discursos:
            splited = re.split(r'[.?!]', discurso)
            splited = [split.strip() for split in splited if split.strip()]
            sep_discursos.append(splited)
        return sep_discursos

    def process_text(self):
        speeches_lower = [[discurso.lower() for discurso in discursos]
                          for discursos in self.discursos]
        speeches_sep = self.sep_phrases(speeches_lower)
        return speeches_sep
