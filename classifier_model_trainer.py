import numpy
import util
from feed_forward_classifier import FeedForwardClassifier
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

raw_data_set = []

raw_data_set.append({'class': "memories.create", 'sentence': "remember that my spare keys are in the drawer next to the sink"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that I parked the car in the 2nd level"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that my hotel room safe code is 6666"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that my registration number is Z1234"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that amit's favorite soccer team is manchester united"})

raw_data_set.append({'class': "memories.get", 'sentence': "where are my spare keys"})
raw_data_set.append({'class': "memories.get", 'sentence': "what is my hotel room safe code"})
raw_data_set.append({'class': "memories.get", 'sentence': "what is my registration number"})
raw_data_set.append({'class': "memories.get", 'sentence': "where are my spare keys"})
raw_data_set.append({'class': "memories.get", 'sentence': "which soccer team does amit like"})

vocabulary = numpy.load ("D:\\beinglabs\\workspace\\ipma_web_app\\classifier_vocabulary.npz")
words = vocabulary['words']
classes = vocabulary['classes'].tolist ()
documents = vocabulary['documents'].tolist ()
ignore_words = ["?", "'s"]

for pattern in raw_data_set:
    w = nltk.word_tokenize (pattern['sentence'])
    documents.append ((w, pattern['class']))
    if pattern['class'] not in classes:
        classes.append (pattern['class'])

print (len (documents), "documents", documents)
print (len (classes), "classes", classes)
print (len (words), "set of stemmed words", words)

ffc = FeedForwardClassifier (input_nodes=len (words), hidden_nodes=15, output_nodes=len (classes), learning_rate=0.1)

training_data_set = []

for doc in documents:
    training_data_input = []
    training_data_target = [0.01] * len(classes)
    pattern_words = doc[0]
    pattern_words = [stemmer.stem (word.lower ()) for word in pattern_words]
    for w in words:
        (training_data_input.append (0.99) if w in pattern_words else training_data_input.append (0.01))
    for w in pattern_words:
        if w not in words:
            training_data_input[len (training_data_input) - 2] = 0.99
        if util.is_numeric (w):
            training_data_input[len (training_data_input) - 1] = 0.99
    training_data_target[classes.index (doc[1])] = 0.99
    training_data_set.append ((training_data_input, training_data_target))

print (len (training_data_set), "training data")

for e in range (0, 500):
    for training_data in training_data_set:
        ffc.train (training_data[0], training_data[1])

ffc.words = words
ffc.classes = classes
ffc.ignore_words = ignore_words
print ("Test sentence: forget my mom's favorite color", "Class: ", ffc.classify ("forget my mom's favorite color"))

numpy.savez_compressed ('classifier_model', words = words, classes = classes, wih = ffc.wih, who = ffc.who)
print ("Model saved")
