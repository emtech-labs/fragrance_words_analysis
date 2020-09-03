# CSVをDICに書き換えるためのやつ

cd ../data

nkf -wLu --overwrite fragrance_user_dic.csv
cp fragrance_user_dic.csv mecab_tmp_dic.csv
 /usr/local/libexec/mecab/mecab-dict-index -d /usr/local/lib/mecab/dic/ipadic -u fragrance_user_dic.csv -f utf-8 -t utf-8 mecab_tmp_dic.csv
rm mecab_tmp_dic.csv