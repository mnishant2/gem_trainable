from flair.data import TaggedCorpus
from flair.data_fetcher import NLPTaskDataFetcher
from flair.data_fetcher import NLPTaskDataFetcher, NLPTask
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, CharacterEmbeddings, FlairEmbeddings, CharLMEmbeddings,ELMoEmbeddings, BertEmbeddings
from pathlib import Path


from typing import List

# 1. get the corpus
# define columns
columns = {0: 'text', 1:'ner'}

# this is the folder in which train, test and dev files reside
data_folder = './'

#retrieve corpus using column format, data folder and the names of the train, dev and test files
corpus: TaggedCorpus = NLPTaskDataFetcher.load_column_corpus(data_folder, columns,
                                                              train_file='customData/usDL/train.txt',
                                                              test_file='customData/usDL/test.txt',
                                                              dev_file='customData/usDL/test.txt')

# len(corpus.train)
print(corpus.train[0].to_tagged_string('ner'))


# 2. what tag do we want to predict?
tag_type = 'ner'

# 3. make the tag dictionary from the corpus
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
print(tag_dictionary.idx2item)
cachedir=Path('/media/bubbles/fecf5b15-5a64-477b-8192-f8508a986ffe/ai/nishant/embeddings')
# # 4. initialize embeddings
embedding_types: List[TokenEmbeddings] = [

    # WordEmbeddings('glove'),

    # comment in this line to use character embeddings
    CharacterEmbeddings(path_to_char_dict="/media/bubbles/fecf5b15-5a64-477b-8192-f8508a986ffe/ai/abs/flair-custom/custom_dict.pkl"),

    # comment in these lines to use flair embeddings
    # FlairEmbeddings('news-forward'),
    # CharLMEmbeddings('news-forward',use_cache=True), 
    ELMoEmbeddings('elmo-small'),
    # BertEmbeddings(),
    # FlairEmbeddings('news-backward-fast'),
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

#5. initialize sequence tagger
from flair.models import SequenceTagger

tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        rnn_layers= 2,
                                        tag_type=tag_type,
                                        use_crf=True)

# 6. initialize trainer
from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus)

# 7. start training
trainer.train('resources/taggers/usDL2',
              learning_rate=0.01,
              embeddings_in_memory=False,
              mini_batch_size=32,
              max_epochs=150,
              checkpoint=True)

# 8. plot training curves (optional)
from flair.visual.training_curves import Plotter
plotter = Plotter()
plotter.plot_training_curves('resources/taggers/nerpan/loss.tsv')
plotter.plot_weights('resources/taggers/nerpan/weights.txt')