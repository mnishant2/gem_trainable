import numpy as np
from keras.utils import to_categorical
import torch.backends.cudnn as cudnn
import torch.backends.cudnn.rnn
import torch.nn as nn
torch.backends.cudnn.enabled = True
from torch.autograd import Variable
import torch.nn.functional as F
import pandas as pd
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('-i','--input', help='path to input csv', required=False,default='new_ground_truth')
parser.add_argument('-m','--model', help='path of base model', required=False,default='base_model')
parser.add_argument('-o','--output', help='output model name', required=False,default='new_model')
parser.add_argument('-e','--epoch', help='number of epochs', required=False,default='60')
args=parser.parse_args()
input_csv_file='./tmp/'+args.input+'.csv'
outname=args.output
# input_folder=
use_gpu=torch.cuda.is_available()
dft=pd.read_csv(input_csv_file)

n_batches=1

df_train=dft[:100]
df_test=dft[100:]
df_test=df_test.reset_index()
print(len(df_train))
num_epochs=int(args.epoch)

vocab='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\'-/ \t\n\r\x0b\x0c:'
char2idx = {w: i + 1 for i, w in enumerate(vocab)}
char2idx['PAD']=0

tags=[0,1,2,3]
tag2idx={w:i for i,w in enumerate(tags)}
tag2idx['PAD']=-1

def generate_batches(df,n_batches=1,seq_length=20):
	# df=df.fillna(0)
	df=df.replace(0.0,None)
	# global name2
	fieldnames=df.columns.tolist()
	# print(df['fatherName'][0])
	for i in range(0,len(df),n_batches):
		ln=[]
		end=i+n_batches

		snt=[df['ocr'][i]]
		snt1=[]
		for k in snt:
			snt1.append(''.join(filter(lambda x: x in vocab , k)))
		snt=snt1
		seq_length=len(snt[0])
		if 'number' in fieldnames:
			dln=[df['number'][i]]
		if 'dob' in fieldnames:
			dt1=[df['dob'][i]]
		if 'doi' in fieldnames:
			dt2=[df['doi'][i]]
		if 'doe' in fieldnames:
			dt3=[df['doe'][i]]
		if 'name' in fieldnames:
			name1=[df['name'][i]]
#         name2=list((df['fatherName'][i:end]))
		if 'fatherName' in fieldnames:
			# print(df["fatherName"][i])
			name2=[df['fatherName'][i]]
			# print(name2)
		# tmpList=list(zip(snt,dl,dt1,name1))
		# tmpList=sorted(tmpList,key=lambda x: len(x[0]),reverse=True)
		# snt,dln,dat1,nm1=zip(*tmpList)
		arr=np.zeros((n_batches,seq_length))
		l_arr=np.ones((n_batches,seq_length))*-1
		for ind,s in enumerate(snt):
			st=s
			# print(ind,dt1)
			label=[0]*len(list(st))

			if dln[ind]:
				dl=str(dln[ind])

				if st.find(dl)>=0:
					label[st.find(dl):st.find(dl)+len(dl)]=[1]*len(dl)
			if dt1[ind]:
				dt1=dt1[ind]

				if st.find(dt1)>=0:
					label[st.find(dt1):st.find(dt1)+len(dt1)]=[2]*len(dt1)
			if dt2[ind]:
				dt2=dt2[ind]
#                 print('********',dl,st.find(dl),st)
				if st.find(dt2)>=0:
					label[st.find(dt2):st.find(dt2)+len(dt2)]=[2]*len(dt2)
			if dt3[ind]:
				dt3=dt3[ind]
#                 print('********',dl,st.find(dl),st)
				if st.find(dt3)>=0:
					label[st.find(dt3):st.find(dt3)+len(dt3)]=[2]*len(dt3)

			if name1[ind]:
				nme1=name1[ind]

				if st.find(nme1)>=0:
					label[st.find(nme1):st.find(nme1)+len(nme1)]=[3]*len(nme1)
			if name2[ind]:
				nme2=name2[ind]
#                 print('********',dl,st.find(dl),st)
				if st.find(nme2)>=0:
					label[st.find(nme2):st.find(nme2)+len(nme2)]=[3]*len(nme2)

			sent=[char2idx[w] for w in st]
			tag=[tag2idx[w] for w in label]

			ln.append(len(sent))
			arr[ind%n_batches][:len(sent)]=sent
			l_arr[ind%n_batches][:len(sent)]=tag


		x=torch.tensor(arr)
		y=torch.LongTensor(l_arr)

		yield x,y,ln

class dlLSTM(nn.Module):
	def __init__(self, nb_layers,vocab,labels,nb_lstm_units=100, batch_size=1):
		super(dlLSTM, self).__init__()
		self.vocab = vocab
		self.tags = labels

		self.nb_layers = nb_layers
		self.nb_lstm_units = nb_lstm_units
#         self.embedding_dim = embedding_dim
		self.batch_size = batch_size

		# don't count the padding tag for the classifier output
		self.nb_tags = len(self.tags) - 1


		self.lstm = nn.LSTM(

			input_size=len(self.vocab),
			hidden_size=self.nb_lstm_units,
			num_layers=self.nb_layers,
			batch_first=True,
			bidirectional=True

		)

		# output layer which projects back to tag space
		self.fc = nn.Linear(self.nb_lstm_units*2, self.nb_tags)




	def init_hidden(self):
		# the weights are of the form (nb_layers, batch_size, nb_lstm_units)
		hidden_a = Variable(torch.randn(self.nb_layers*2, self.batch_size, self.nb_lstm_units))
		hidden_b = Variable(torch.randn(self.nb_layers*2, self.batch_size, self.nb_lstm_units))


		if use_gpu:
			hidden_a = hidden_a.cuda()
			hidden_b = hidden_b.cuda()

		return (hidden_a, hidden_b)

	def forward(self, X, X_lengths):
 
		self.hidden = self.init_hidden()

		batch_size, seq_len = X.size()


		X=torch.tensor(to_categorical(X,num_classes=len(self.vocab)))
		X=Variable(X)
		X=torch.nn.utils.rnn.pack_padded_sequence(X,batch_first=True, lengths=X_lengths)
		if use_gpu:
			X=X.cuda()

		X, self.hidden = self.lstm(X, self.hidden)

 
		X, _ = torch.nn.utils.rnn.pad_packed_sequence(X, batch_first=True)

		X = X.contiguous()
		X = X.view(-1, X.shape[2])


		X = self.fc(X)


		X = F.log_softmax(X, dim=1)

		Y_hat = X
		return Y_hat

	def loss(self, Y_hat, Y):

		Y = Y.view(-1)

 
		tag_pad_token = self.tags['PAD']
		mask = (Y > tag_pad_token).float()


		nb_tokens = int(torch.sum(mask).item())


		Y_hat = Y_hat[range(Y_hat.shape[0]), Y] * mask


		ce_loss = -torch.sum(Y_hat) / nb_tokens

		return ce_loss

net = dlLSTM(nb_layers=4,vocab=char2idx,labels=tag2idx)
net.load_state_dict(torch.load('./models/'+args.model+'.pth'))
# print(time.time()-t1)
# print(net.loss())
if use_gpu:
	net=net.cuda()
# define the loss and the optimizer
optimizer = torch.optim.Adam(net.parameters(), lr=0.001)

val_losses=list()
best_loss=0.5
for epoch in range(num_epochs):
	# is_train=True
	for i,(x,y,ln) in enumerate(generate_batches(df_train)):
#         print(ln)
		if use_gpu:
#             x=x.cuda()
			y=y.cuda()



#             ln=ln.cuda()
		optimizer.zero_grad()
		output=net(x,ln)
		loss=net.loss(output,y)
		loss.backward()
		optimizer.step()
		if i%5==0 and i!=0:
			is_train=False
			for val_x,val_y,val_ln in generate_batches(df_test):
				print('hgsdudu')
				with torch.no_grad():
					if use_gpu:
	#                     val_x=val_x.cuda()
						val_y=val_y.cuda()
	#                     val_ln=val_ln.cuda()
	#                 print(val_x.size())

					val_out=net(val_x,val_ln)
					val_loss=net.loss(val_out,val_y)
					print(val_loss)
					val_losses.append(val_loss.item())
			if val_loss<best_loss:
				print('the model improved')
				filename='./models/'+outname+str(epoch)+'_weights.pth'
				torch.save(net.state_dict(),filename)
				best_loss=val_loss
			else:
				print('model did not improve')
			print("Epoch: {}, Batch: {}, Train Loss: {:.6f}, Validation Loss: {:.6f}".format(epoch, i, loss.item(), val_loss.item()))
	#     print(x.size)copy