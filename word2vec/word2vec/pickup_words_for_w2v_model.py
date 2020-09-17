#! usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/4/22
@author: isozaki
"""

import os
import sys
import csv
import pandas as pd
import time
sys.path.append('./utils')

from detect_meta_words_for_contents import DetectMetaWords
from text_handle_lib import TextUtils


# ---------------------------------------------------------------------------------
# メインプログラム 
#
# テキスト文からキーワードを抽出する
# ---------------------------------------------------------------------------------
if __name__ == "__main__": 

    mode_count_all = False   # すべての記事で出現したワードの出現数のカウント
    MIN_COUNT_LIMIT = 2      # 最小カウント数
    MAX_NUM_TAGS = 15        # 付加するタグの上限数

    # disp_mode     0-3  : 情報表示レベル
    # strict_mode   1: user 辞書に登録されている単語がふくまれているもののみ検出
    # process_mode  0: 統計値からワードごとのスコアー値を取得する  1: 出現データのカウント値を生成する

    argvs = sys.argv
    argc = len(argvs)

    dmw = DetectMetaWords()
    tut = TextUtils()

    if (argc != 8):
        print ('Usage: # python %s input_file request_file otput_file offset num_execute disp_mode process_mode' % argvs[0])
        quit()

    print ("### Detecting meta data") 
    in_file_name = sys.argv[1]   # 入力データ(tsv)    ex. article.tsv

    request_file_name = sys.argv[2]   # マッチングワード(tsv)    ex. common/em_motivation_words.tsv


    # 解析対象センテンスでキーフレーズを抽出する際に有効にするワードの読み込み
    request_words = []

    with open(request_file_name) as rf:
        reader = csv.DictReader(rf, delimiter='\t')
        for row in reader:
            request_words.append(row['word'] )


    out_file_name = sys.argv[3]  # 出力リスト (tsv)

    offset = int(sys.argv[4])   # Listの先頭からのオフセット
    if offset < 1: offset = 1

    num_exec = int(sys.argv[5]) # 処理する数
    if num_exec < 1: num_exec = 1

    disp_mode = int(sys.argv[6]) # Disp mode

    try:
        target_data = pd.read_table(in_file_name, sep='\t')  # tsv ファイル
    except:
        print ("Error %s cannot open!" % in_file_name)
        quit()
    target_data = target_data.fillna("")  # 欠損値 NAを""に置き換える

    process_mode = int(sys.argv[7]) #

    count_mode = False
    w2v_mode = False      
    no_filter = False

    # prosess_mode 0: Filter ON / Count OFF / Short window
    # prosess_mode 1: Filter ON / Count ON / Wide window
    # prosess_mode 2: Filter ON / Count OFF / Wide window
    # prosess_mode 3: Filter OFF  / Count OFF / Wide window
    if process_mode ==1:
        count_mode = True # True は抽出されたワード数をカウントする

    elif process_mode >0:
       w2v_mode = True       # True: word2vec モデルの生成時の一度に処理するテキストの長さをのばす
       if process_mode ==3:
           no_filter = True  # word2vec モデルの生成時にテキストを選別しない  

    start_main = time.time()

    # ------- 解析対象センテンスごとにメタ抽出する処理  ------------------------------     
    i = 0
    result = []
    count_all = {}
    count_result_all = []
    for index, row in target_data.iterrows():

        i += 1
        if i >= offset + num_exec: break
        if i >= offset:  # 処理するリスト上での開始場所

            # テキストデータのカラム情報ごとの読み込み (解析対象ごとに修正が必要）
            try:
                id = str(row.article_id)
            except:
                id = i

            try:
                title= row.title
            except:
                title= ""

            catch_copy = ""
            try:
                description= row.description
            except:
                description= row.content

            detected_keywords = {}

            if disp_mode >0 or (disp_mode ==0 and i % 100 ==1):
                print ("[%d] %s %s -----------------------------" % (i, id, title))
            if disp_mode > 1:
                print (description)
                print ("========")

            tmp = title + "。" + description # 文書のフォーマットごとに修正
            tmp = tut.word_normalize(tmp)
            if w2v_mode == False: 
               tmp = tmp.replace('@', '。')
               if len(tmp) > 36:
                   tmp = tmp.replace('、', '。')
            else:
               tmp = tmp.replace('@', ' ')

            tmp = tmp.replace('!?', '。')
            tmp = tmp.replace('\n', '')
            tmp = tmp.replace('(', ' ')
            tmp = tmp.replace(')', ' ')
            tmp = tmp.replace('（', ' ')
            tmp = tmp.replace('）', ' ')
            sentence = tmp.upper()
            feature_words_in_sentence = []
            for text in sentence.split('。'):
               feature_words, count_all = \
                    dmw.detect_feature_from_sentence(text, count_all, 1)

               matched_list = list(set(feature_words) & set(request_words) )
               if no_filter or len(matched_list) >0:
                  if w2v_mode == False and disp_mode >1: 
                     print ("XXXXX", matched_list,":", text)
                  feature_words_in_sentence += feature_words

            if len(feature_words_in_sentence) >0:
                detect_words = " ".join(feature_words_in_sentence)

                if disp_mode > 0:
                    print (">>>>>>",detect_words)

                result.append(detect_words)

    #重複削除
    result = list(set(result))

    # ファイル出力
    print ("### Writing result to file") 
    if len(result) > 0:
            summary_info = pd.DataFrame(result)
            summary_info = summary_info.fillna("") # 欠損値 NAを""に置き換える
            summary_info.columns =['words']

            summary_info.to_csv(out_file_name , sep='\t',encoding='utf-8',index=False,  header=None) # tsv file

    if count_mode:
        for wd, value in sorted(count_all.items(), key=lambda x: x[1], reverse=True):
                #detail_info, find_flag = fdi.get_info_from_userdic(wd, 0)
                #detail_str = "*"
                #if find_flag:
                #    detail_str = "|".join(detail_info[:4])
                count_result_all.append([wd, value])
                if disp_mode >0:
                    if value >1:
                        print (wd, value)

        out_file_name2 = out_file_name.split(".")[0] + "_count.tsv"
        if len(count_result_all) > 0:
            summary_info = pd.DataFrame(count_result_all)
            summary_info = summary_info.fillna("") # 欠損値 NAを""に置き換える
            summary_info.columns =['word', 'num_count']
            summary_info.to_csv(out_file_name2 , sep='\t',encoding='utf-8',index=False) # tsv file

    elapsed_time = time.time() - start_main
    print (">> Finish meta detectiont:: elapsed_time %5.3f [sec] " % (float(time.time() - start_main)) )


