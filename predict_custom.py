from flair.data import Sentence
from flair.models import SequenceTagger
import pandas as pd
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, CharacterEmbeddings, FlairEmbeddings, CharLMEmbeddings,ELMoEmbeddings, BertEmbeddings
from pathlib import Path



df=pd.read_csv("/media/bubbles/fecf5b15-5a64-477b-8192-f8508a986ffe/ai/abs/flair-custom/customData/usDL/usDl2.csv",dtype='str')
vocab = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\'-/\t \n\r\x0b\x0c:"

ocr_text = ''.join(filter(lambda x: x in vocab, df['ocr'][295]))

# ocr_text = ''.join(filter(lambda x: x in vocab, df['ocr'][4]))
ocr_text = """HAWAI DRIVER LICENSE
USA
jacovella LFLARLA
01
07
44gm -153459821
3DOB 01/01/1979 4bExp 01/01/2007 
15Hgt 16Wgt 18Hair 17Eye 13 Sex cty
5-04 110 BRN BRN F O
4aIss
9 Class 12 Restr
01/01/2001
heleni A Sample 9a End
1 jacovella CAPPELLO
CDL
8123 ANY STREET
AHCD
ORGAN
ANYTOWN HI 00000
DONOR"""

# ocr_text = ''.join(filter(lambda x: x in vocab, ocr_text))
# print(ocr_text)
sent: Sentence =Sentence(ocr_text,use_tokenizer=True)
tag_type = 'ner'

# 3. make the tag dictionary from the corpus
# tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
# print(tag_dictionary.idx2item)
# cachedir=Path('/media/bubbles/fecf5b15-5a64-477b-8192-f8508a986ffe/ai/nishant/embeddings')
# # 4. initialize embeddings
# embedding_types: List[TokenEmbeddings] = [

#     # WordEmbeddings('glove'),

#     # comment in this line to use character embeddings
#     # CharacterEmbeddings(),

#     # comment in these lines to use flair embeddings
#     FlairEmbeddings('news-forward-fast',use_cache= True,cache_directory=cachedir),
#     # CharLMEmbeddings('news-forward',use_cache=True),
#     # ELMoEmbeddings('elmo-small'),
#     # BertEmbeddings(),
#     FlairEmbeddings('news-backward-fast',use_cache=True,cache_directory=cachedir),
# ]

# embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# # 5. initialize sequence tagger
# from flair.models import SequenceTagger

# tagger: SequenceTagger = SequenceTagger(hidden_size=256,
#                                         embeddings=embeddings,
#                                         tag_dictionary=tag_dictionary,
#                                         rnn_layers= 2,
#                                         tag_type=tag_type,
#                                         use_crf=True)


# 5. initialize sequence tagger
from flair.models import SequenceTagger

# SequenceTagger = SequenceTagger()
# state=SequenceTagger._load_state('/media/bubbles/fecf5b15-5a64-477b-8192-f8508a986ffe/ai/abs/flair-custom/resources/taggers/new-ner/checkpoint.pt')
# print(state['tag_dictionary'].idx2item)
import time

start = time.time()
model=SequenceTagger.load_from_file(model_file=Path('/media/bubbles/fecf5b15-5a64-477b-8192-f8508a986ffe/ai/abs/flair-custom/resources/taggers/usDL2/best-model.pt'))
print (time.time() - start)
# if 'B-DOE' in model.tag_dictionary.idx2item):

start = time.time()
model.predict(sent)
out=sent.to_dict('ner')
print(sent.to_tokenized_string())
print(out['entities'][0])
for word in sent.tokens:
    print(type(word.tags["ner"].value))
    print(word.text)
# for span in sent.get_spans('ner'):
#     idx=[token for token in span.tokens]
#     print(idx)
print (time.time() - start)
print(sent.to_tagged_string())
# for tokens in sent.to_tagged_string():
#     print(tokens)