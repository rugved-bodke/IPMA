import numpy
import re
import util
import scipy.special
from feed_forward_neural_network import FeedForwardNeuralNetwork
import nltk

class FeedForwardNER (FeedForwardNeuralNetwork):

    def __init__ (self, input_nodes=None, hidden_nodes=None, output_nodes=None, learning_rate=None, model_path=None):
        if model_path is not None:
            self.model = numpy.load (model_path)
            self.wih = self.model['wih']
            self.who = self.model['who']
            self.words = numpy.ndarray.tolist (self.model['words'])
            self.entities = numpy.ndarray.tolist (self.model['entities'])
            self.ignore_words = ["?", "'s"]
        else:
            self.inodes = input_nodes
            self.hnodes = hidden_nodes
            self.onodes = output_nodes
            self.wih = numpy.random.normal (0.0, pow (self.hnodes, -0.5), (self.hnodes, self.inodes))
            self.who = numpy.random.normal (0.0, pow (self.onodes, -0.5), (self.onodes, self.hnodes))
            self.lr = learning_rate
        self.activation_function = lambda x: scipy.special.expit (x)

    
    def recognize (self, sentence):
        query_words = nltk.word_tokenize (sentence)
        query_words = [word.lower () for word in query_words if not word in self.ignore_words]
        result_words = [[] for entity in self.entities]
        result_document = []
        for query_word in query_words:
            query_data_input = []
            for word in self.words:
                (query_data_input.append (0.99) if word == query_word else query_data_input.append (0.01))
            if query_word not in self.words:
                query_data_input[len (query_data_input) - 2] = 0.99
            if util.is_numeric (query_word):
                query_data_input[len (query_data_input) - 1] = 0.99
            result_words[numpy.argmax (self.query (query_data_input))].append (query_word)
        result_document.append ({self.entities[i]: result_words[i] for i in range (0, len (result_words))})
        return result_document

#ffner = FeedForwardNER (model_path = "D:\\beinglabs\\workspace\\ipma_web_app\\ner_model.npz")
#print ("Test sentence: remember that sourav is genious", "Entities: ", ffner.recognize ("remember that sourav is genious"))
