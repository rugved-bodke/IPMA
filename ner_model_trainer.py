import numpy
import util
from feed_forward_ner import FeedForwardNER
import nltk

raw_data_set = []

raw_data_set.append({'word': "laptop", 'entity': "keyword"})
raw_data_set.append({'word': "phone", 'entity': "keyword"})
raw_data_set.append({'word': "jiofi", 'entity': "keyword"})
raw_data_set.append({'word': "1511030079", 'entity': "keyword"})
raw_data_set.append({'word': "8605343857", 'entity': "keyword"})

vocabulary = numpy.load ("D:\\beinglabs\\workspace\\ipma_web_app\\ner_vocabulary.npz")
words = vocabulary['words']
entities = vocabulary['entities'].tolist()
documents = vocabulary['documents'].tolist()
ignore_words = ["?", "'s"]

for pattern in raw_data_set:
    entities.append (pattern['entity'])
    documents.append ((pattern['word'], pattern['entity']))

entities = list(set(entities))

print (len (documents), "documents", documents)
print (len (entities), "entities", entities)
print (len (words), "set of words", words)

training_data_set = []

for doc in documents:
    training_data_input = []
    training_data_target = [0.01] * len (entities)
    pattern_word = doc[0].lower ()
    for word in words:
        (training_data_input.append (0.99) if word in pattern_word else training_data_input.append (0.01))
    if pattern_word not in words:
        training_data_input[len (training_data_input) - 2] = 0.99
    if util.is_numeric (pattern_word):
        training_data_input[len (training_data_input) - 1] = 0.99
    training_data_target[entities.index (doc[1])] = 0.99        
    training_data_set.append ((training_data_input, training_data_target))

print (len (training_data_set), "training data")

ffner = FeedForwardNER (input_nodes=len (words), hidden_nodes=15, output_nodes=len (entities), learning_rate=0.1)

for e in range (0, 1000):
    for training_data in training_data_set:
        ffner.train (training_data[0], training_data[1])

ffner.words = words
ffner.entities = entities
ffner.ignore_words = ignore_words
print ("Test sentence: remember that sourav is genious", "Entities: ", ffner.recognize ("remember that sourav is genious"))

numpy.savez_compressed ('ner_model', words = words, entities = entities, wih = ffner.wih, who = ffner.who)
print ("Model saved")
