import os,sys
import json,csv
import pandas as pd
import numpy as np
import random
from xeger import Xeger
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('-i','--input', help='path to input csv', required=False,default='ground_truth')
parser.add_argument('-o','--output', help='name of output csv file', required=False,default='new_ground_truth')

args=parser.parse_args()
outname=args.output
inp=args.input
dir_path = os.path.dirname(os.path.realpath(__file__))
input_csv_file=inp+'.csv'
output_csv_file= outname+'.csv'
pd.options.mode.chained_assignment = None
with open('./numlist.txt','r') as f:
    numlist=json.load(f)
with open('./noise.txt','r') as f:
    noise=json.load(f)
name_list = []
random_name_list =[]
indian_names =open('./indian_names.csv', 'r')
for index, something in enumerate(indian_names):
    if '@' in something or '/' in something:
        continue
    else:
        name_list.append(something.split(',')[0])

file1 = open('./first_names.txt')
file2 = open('./last_names.txt')
list_name=list(file1)
list_surname=list(file2)
# print(list(file1))
for first_name , last_name in zip(list_name, list_surname):
    first_name = first_name.replace(' ','')
    first_name = first_name.strip('\n')
    last_name = last_name.replace(' ','')
    last_name = last_name.strip('\n')
    name = first_name+' '+last_name
    random_name_list.append(name)
# print(len(random_name_list))
import random
for name in range(100000- len(name_list)):
    name_list.append(random.choice(random_name_list))

# print(len(name_list))
import math
file = pd.read_csv(input_csv_file)
fieldnames=file.columns.tolist()
# print(fieldnames)
# file=file[:150]
fieldname_retained=[i for i in fieldnames if i not in ['firstName','ocr','lastName','fatherName']]

def combine_first_two_names(name):
    temp = name.split()
    return temp[0]+temp[1]+' '+temp[2]
def generate_number():
    regex="([a-z]{1,3}[- ]{0,4}\d{8,13})|([a-z]{1,3}\d{0,3}[- ]{1,4}\d{8,13})|([a-z]{2,3}[- ]{0,4}[\d/]{8,15}$)|([a-z]{2,3}[- ]{0,4}[\d/]{8,15}$)|([a-z]{2,3}[- ]{0,4}[\d/]{8,15})|([a-z]{1,2}\d{,2}[- ]{,2}[\d/]{8,12})|([a-z]{1,2}[- ]{1,3}[\d ]{9,15})|([a-z]{1,2}[\d /]{12,18})|(\d{8,15}$)"
    x = Xeger(limit=20)
    randnum=x.xeger(regex)
    return randnum
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start
def name_augment(df):

    df=df.fillna('')
    
    num=100
    ind=range(num*len(df['ocr']))
    df_copy=pd.DataFrame(columns=fieldnames,index=ind)
    for i in range(len(df['ocr'])):
        print(i)
        # print(i)
        # opt=np.random.choice(options, p=probdist)
        if df['ocr'][i]:
            df_copy['ocr'][num*i]=df['ocr'][i]
            df_copy['firstName'][num*i]=df['firstName'][i]
            df_copy['fatherName'][num * i] = df['fatherName'][i]
            # print('***************',df_copy['fatherName'][num * i])
            df_copy['lastName'][num * i] = df['lastName'][i]
            # df_copy['fatherlastName'][num * i] = df['fatherlastName'][i]
            for fields in fieldname_retained:
                df_copy[fields][num*i]=df[fields][i]
            for j in range(1,num):
                # print('#######',df['fatherName'][i])
                # print(j)
                if 'firstName' in fieldnames:
                    # print(num*i+j)
                    if df['firstName'][i] and not df['lastName'][i]:
                        # print('bjej')
                        new_name=random.choice(name_list)
                        name_list2=name_list
                        # print(len(name_list2))

                        # print(new_name)
                        df_copy['ocr'][num * i + j] = df['ocr'][i]
                        if df['fatherName'][i]:
                            if np.random.randint(2):
                                # print('yoyo')
                                name_list2.remove(new_name)
                                new_fathername = random.choice(name_list2)
                                # print(new_fathername)
                                # print(df['ocr'][i])
                                df_copy['ocr'][num * i + j] = df['ocr'][i].replace(df['fatherName'][i], new_fathername)
                                df_copy['fatherName'][num * i + j] = new_fathername
                                # print(df_copy['ocr'][num * i + j])
                            else:
                                df_copy['fatherName'][num * i + j] = df['fatherName'][i]
                                df_copy['ocr'][num * i + j] = df['ocr'][i]
                        df_copy['ocr'][num*i+j]=df_copy['ocr'][num * i + j].replace(df['firstName'][i],new_name)
                        df_copy['firstName'][num*i+j]=new_name
                        for fields in fieldname_retained:
                            df_copy[fields][num*i+j]=df[fields][i]

                    elif df['firstName'][i] and df['lastName'][i]:
                        # print(len(list(file1)))
                        new_firstName = random.choice(list_name).strip('\n')
                        new_lastName = random.choice(list_surname).strip('\n')
                        new_fathername=random.choice(name_list)
                        df_copy['ocr'][num * i + j] = df['ocr'][i]
                        # print(new_name)
                        if df['fatherName'][i]:
                            if np.random.randint(2):
                                # print('yoyoyo')
                                df_copy['ocr'][num * i + j] = df['ocr'][i].replace(df['fatherName'][i], new_fathername)
                                df_copy['fatherName'][num * i + j] = new_fathername
                            else:
                                df_copy['fatherName'][num * i + j] = df['fatherName'][i]
                                df_copy['ocr'][num * i + j] = df['ocr'][i]
                        df_copy['ocr'][num*i+j]=df_copy['ocr'][num * i + j].replace(df['firstName'][i],new_firstName)
                        df_copy['firstName'][num*i+j]=new_firstName
                        df_copy['ocr'][num * i + j] = df_copy['ocr'][num * i + j].replace(df['lastName'][i], new_lastName)
                        df_copy['lastName'][num * i + j] = new_lastName
                        for fields in fieldname_retained:
                            df_copy[fields][num*i+j]=df[fields][i]

                    elif (df['fatherName'][i]) and not (df['firstName'][i] or df['lastName'][i]):
                        new_fathername = random.choice(name_list)
                        df_copy['ocr'][num * i + j] = df['ocr'][i]
                        df_copy['firstName'][num * i + j] = df['firstName'][i]
                        df_copy['lastName'][num * i + j] = df['lastName'][i]
                        if np.random.randint(2):
                            # print('yoyoyo')
                            df_copy['ocr'][num * i + j] = df['ocr'][i].replace(df['fatherName'][i], new_fathername)
                            df_copy['fatherName'][num * i + j] = new_fathername
                        else:
                            df_copy['fatherName'][num * i + j] = df['fatherName'][i]
                        for fields in fieldname_retained:
                            df_copy[fields][num*i+j]=df[fields][i]

                    elif (df['number'][i]) and not(df['firstName'][i] or df['lastName'][i] or df['fatherName'][i]):
                        df_copy['ocr'][num * i + j] = df['ocr'][i]
                        df_copy['firstName'][num * i + j] = df['firstName'][i]
                        df_copy['lastName'][num * i + j] = df['lastName'][i]
                        df_copy['fatherName'][num * i + j] = df['fatherName'][i]
                        for fields in fieldname_retained:
                            df_copy[fields][num*i+j]=df[fields][i]
                        break
                    else:
                        print("nncbnns")
                        continue
                # print(df_copy['fatherName'][num * i + j])
        # print(df['fatherName'][i],df_copy['fatherName'][num * i])
    return df_copy

    # print('################')

    # num=20
    # print(len(df['ocr']))
def swapcase(df):
    df = df.fillna('')
    df_copy = df.copy()
    for i in range(len(df['ocr'])):
        # print('##############################################\n###############################################')
        # print(i)
        # opt=np.random.choice(options, p=probdist)
        if df['ocr'][i]:
            if random.random()<0.6:
                if (df['fatherName'][i]) or (df['firstName'][i]):
                    a=np.random.randint(2)
                    if a:
                        # print(a)
                        if 'firstName' in fieldnames:
                            if df['firstName'][i]:
                                # print(df_copy['firstName'][i])
                                # print(df_copy['ocr'][i])
                                df_copy['ocr'][i]=df['ocr'][i].replace(df['firstName'][i],df['firstName'][i].swapcase())
                                df_copy['firstName'][i]=df['firstName'][i].swapcase()
                                # print(df_copy['ocr'][i])
                                # print(df_copy['firstName'][i])
                                # if not df.isnull()['fatherName'][i]:
                        if 'fatherName' in fieldnames:
                            if df['fatherName'][i]:
                                df_copy['ocr'][i]=df_copy['ocr'][i].replace(df['fatherName'][i],df['fatherName'][i].swapcase())
                                df_copy['fatherName'][i]=df['fatherName'][i].swapcase()
                    else:
                        if 'firstName' in fieldnames:
                            if df['firstName'][i]:
                                # print(df_copy['firstName'][i])
                                # print(df_copy['ocr'][i])
                                df_copy['ocr'][i]=df['ocr'][i].replace(df['firstName'][i],df['firstName'][i].title())
                                df_copy['firstName'][i]=df['firstName'][i].title()
                                # print(df_copy['ocr'][i])
                                # print(df_copy['firstName'][i])
                #                 if not df.isnull()['fatherName'][i]:
                        if 'fatherName' in fieldnames:
                            if df['fatherName'][i]:
                                df_copy['ocr'][i]=df_copy['ocr'][i].replace(df['fatherName'][i],df['fatherName'][i].title())
                                df_copy['fatherName'][i]=df['fatherName'][i].title()
    return df_copy
def swapnames(df):
    df = df.fillna('')
    df_copy = df.copy()
    for i in range(len(df['ocr'])):
        if random.random()<0.45:
            # print('')
            if 'firstName' in fieldnames and 'fatherName' in fieldnames:
                if (df['fatherName'][i]) and (df['firstName'][i]):
                    a=np.random.randint(3)
                    if a==0:

                        # print(df_copy['ocr'][i])
                        # print(df_copy['firstName'][i],df_copy['fatherName'][i])
                        df_copy['ocr'][i]=df['ocr'][i].replace(df['firstName'][i],df['fatherName'][i].swapcase())
                        df_copy['ocr'][i]=df_copy['ocr'][i].replace(df['fatherName'][i],df['firstName'][i].swapcase())
                        # print(df_copy['ocr'][i])

                        df_copy['firstName'][i]=df['fatherName'][i].swapcase()
                        df_copy['fatherName'][i]=df['firstName'][i].swapcase()
                        # print(df_copy['firstName'][i], df_copy['fatherName'][i])
                    elif a==1:
                        if (df_copy['firstName'][i]==df_copy['firstName'][i].title()) or (df_copy['fatherName'][i]==df_copy['fatherName'][i].title()):
                            df_copy['ocr'][i] = df['ocr'][i].replace(df['firstName'][i], df['fatherName'][i].swapcase())
                            df_copy['ocr'][i] = df_copy['ocr'][i].replace(df['fatherName'][i],df['firstName'][i].swapcase())
                            df_copy['firstName'][i] = df['fatherName'][i].swapcase()
                            df_copy['fatherName'][i] = df['firstName'][i].swapcase()
                        else:
                            df_copy['ocr'][i]=df['ocr'][i].replace(df['firstName'][i],df['fatherName'][i].title())
                            df_copy['ocr'][i] = df_copy['ocr'][i].replace(df['fatherName'][i],df['firstName'][i].title())
                            df_copy['firstName'][i]=df['fatherName'][i].title()
                            df_copy['fatherName'][i]=df['firstName'][i].title()
                    else:
                        # print('dhinkachika')
                        if (df_copy['ocr'][i].find(df_copy['firstName'][i])>=0) and (df_copy['ocr'][i].find(df_copy['fatherName'][i])>=0):
                            # print(df_copy['ocr'][i])
                            # print(df_copy['firstName'][i], df_copy['fatherName'][i])
                            if df_copy['ocr'][i].find(df_copy['firstName'][i])<df_copy['ocr'][i].find(df_copy['fatherName'][i]):
                                df_copy['ocr'][i] = df['ocr'][i].replace(df['firstName'][i], df['fatherName'][i])
                                father_pos=find_nth(df_copy['ocr'][i],df['fatherName'][i],2)
                                df_copy['ocr'][i]=df_copy['ocr'][i][:father_pos]+df['firstName'][i]+df_copy['ocr'][i][father_pos+len(df['fatherName'][i]):]
                                df_copy['firstName'][i] = df['fatherName'][i]
                                df_copy['fatherName'][i] = df['firstName'][i]
                                # print('**************',df_copy['ocr'][i])
                                # print(df_copy['firstName'][i], df_copy['fatherName'][i])
                            else:
                                df_copy['ocr'][i] = df['ocr'][i].replace(df['fatherName'][i], df['firstName'][i])
                                first_pos = find_nth(df_copy['ocr'][i], df['firstName'][i], 2)
                                df_copy['ocr'][i] = df_copy['ocr'][i][:first_pos] + df['fatherName'][i] + \
                                                    df_copy['ocr'][i][first_pos+len(df['firstName'][i]):]
                                df_copy['firstName'][i] = df['fatherName'][i]
                                df_copy['fatherName'][i] = df['firstName'][i]
                                # print('############',df_copy['ocr'][i])
                                # print(df_copy['firstName'][i], df_copy['fatherName'][i])
                        else:
                            continue

    return df_copy
def numchange(df):
    df = df.fillna('')
    df_copy = df.copy()
    for i in range(len(df['ocr'])):
        if random.random()<0.5:
            if 'number' in fieldnames:
                if df['number'][i]:
                    if random.random()<0.25:
                        newnum=generate_number()
                        df_copy['ocr'][i]=df['ocr'][i].replace(df['number'][i],newnum)
                        df_copy['number'][i]=newnum
                    else:
                        newnum=random.choice(numlist)
                        df_copy['ocr'][i]=df['ocr'][i].replace(df['number'][i],newnum)
                        df_copy['number'][i]=newnum
    return df_copy
def addnoise(df):
    df = df.fillna('')
    df_copy = df.copy()
    for i in range(len(df['ocr'])):
            # if random.random()<0.5:
        ocr_sent=df_copy['ocr'][i].split('\n')

        no_sent=len(ocr_sent)
        # print(no_sent)
        if np.random.randint(2):
            try:
                degreeOfNoise=np.random.randint(no_sent//2)
                for k in range(degreeOfNoise):
                    noisySentence=random.choice(noise)
                    placeToInsert=np.random.randint(no_sent+1)
                    ocr_sent.insert(placeToInsert,noisySentence)
                    placeToRemove = np.random.randint(no_sent+1)
                    if not any([x in ocr_sent[placeToRemove] for x in [df_copy['firstName'][i],df_copy['lastName'][i],df_copy['fatherName'][i],df_copy['number'][i],df_copy['dob'][i],df_copy['doi'][i],df_copy['doe'][i]]]):
                        ocr_sent.remove(ocr_sent[placeToRemove])
            except Exception as e:
                print(e)
                pass
        df_copy['ocr'][i]='\n'.join(ocr_sent)
    return df_copy

def randomise(df):
    df_new=swapcase(df)
    df_new=swapnames(df_new)
    df_new=numchange(df_new)
    df_new=addnoise(df_new)
    df_new = df_new.sample(frac=1).reset_index(drop=True)
    return df_new

# print(csvfile)
# inter_csv_file='/home/nishant/pandocinter.csv'
df=pd.read_csv(input_csv_file,dtype=str)
df_cp=name_augment(df)
# df_cp.dropna(inplace=True)
order=fieldnames
# df_cp[order].to_csv(inter_csv_file,sep=',',index=False)
df_new=randomise(df_cp)
# output_csv_file='./tmp/new_ground_truth.csv'
order=fieldnames
df_new[order].to_csv(output_csv_file,sep=',',index=False)

