import requests
import os, shutil
import csv
import time
import  json
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from requests_toolbelt.multipart.encoder import MultipartEncoder
# from requests_toolbelt.multipart.encoder import MultipartEncoder
def getGoogleOcr(persist_url):
	print ("getting ocr.....")
	url = "https://staging.signzy.xyz/ocr"

	payload = { "urls":[persist_url],  "toUseApi" : "googleDocumentOcr"}
	payload = json.dumps(payload)
	headers = {
	   'Content-Type': "application/json",
	   'cache-control': "no-cache",
	   'Postman-Token': "eab85026-a7f2-4e6b-bb75-e411805ac076"
	   }

	response = requests.request("POST", url, data=payload, headers=headers)
	# print(response.text)
	output = json.loads(response.text)

	# print ("##############################################")
	# print (output["ocrs"][0]["text"])
	return (output["ocrs"][0]["text"])

def store_in_persist(file_name, url=None, binary=False, image_data=None):
   """
   If binary is false, then the file_name must be a valid file path, else, if
   binary is true, then image_data must be in Binary form, to perform in-place file upload.

   :param file_name: name of file
   :param url: the endpoint were the images needs to stored(Optional)
   :param binary: bool (Optional)
   :param image_data: binary_image_data (Optional)
   :return:
   """
   if url is None:
	   url = "http://development.persist.signzy.tech/api/files/upload"

   if binary and image_data:
	   binary_data = image_data
   else:
	   binary_data = open(file_name, 'rb')

   multipart_data = MultipartEncoder(
	   fields={
		   # a file upload field
		   'file': (file_name, binary_data, 'image/jpeg')
	   }
   )

   response = requests.post(url, data=multipart_data,
							headers={'Content-Type': multipart_data.content_type})
   binary_data.close()

   output = json.loads(response.text)
   url = output['file']['directURL']
   url = url.replace("download", "download-bypass")

   return url

if __name__=='__main__':
	import argparse
	parser=argparse.ArgumentParser()
	
	parser.add_argument('-f','--folder', help='path to folder of samples', required=True)
	parser.add_argument('-o','--output', help='name of output csv file', required=False,default='ground_truth')
	args=parser.parse_args()
	outname=args.output
	input_folder=args.folder
	print('''Hi, in order to train the model for your data please select from the list below the data you want to train on\
you just have to pass the numeric index of each data you need as argument while running this script\nBelow is the list of data\n 1. Firstname\n 2. Lastname/Surname\n 3. Father/Guardian/Spouse Name\
\n 4. Number\n 5. Date of birth(DOB)\n 6. Date of issue(DOI)\n 7. Date of expiry(DOE)\n 8. Address\n''')
	input_string = input("Enter a list of indices for data you want to train on separated by space and press enter : ")
	cols=input_string.split(' ')
	dir_path = os.path.dirname(os.path.realpath(__file__))
	tstr=time.strftime("%Y_%m_%d_%H:%M:%S")
	output_csv_file=dir_path+'/tmp/'+ outname+'.csv'
	# k = len(os.path.listdir(input_folder))
	datalist=['index','firstname','lastname','fatherName','number','dob','doi','doe','address']
	index=0
	urls=[]
	gocr=[]
	name=[]
	fatherName=[]
	number=[]
	dob=[]
	doi=[]
	doe=[]
	address=[]
	k=0
	for i in os.listdir(input_folder):
		try:
			FrontImage=store_in_persist(os.path.join(input_folder,i))
			# FrontImage=df['url'][i]

			# ['FrontURL', 'BackURL', 'Unnamed: 2', 'UID', 'VID', 'name', 'dob ', 'yob', 'gender', 'address']
			print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			# print(i)

			gDoc = getGoogleOcr(FrontImage)
			# gText = getGoogletextOcr(FrontImage)

			urls.append(FrontImage)    
			gocr.append(gDoc) 
			# gtocr.append(gText)
			k+=1
			print(k)
		except Exception as e:
			print (e)

	final={'url':urls[:k],'ocr':gocr[:k]}
	for j in range(len(cols)):
		final[datalist[int(cols[j])]]=['']*k
	print(cols,final)
	ordered_cols=sorted(cols,key=lambda x :int(x))
	order=['url','ocr']
	ord1=[datalist[int(ordered_cols[l])] for l in range(len(ordered_cols))]

	order.extend(ord1)
	df1=pd.DataFrame(data=final)
	print(order)
	df1[order].to_csv(output_csv_file,sep=',',index=False)
  