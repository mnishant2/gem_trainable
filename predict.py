import os,sys,json
from flair.data import Sentence
import time
import flair
from date_sanity import checkfirst,check_all
from datetime import datetime
from dateutil.parser import parse


def predict(model, fields,docOCR, textOCR=None):
    output={}
    if textOCR:
        text_sent = Sentence(textOCR, use_tokenizer=True)
        # time_to_predict=time.time()
        model.predict(text_sent)
        textout = find_vals(text_sent, fields)
        doc_sent = Sentence(docOCR, use_tokenizer=True)
        model.predict(doc_sent)
        docout = find_vals(doc_sent, fields)
        for k in docout.keys():
            # if len(textout[k])>len(docout[k]):
            #     output[k]=textout[k]
            # else:
            output[k]=docout[k]
    else:
        doc_sent = Sentence(docOCR, use_tokenizer=True)
        model.predict(doc_sent)
        docout = find_vals(doc_sent,fields)
        output=docout
        # print(output)
    return output
    
def find_vals(sent,fields):
    # start_time=
    out1={}
    out={}
    # print(fields)
    # print("bfusfusu")
    for fname in fields:
        out1[fname]=[]
    for word in sent.tokens:
        # print(word.tags["ner"].value)
        
        if word.tags["ner"].value=="B-PER":
            # print(word)
            out1['firstName'].append(word.text)
        elif word.tags["ner"].value=="I-PER":
            out1['lastName'].append(word.text)
        elif word.tags["ner"].value == "B-NUM":
            # print("###################")
            out1['number'].append(word.text)
        elif word.tags["ner"].value == "B-DOB":
            out1['dob'].append(word.text)
        elif word.tags["ner"].value == "B-DOI":
            out1['issueDate'].append(word.text)
        elif word.tags["ner"].value == "B-DOE":
            out1['expiryDate'].append(word.text)
        elif word.tags["ner"].value == "B-ADD":
            out1['address'].append(word.text)

    print (out1)
    out1=checkfirst(out1)
    try:
        if (len(out1['dob'])) and (len(out1['issueDate'])) and (len(out1['expiryDate'])) and (not (out1['dob'][0],out1['issueDate'][0],out1['expiryDate'][0]==sorted([out1['dob'][0],out1['issueDate'][0],out1['expiryDate'][0]], key=lambda x: datetime.strptime(x, '%d/%m/%Y')))):
            out1['dob'],out1['issueDate'],out1['expiryDate']=check_all(out1['dob'],out1['issueDate'],out1['expiryDate'])
    except Exception as e:
        out1['dob'],out1['issueDate'],out1['expiryDate']=check_all(out1['dob'],out1['issueDate'],out1['expiryDate'])

    for fname in fields:
        out[fname]=' '.join(out1[fname])
    # print(out)
    return out