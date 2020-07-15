
from config import *

class preprocessing():

  def __init__(self,train_titles,train_articles,valid_titles,valid_articles):
    self.train_articles = train_articles
    self.train_titles = train_titles
    self.valid_articles = valid_articles    
    self.valid_titles = valid_titles
    self.max_sent_len = 50
    self.max_tit_len = 15

  def clean(self,section):
  
    if section == "train":
      with open(self.train_articles,"r",encoding = 'utf-8') as f:
        articles_text_lines = f.readlines()
        articles_text_arr = [re.sub("[#.]+","#",x) for x in articles_text_lines]
      with open(self.train_titles,"r",encoding = 'utf-8') as f:
        titles_text_lines = f.readlines()   
        titles_text_arr = [re.sub("[#.]+","#",x) for x in titles_text_lines]
      return(titles_text_arr,articles_text_arr)
  
    elif section == "valid":  
      with open(self.valid_articles,"r",encoding = 'utf-8') as f:
        article_text_lines = f.readlines()
      return([[re.sub("[#.]+","#",x) for x in articles_text_lines]])

  def get_dictionary(self):
    
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

    titles,articles = self.clean("train")
    titles_words = word_tokenize(",".join(x for x in titles))
    articles_words = word_tokenize(",".join(x for x in articles))
    words = titles_words + articles_words
    words_counter = collections.Counter(words).most_common()
    for i,_ in words_counter:
      word_dict[i] = len(word_dict)
    reversed_dict = dict(zip(word_dict.values(),word_dict.keys()))
    self.word_dict = word_dict
    with open('word_dict.pkl',"wb") as f:
      pickle.dump(word_dict,f)
    with open('reversed_dict.pkl',"wb") as f:
      pickle.dump(reversed_dict,f)  
    return(word_dict,reversed_dict)

#padding the sentences and also if any of the words not in dict repalcing them with <unk> tag 
  def dataset(self,word_dict_pickle_file,section):

    if section == "train":
      article_text_arr,title_text_arr = self.clean("train")
    elif section == 'valid':
      article_text_arr = self.clean('valid')
    else:
      print("invalid argument")
    
    with open(word_dict_pickle_file,'rb') as f:
      word_dict = pickle.load(f)
    
    a = [word_tokenize(x) for x in article_text_arr]
    a = [[word_dict.get(w,word_dict["<unk>"]) for w in x] for x in a]  
    # a is a list of lists containing the embedded words of a sentence  
    a = [x[:self.max_sent_len] for x in a]
    a = [(x + (self.max_sent_len - len(x))*word_dict['<padding>']) for x in a]
    
    if section == "valid": return a
    elif section == "train":
      b = [word_tokenize(x) for x in title_text_arr]
      b = [[word_dict.get(w,word_dict["<unk>"]) for w in x] for x in a]
      b = [x[:self.max_tit_len] for x in a]
      return a,b

preprocessing = preprocessing(train_titles,train_articles,valid_titles,valid_articles)
train_x,train_y = preprocessing.dataset("word_dict.pkl","train")
print(len(train_x),len(train_y))


