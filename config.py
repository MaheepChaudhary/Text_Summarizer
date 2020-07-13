
import sys
sys.path.append('/home/maheep/nlp/lib/python3.6/site-packages')

import collections
import nltk
import gensim
from nltk.tokenize import word_tokenize
import os
import re

path = './train'
train_articles = os.path.join(path,'train.article.txt')
train_titles = os.path.join(path,'train.title.txt')
valid_articles = os.path.join(path,'valid.article.filter.txt')
valid_titles = os.path.join(path,'valid.title.filter.txt')

