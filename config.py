import sys
sys.path.append('/home/maheep/nlp/lib/python3.6/site-packages')
import collections
import nltk
import gensim
from nltk.tokenize import word_tokenize
import os
import re
import pickle 
import tensorflow.keras as tf
from tensorflow.keras.layers import Input,Embedding,LSTM
from tensorflow.keras.models import Model

path = './train'
train_articles = os.path.join(path,'train.article.txt')
train_titles = os.path.join(path,'train.title.txt')
valid_articles = os.path.join(path,'valid.article.filter.txt')
valid_titles = os.path.join(path,'valid.title.filter.txt')
max_sent_len = 50
max_tit_len = 15
