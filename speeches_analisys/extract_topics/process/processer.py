import string
import spacy
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import download


class Processer():
    """
    This class processes the text

    It lemmatizes, lower and remove stop words of all the text."""
    nlp: spacy.language.Language
    discursos: list[list[str]] | None
    stop_words: set[str]

    def __init__(self, discursos: list[list[str]] | None = None,
                 added_stop_words: list[str] | None = None) -> None:
        self.nlp: spacy.language.Language
        download("stopwords")
        download("punkt_tab")
        if discursos is not None and discursos != []:
            self.discursos = discursos
        stop_words = set(stopwords.words("portuguese"))
        if added_stop_words is not None:
            stop_words.update(added_stop_words)
        self.stop_words = stop_words

    def lemmatization(self, allowed_postags):
        lemmatized_discursos = [self.__lemmatization(discursos, self.nlp, allowed_postags) for discursos in self.discursos]
        return lemmatized_discursos

    def __lemmatization(self,
                        texts: list[str],
                        nlp,
                        allowed_postags: list[str] | None = None):
        if allowed_postags is None:
            allowed_postags = ["NOUN", "ADJ", "VERB", "ADV"]
        texts_out = []
        for sent in texts:
            doc = nlp(sent)
            texts_out.append(" ".join([token.lemma_
                                       if token.lemma_ not in ["-PRON-"]
                                       else ""
                                       for token in doc
                                       if token.pos_ in allowed_postags]))
        return texts_out

    def __remove_stop_words_punct(self,
                                  discursos: list[list[str]]) -> list[str]:
        novos_discursos = []
        punctuation = string.punctuation
        for discurso in discursos:
            novo_discurso = []
            for token in discurso:
                if ((token not in punctuation)
                        and (token not in self.stop_words)):
                    novo_discurso.append(token)
                novo_discurso_str = " ".join(novo_discurso)
                novos_discursos.append(novo_discurso_str)
        return novos_discursos

    def process_text(self,
                     allowed_postags: list[str] | None = None
                     ) -> list[list[str]]:
        self.nlp = spacy.load("pt_core_news_lg")
        print("Modelo carregado")
        lemmatized_discursos = self.lemmatization(allowed_postags)
        print("Textos lemmatizados")
        del self.nlp
        discursos_lower = [[discurso.lower()
                            for discurso in discursos]
                           for discursos in lemmatized_discursos]
        print("Textos em lower")
        del lemmatized_discursos
        discursos_tokenized = [[word_tokenize(discurso)
                                for discurso in discursos]
                               for discursos in discursos_lower]
        print("Textos tokenizados")
        del discursos_lower
        treated_discursos = [self.__remove_stop_words_punct(
            discursos=discursos)
            for discursos in discursos_tokenized]
        print("Stopwords removidas")
        del discursos_tokenized
        return treated_discursos
