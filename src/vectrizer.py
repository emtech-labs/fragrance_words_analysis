import sys
import json

import spacy
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer

class ContentVectorizer:
    def __init__(self, model_file=None):
        self.ginza = spacy.load('ja_ginza')

        if model_file:
            self.load_model(model_file)

    def load_model(self, model_file):
        try:
            model = Word2Vec.load(model_file, mmap="r")
        except FileNotFoundError as e:
            print(e, file=sys.stderr)
            return

        wv = model.wv
        self.ginza.vocab.reset_vectors(width=wv.vectors.shape[1])
        for word in wv.vocab.keys():
            self.ginza.vocab.set_vector(word, wv[word])

    def dump_vector(self, text: str, title=None, vector_type="doc"):
        dump_list = []
        if vector_type == "sent":
            sents_vector = self.sent_vectorize(text)
            for sent, vector in sents_vector:
                dump_vector = {
                    'text': sent.text,
                    'vector': vector.tolist(),
                }
                dump_list.append(json.dumps(dump_vector, ensure_ascii=False))

        elif vector_type == "word":
            words_vector = self.word_vectorize(text)
            for word, vector in words_vector:
                dump_vector = {
                    'text': word.text,
                    'vector': vector.tolist(),
                }
                dump_list.append(json.dumps(dump_vector, ensure_ascii=False))
        else:
            doc, vector = self.vectorize(text)
            if title is None:
                title = doc.text
            dump_vector = {
                'text': title,
                'vector': vector.tolist(),
            }
            dump_list.append(json.dumps(dump_vector, ensure_ascii=False))

        return dump_list

    def vectorize(self, text):
        doc = self.ginza(text, disable=['ner'])
        return (doc, doc.vector)

    def sent_vectorize(self, text):
        doc = self.ginza(text, disable=['ner'])
        sents_vector = []
        for sent in doc.sents:
            sents_vector.append((sent, sent.vector))

        return sents_vector

    def word_vectorize(self, text):
        doc = self.ginza(text, disable=['ner'])
        words_vector = []
        for sent in doc.sents:
            for word in sent:
                words_vector.append((word, word.vector))

        return words_vector

    def tfidf_vectorize(self):
        vectors_list = vectorizer.fit_transform([" ".join(data["metas"]) for data in data_list])