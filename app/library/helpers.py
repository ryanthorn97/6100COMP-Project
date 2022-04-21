import json
import os.path
import markdown

class obj:
      
    # constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)

def dict2obj(dict1):
      
    # using json.loads method and passing json.dumps
    # method and custom object hook as arguments
    return json.loads(json.dumps(dict1), object_hook=obj)


def openfile(filename):
    filepath = os.path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data


def common_data(list1, list2):
    result = False
  
    # traverse in the 1st list
    for x in list1:
  
        # traverse in the 2nd list
        for y in list2:
    
            # if one common
            if x == y:
                result = True
                return result 
                  
    return result

def flattenList(list):

    list = [r[0] for r in list]
    return list

def calcStatPerc(stat, list):
    avgStat = sum(list) / len(list)

    if stat > avgStat:
        statPerc = 100
    else:
        statPerc = (stat/avgStat)*100
    return statPerc

def num_sim(n1, n2):
  """ calculates a similarity score between 2 numbers """
  return 1 - abs(n1 - n2) / (n1 + n2)