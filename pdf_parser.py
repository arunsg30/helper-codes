import os

from invoice2data import extract_data
import PyPDF2
import pdftotext
import re

import pandas as pd

import spacy
from spacy import displacy
import en_core_web_lg
nlp = en_core_web_lg.load()


# 769 school list
school = pd.read_excel("./school list.xlsx")
school_list = school['name'].values.tolist()
school_list = list(set(school_list)) #removing duplicates

def find_word(txt,keyword):
    keyword = keyword.lower()
    res = []
    for i in txt:
        if keyword in i.lower():
            res.append(i)
    res = [re.sub(' +'," ",i).strip() for i in res]
    res = [i for i in res if len(i)<50]
    return list(set(res))


# extracting entites 
def extract_entites(toi)
	text_result = {}
	names,ID = [], []
	student = find_word(toi,"Student ID") + find_word(toi,"Student name")
	schools = (find_word(toi,"university")+find_word(toi,"institute")+find_word(toi,"Technology"))
	fee = find_word(toi,"fee") + find_word(toi,"amount") 
	text_result["Fee"] =  fee
	for school in school_list:
	    if school in schools:
	        text_result["School Name"] = school
	        break
	for st in student:
	    doc = nlp(st)
	    name_list = ([(X.text, X.label_) for X in doc.ents if X.label_ == "PERSON" ])
	    id_list = ([(X.text, X.label_) for X in doc.ents if X.label_ == "CARDINAL" ])
	    if name_list != [] and name_list[0][0] not in names:
	        names.append(name_list[0][0])
	    if id_list != [] and id_list[0][0] not in ID:
	        ID.append(id_list[0][0])
	text_result["Student Name"] = names
	text_result["Student ID"] = ID
	return text_result





if __name__ == '__main__':

    if len(sys.argv) > 1:
        filePath = sys.argv[1]

	with open(filePath, "rb") as f:
  	  pdf = pdftotext.PDF(f)
	toi = "\n".join(pdf) # merging all pages 
	toi = toi.split("\n")
	print(extract_entites(toi))



