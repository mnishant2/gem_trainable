import pandas as pd
import numpy as np
import os
import re

df = pd.read_csv(
    "/media/bubbles/fecf5b15-5a64-477b-8192-f8508a986ffe/ai/abs/flair-custom/customData/usDL/usDl3.csv",
    dtype=str)
df = df.replace(np.nan, '', regex=True)
start = 0
end = len(df) - 4500
google_doc = df["ocr"][start:end]
firstName = df["firstName"][start:end]
lastName = df["lastName"][start:end]
fatherName = df["fatherName"][start:end]
numbers = df["number"][start:end]
dob=df['dob'][start:end]
doi=df['doi'][start:end]
doe=df['doe'][start:end]
address=df['address'][start:end]
# print (google_doc[0])
# print (firstName[0])
pattern = re.compile(r"\s")
pattern1 = re.compile(r"[0-9\w\-/:\']")
# google_doc = google_doc[start:end]
# firstName = firstName[start:end]
# lastName = lastName[start:end]

# print (firstName)

fileName = "customData/usDL/train.txt"
if os.path.isfile(fileName):
    os.remove(fileName)

for index, ocr_text in enumerate(google_doc):
    print(index)
    index=index+start
    vocab = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\'-/ \t\n\r\x0b\x0c:"
    ocr_text = ''.join(filter(lambda x: x in vocab, ocr_text))
    # teststr="jbjdwwdji12456 ddds"
    # if start < index < end:
    str2 = re.sub(pattern1, '1', ocr_text)
    # print(re.sub(pattern1, '1', teststr))
    str2 = re.sub(pattern, '0', str2)
    list1 = list(str2)
    list2 = [0] * len(list(ocr_text))
    if ocr_text.find(firstName[index])>=0:
        list2[ocr_text.find(firstName[index]):ocr_text.find(firstName[index]) + len(firstName[index])] = [1] * len(firstName[index])
    if ocr_text.find(fatherName[index])>=0:
        list2[ocr_text.find(fatherName[index]):ocr_text.find(fatherName[index]) + len(fatherName[index])] = [1] * len(fatherName[index])
    if ocr_text.find(lastName[index]) >= 0:
        list2[ocr_text.find(lastName[index]):ocr_text.find(lastName[index]) + len(lastName[index])] = [1] * len(lastName[index])
    # print(ocr_text.find(numbers[index]),len(numbers[index]))
    if ocr_text.find(numbers[index])>=0:
        list2[ocr_text.find(numbers[index]):ocr_text.find(numbers[index]) + len(numbers[index])] = [1] * len(numbers[index])
    if ocr_text.find(dob[index])>=0:
        list2[ocr_text.find(dob[index]):ocr_text.find(dob[index]) + len(dob[index])] = [1] * len(dob[index])
    if ocr_text.find(doi[index])>=0:
        list2[ocr_text.find(doi[index]):ocr_text.find(doi[index]) + len(doi[index])] = [1] * len(doi[index])
    if ocr_text.find(doe[index])>=0:
        list2[ocr_text.find(doe[index]):ocr_text.find(doe[index]) + len(doe[index])] = [1] * len(doe[index])

    query_string = address[index].strip()
    query_string = ''.join(filter(lambda x: x in vocab, query_string))
    query_string = query_string.replace("\n","").replace(" ","[\\n\s]")
    print (address[index].rstrip())
    print (query_string)
    print (ocr_text)
    addregex = re.search(query_string, ocr_text)
    if addregex:
        # print ("&&&&&&&&&&&&")
        list2[addregex.start():addregex.end()] = [1] * len(addregex.group())
    newlist = []
    for a, b in zip(list1, list2):
        x = (int(a) * int(b)) + int(a)
        newlist.append(str(x))
    newlist = ''.join(newlist)
    newlist = newlist.split('0')
    final_list = [int(x) % 10 for x in newlist if x]
    texts = ocr_text.split()
    # print(len(final_list),len(texts))
    for idx, text in enumerate(texts[:len(final_list)]):
        label = "O"
        # print (text)
        thisFirstName = firstName[index].split()
        thisLastName = lastName[index].split()
        thisFatherName = fatherName[index].split()
        thisnumber = numbers[index].split()
        thisdob= dob[index]
        thisdoi= doi[index]
        thisdoe= doe[index]
        thisaddress= address[index].split()
        # print (thisaddress)
        # print("------------------------------")
        # print(thisnumber)
        if (text in thisFirstName) and (final_list[idx] == 2):
            print("------------------------------")
            print(text.lower(), thisFirstName)
            label = "B-PER"
        elif (text in thisLastName) and (final_list[idx] == 2):
            print("------------------------------")
            print(text.lower(), thisLastName)
            label = "I-PER"
        elif (text in thisFatherName) and (final_list[idx] == 2):
            print("###################")
            print(text.lower(), thisFatherName)
            label = "B-PER"
        elif (text in thisnumber) and (final_list[idx] == 2):
            # print("#################")
            # print(text,thisnumber,final_list[idx])
            label = "B-NUM"
        elif (text ==thisdob) and (final_list[idx] == 2):
            print(thisdob)
            label="B-DOB"
        elif (text ==thisdoi)and (final_list[idx] == 2):
            print(thisdoi)
            label="B-DOI"
        elif (text ==thisdoe) and (final_list[idx] == 2):
            label="B-DOE"
            print(thisdoe)
        elif (text in thisaddress) and  (final_list[idx] == 2):
            label="B-ADD"
            print ("******")
            print(text)
        file1 = open(fileName, "a")
        file1.write(text + " " + label + "\n")
        file1.close()

    file1 = open(fileName, "a")
    file1.write(" \n")
    file1.close()
