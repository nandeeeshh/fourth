import numpy as np
import re
import itertools
from collections import Counter


def clean_str(string):
    """
    Tokenization/string cleaning for datasets.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

"""
    Loads polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
"""
    
def load_data_and_labels():
    # Load data from files
    #positive_examples = list(open("./data/rt-polarity.pos", "r", encoding='latin-1').readlines())
	positive_examples = list(open("./data/posreviews.txt", "r", encoding='utf-8').readlines())
	positive_examples = [s.strip() for s in positive_examples] #remove white spaces in the beginning
    #negative_examples = list(open("./data/rt-polarity.neg", "r", encoding='latin-1').readlines())
	negative_examples = list(open("./data/negreviews.txt", "r", encoding='utf-8').readlines())
	negative_examples = [s.strip() for s in negative_examples] #remove white spaces in the beginning
	# Split by words
	x_text = positive_examples + negative_examples
	x_text = [clean_str(sent) for sent in x_text] #remove mulitple blank spaces
	x_text = [s.split(" ") for s in x_text]    # List of Lists of all the words in each review
    # Generate labels
	positive_labels = [[1] for _ in positive_examples] 
	negative_labels = [[0] for _ in negative_examples]
	y = np.concatenate([positive_labels, negative_labels], 0)
	return [x_text, y]


def pad_sentences(sentences, padding_word="<PAD/>"):
    """
    Pads all sentences to the same length. The length is defined by the longest sentence.
    Returns padded sentences.
    """
	#thefile=open('./datatobeclaasified.txt','w',encoding='utf-8');
	#for item in sentences:
		#thefile.write("%s" % item)
	
	
	
	
    sequence_length = max(len(x) for x in sentences)
    padded_sentences = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        num_padding = sequence_length - len(sentence)
        new_sentence = sentence + [padding_word] * num_padding
        padded_sentences.append(new_sentence)
    return padded_sentences

"""
    Builds a vocabulary mapping from word to index based on the sentences.
    Returns vocabulary mapping and inverse vocabulary mapping.
"""
def build_vocab(sentences):
    
    # Build vocabulary
	word_counts = Counter(itertools.chain(*sentences))
    # Mapping from index to word
	vocabulary_inv = [x[0] for x in word_counts.most_common()]
	vocabulary_inv = list(sorted(vocabulary_inv))
	# Mapping from word to index
	vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
	return [vocabulary, vocabulary_inv]


def build_input_data(sentences, labels, vocabulary):
    """
    Maps sentences and labels to vectors based on a vocabulary.
    """
    x = np.array([[vocabulary[word] for word in sentence] for sentence in sentences])
    y = np.array(labels)
    return [x, y]


def load_data():
    """
    Loads and preprocessed data for the dataset.
    Returns input vectors, labels, vocabulary, and inverse vocabulary.
    """
    # Load and preprocess data
    sentences, labels = load_data_and_labels()
    sentences_padded = pad_sentences(sentences)
    vocabulary, vocabulary_inv = build_vocab(sentences_padded)
    x, y = build_input_data(sentences_padded, labels, vocabulary)
    return [x, y, vocabulary, vocabulary_inv]
