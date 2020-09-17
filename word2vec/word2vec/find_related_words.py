# coding: utf-8
#from __future__ import division
import os
import sys
import csv
import pandas as pd

sys.path.append('./utils')

from gensim.models import word2vec

#-------------------------------------------------------------
# word2vec のモデルから query words に関連するワードを抽出する
#-------------------------------------------------------------
if __name__ == "__main__": 

    NUM_MAX_WORDS = 20    # 関連ワード数
    # disp_mode     0-1  : 情報表示レベル

    argvs = sys.argv
    argc = len(argvs)

    if (argc != 6):
        print ('Usage: # python %s in_file model_name offset num_execute disp_mode' % argvs[0])
        quit()

    in_file = sys.argv[1]   # 関連ワードを調べる対象データ(tsv)    ex. "query_words.tsv"
    model_name = sys.argv[2]   # word2vec モデル  ex. model/model_all.bin
    offset = int(sys.argv[3])   # 処理開始番号

    try:
       model = word2vec.Word2Vec.load(model_name)
    except:
       print ("%s not found !" % model_name)
       quit()

    num_exec = int(sys.argv[4]) # 処理する数
    if num_exec < 1: num_exec = 1

    disp_mode = int(sys.argv[5]) # Disp mode

    query_words = {}

    with open(in_file) as rf:
        reader = csv.DictReader(rf, delimiter='\t')
        for row in reader:
            id = row['id']
            query_words[id] = {}
            query_words[id]['phrase'] = row['phrase']
            query_words[id]['positive'] = []  
            query_words[id]['negative'] = []  
            if len(row['word_positive']) >0:  
                query_words[id]['positive'] += row['word_positive'].split(" ")
            if len(row['word_negative']) >0:  
                query_words[id]['negative'] = row['word_negative'].split(" ") 
  

    result = []
    summary_info = {}
    i = 0
    for id in query_words:
      i += 1
      if i >= offset + num_exec: break
      if i >= offset:  # 処理するリスト上での開始場所

        target_word = query_words[id]['positive']
        target_negative = query_words[id]['negative']


        phrase =  query_words[id]['phrase'] 
        if not phrase in summary_info:
            summary_info[phrase] = {}
        
        if disp_mode >0:
            print ("----------------------------------\n")
            print (phrase)
            print ("positive=", " ".join(target_word), "negative=", " ".join(target_negative))
            print ("----------------------------------" )

        try:
            out = model.most_similar(positive=target_word, negative=target_negative, topn=NUM_MAX_WORDS)
            for x in out:
                word = x[0].upper()
                score = int(float(x[1])*10000)/10000
                print (word, score) 
        except:
          if disp_mode >=0:
                print ("Not found:",  phrase, " ".join(target_word))

