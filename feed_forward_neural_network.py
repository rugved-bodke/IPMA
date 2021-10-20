import numpy
import scipy.special

class FeedForwardNeuralNetwork:

    def __init__ (self, input_nodes, hidden_nodes, output_nodes, learning_rate, model_path=None):
        if model_path is not None:
            self.model = numpy.load (model_path)
            self.wih = self.model['wih']
            self.who = self.model['who']
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

    def train (self, inputs_list, targets_list):
        inputs = numpy.array (inputs_list, ndmin=2).T
        targets = numpy.array (targets_list, ndmin=2).T
        hidden_inputs = numpy.dot (self.wih, inputs)
        hidden_outputs = self.activation_function (hidden_inputs)
        final_inputs = numpy.dot (self.who, hidden_outputs)
        final_outputs = self.activation_function (final_inputs)
        output_errors = targets - final_outputs
        hidden_errors = numpy.dot (self.who.T, output_errors)
        self.who += self.lr * numpy.dot (output_errors * final_outputs * (1.0 - final_outputs), numpy.transpose (hidden_outputs))
        self.wih += self.lr * numpy.dot (hidden_errors * hidden_outputs * (1.0 - hidden_outputs), numpy.transpose (inputs))
        pass

    def query (self, inputs_list):
        inputs = numpy.array (inputs_list, ndmin=2).T
        hidden_inputs = numpy.dot (self.wih, inputs)
        hidden_outputs = self.activation_function (hidden_inputs)
        final_inputs = numpy.dot (self.who, hidden_outputs)
        final_outputs = self.activation_function (final_inputs)
        return final_outputs
