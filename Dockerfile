FROM shunk031/mecab-neologd-py3

# nodejsの導入
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash - \
    && sudo apt-get install -y nodejs

RUN pip install -U pip && \
    pip install fastprogress japanize-matplotlib && \
    pip install jupyterlab && \
    pip install ipywidgets


RUN pip install pandas &&\
    pip install networkx

RUN pip install mecab-python3 && \
    pip install unidic-lite

RUN pip install -U scikit-learn && \
    pip install fasttext && \
    pip install gensim

RUN jupyter nbextension enable --py widgetsnbextension