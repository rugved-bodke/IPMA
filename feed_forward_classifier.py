import numpy
import util
import scipy.special
import nltk
from feed_forward_neural_network import FeedForwardNeuralNetwork
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

class FeedForwardClassifier (FeedForwardNeuralNetwork):

    def __init__ (self, input_nodes=None, hidden_nodes=None, output_nodes=None, learning_rate=None, model_path=None):
        if model_path is not None:
            model = numpy.load (model_path)
            self.wih = model['wih']
            self.who = model['who']
            self.words = model['words']
            self.classes = model['classes']
            self.ignore_words = ["?", "'s"]
            pass
        else:
            self.inodes = input_nodes
            self.hnodes = hidden_nodes
            self.onodes = output_nodes
            self.wih = numpy.random.normal (0.0, pow (self.hnodes, -0.5), (self.hnodes, self.inodes))
            self.who = numpy.random.normal (0.0, pow (self.onodes, -0.5), (self.onodes, self.hnodes))
            self.lr = learning_rate
            pass
        self.activation_function = lambda x: scipy.special.expit (x)
        pass
    
    def classify (self, sentence):
        query_data_input = []
        query_words = nltk.word_tokenize (sentence)
        query_words = [stemmer.stem (word.lower ()) for word in query_words if word not in self.ignore_words]
        for w in self.words:
            (query_data_input.append (0.99) if w in query_words else query_data_input.append (0.01))
        for w in query_words:
            if w not in self.words:
                query_data_input[len (query_data_input) - 2] = 0.99
            if util.is_numeric (w):
                query_data_input[len (query_data_input) - 1] = 0.99
        return self.classes[numpy.argmax (self.query (query_data_input))]

#ffc = FeedForwardClassifier (model_path = "D:\\beinglabs\\workspace\\ipma_web_app\\classifier_model.npz")
#print ("Test sentence: forget my mom's favorite color", "Class: ", ffc.classify ("forget my mom's favorite color"))
