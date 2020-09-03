#!/usr/bin/env python
# coding: utf-8

import csv
import pandas as pd


class ConvertDict:

  def make_worddict(self,
      word,
      score1='-1',
      score2='-1',
      pos='名詞',
      pos_datail='一般',
      unused='*',
      normalization=None,
      abstraction=None,
      category1='*',
      interpretation='*',
      category2='*',
      attribute='*',
      category3='*',
      wordtype='名詞',
      writer='mydic'):

      newword_dic = {}
      newword_dic['word'] = word
      newword_dic['score1'] = score1
      newword_dic['score2'] = score2
      newword_dic['weight'] = len(word)*(-100)
      newword_dic['pos'] = pos
      newword_dic['pos_datail'] = pos_datail
      newword_dic['unused1']=unused
      newword_dic['unused2']=unused
      newword_dic['unused3']=unused
      newword_dic['unused4']=unused
      if normalization is None:
        newword_dic['normalization']=word
      else:
        newword_dic['normalization']=normalization
      if abstraction is None:
        newword_dic['abstraction']=word
      else:
        newword_dic['abstraction']=normalization
      newword_dic['category1']=category1 #M列
      newword_dic['interpretation']=interpretation
      newword_dic['category2']=category2
      newword_dic['attribute']=attribute
      newword_dic['category3']=category3
      newword_dic['wordtype']=wordtype
      newword_dic['writer']=writer

      return newword_dic


  def output_str(self,newword_dic):
      key_order=['word',
      'score1',
      'score2',
      'weight',
      'pos',
      'pos_datail',
      'unused1',
      'unused2',
      'unused3',
      'unused4',
      'normalization',
      'abstraction',
      'category1',
      'interpretation',
      'category2',
      'attribute',
      'category3',
      'wordtype',
      'writer']

      newword_list=[]
      for k in key_order:
        newword_list.append(newword_dic[k])

      return newword_list


  def convert(self,addwords):
    f = open('/Users/kayo/workspace/perfume/perfume_table/src/result/newword_dict.csv', 'w', encoding='shift_jis')
    writer = csv.writer(f, lineterminator='\n')
    for w in addwords:
      nworddic=self.make_worddict(w,category2='香り')
      outputlist=self.output_str(nworddic)
      writer.writerow(outputlist)

    f.close()


if __name__=='__main__':
  cd=ConvertDict()

  addw_fn = '/Users/kayo/workspace/perfume/perfume_table/addwords.csv'
  addwords = []

  with open(addw_fn) as f:
    reader = csv.reader(f)
    for w in reader:
      #print(w[0])
      addwords.append(w[0])
    cd.convert(addwords)
  print('output: /Users/kayo/workspace/perfume/perfume_table/src/newword_dict.csv')
