import string
import spacy
from nltk.corpus import stopwords
import nltk


class NetProcesser():
    discursos: list[list[str]] | None
    stop_words: set[str]

    def __init__(self, discursos: list[list[str]] | None = None,
                 added_stop_words: list[str] | None = None,
                 *args, **kwargs):
        self.nlp: spacy.language.Language
        nltk.download("stopwords")
        if discursos is not None and discursos != []:
            self.discursos = discursos
        stop_words = set(stopwords.words("portuguese"))
        if added_stop_words is not None:
            stop_words.update(added_stop_words)
        self.stop_words = stop_words
        pass

    def __remove_stop_words_punct(self,
                                  discursos: list[list[str]]) -> list[str]:
        novos_discursos = []
        for discurso in discursos:
            novo_discurso = []
            for token in discurso:
                if ((token not in string.punctuation)
                        and (token not in self.stop_words)):
                    novo_discurso.append(token)
                novo_discurso_str = " ".join(novo_discurso)
                novos_discursos.append(novo_discurso_str)
        return novos_discursos

    def lemmatization(self, allowed_postags=None):
        lemmatized_discursos = [self.__lemmatization(
            discursos, self.nlp,
            allowed_postags=allowed_postags)
                                for discursos in self.discursos]
        return lemmatized_discursos

    def __lemmatization(self,
                        texts: list[str],
                        nlp,
                        allowed_postags: list[str] | None = None):
        if allowed_postags is None:
            allowed_postags = ["NOUN", "ADJ", "VERB", "ADV"]
        texts_out: list[str] = []
        for sent in texts:
            doc = nlp(sent)
            texts_out.append(" ".join([token.lemma_
                                       if token.lemma_ not in ["-PRON-"]
                                       else ""
                                       for token in doc
                                       if token.pos_ in allowed_postags]))
        return texts_out

    def process_text(self, allowed_postags: list[str] | None = None) -> list[list[str]]:
        self.nlp = spacy.load("pt_core_news_lg")
        lemmatized_speeches = self.lemmatization()
        speeches_lower = [[speech.lower() for speech in speeches]
                          for speeches in lemmatized_speeches]
        speeches_tokenized = [[nltk.word_tokenize(speech)
                               for speech in speeches]
                              for speeches in speeches_lower]
        speeches_treated = [self.__remove_stop_words_punct(speeches)
                            for speeches in speeches_tokenized]
        return speeches_treated
