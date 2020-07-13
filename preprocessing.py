
from config import *

def clean(section):
  with open(section,"r") as f:
    text = f.readlines()      
    return([re.sub("[#.]+","#",x) for x in text])
  
def get_dictionary(section):
  word_dict = {}
  return([collections.Counter(clean(section)).most_common()])

print(get_dictionary(train_titles))
