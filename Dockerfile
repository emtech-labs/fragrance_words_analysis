FROM shunk031/mecab-neologd-py3

# nodejsの導入
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash - \
    && sudo apt-get install -y nodejs

RUN pip install -U pip && \
    pip install fastprogress japanize-matplotlib && \
    pip install jupyterlab && \
    pip install ipywidgets && \
    pip install pandas

RUN pip install networkx && \
    pip install ginza

RUN jupyter nbextension enable --py widgetsnbextension
