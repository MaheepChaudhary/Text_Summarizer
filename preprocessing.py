
from config import *

class preprocessing():

  def __init__(self,train_titles,train_articles,valid_titles,valid_articles):
    self.train_articles = train_articles
    self.train_titles = train_titles
    self.valid_articles = valid_articles    
    self.valid_titles = valid_titles

  def clean(self,section):
  
    if section == "train":
      with open(self.train_articles,"r") as f:
        articles_text_lines = f.readlines()
        articles_text_arr = [re.sub("[#.]+","#",x) for x in articles_text_lines]
      with open(self.train_titles,"r") as f:
        titles_text_lines = f.readlines()   
        titles_text_arr = [re.sub("[#.]+","#",x) for x in titles_text_lines]
      return(titles_text_arr,articles_text_arr)
  
    elif section == "valid":  
      with open(self.valid_articles,"r") as f:
        article_text_lines = f.readlines()
        return([[re.sub("[#.]+","#",x) for x in articles_text_lines]])

  def get_dictionary(self,section):
    
    word_dict = {}
    reversed_dict = {}
    word_dict["<padding>"] = 0
    word_dict["<unk>"] = 1
    word_dict["<s>"] = 2
    word_dict["</s>"] = 3
    titles = []
    titles_text = ''
    articles_text = ''
    articles = []

    if section == "train":
      titles,articles = self.clean("train")
      titles_words = word_tokenize(",".join(x for x in titles))
      articles_words = word_tokenize(",".join(x for x in articles))
      words = titles_words + articles_words
      words_counter = collections.Counter(words).most_common()
      for i,_ in words_counter:
        word_dict[i] = len(word_dict)
      reversed_dict = dict(zip(word_dict.values(),word_dict.keys()))
    max_sent_len = 50
    max_summary_len = 15
    return(word_dict,reversed_dict,max_sent_len,max_summary_len)

#preparing the dataset

  


