#! usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/4/22
@author: isozaki
"""

import os
import sys
import codecs
import pandas as pd
from gensim.models import word2vec

if __name__ == "__main__":

    argvs = sys.argv
    argc = len(argvs)
 
    if (argc != 3):
        print ('Usage: # python %s input_file otput_file' % argvs[0])
        quit()

    in_file_name = sys.argv[1]   # 入力データ(tsv) の集計ファイル   ex. video_all.tsv
    out_file_name = sys.argv[2]  # 出力リスト (bin)

    #data = word2vec.Text8Corpus('result/review_feature_words.tsv')
    data = word2vec.Text8Corpus(in_file_name)

    # CBOW(Continuous Bag-of-Words)は単語周辺の文脈から単語を推定します。
    # 基本的にはNNです。

    # Word2Vecのインスタンス作成
    # sentences : 対象となる分かち書きされているテキスト
    # size      : 出力するベクトルの次元数
    # min_count : この数値よりも登場回数が少ない単語は無視する
    # window    : 一つの単語に対してこの数値分だけ前後をチェックする

    #model = word2vec.Word2Vec(data, size=100, workers=4, min_count=5, window=5)
    #model = word2vec.Word2Vec(data, size=200, workers=4, sg=0)
    #model.save("review_CBOW.bin")

    #skip-gramはCBOWの逆で,単語から文脈中の一単語を推定します。
    #NNの隠れ層の出力を取り出す手法で入力データの特徴を低次元で表現した隠れ層を取り出す。
    #イメージとしては主成分分析。

    model = word2vec.Word2Vec(data, size=100, workers=4, sg=1, min_count=5, window=10)
    #model = word2vec.Word2Vec(data, size=200, workers=4, sg=1) # skip-gram 
    #model.save("review_sgram.bin")
    model.save(out_file_name)

