import numpy
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

raw_data_set = []

raw_data_set.append({'class': "memories.create", 'sentence': "remember this"})
raw_data_set.append({'class': "memories.create", 'sentence': "can you remember something"})
raw_data_set.append({'class': "memories.create", 'sentence': "create a note"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember something"})
raw_data_set.append({'class': "memories.create", 'sentence': "note that my book is in trunk"})
raw_data_set.append({'class': "memories.create", 'sentence': "note that my enrollment number is 1511030079"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that the specific heat of water is 4.184 joules"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that my wrist watch is on table"})
raw_data_set.append({'class': "memories.create", 'sentence': "note that my mobile is in pocket"})
raw_data_set.append({'class': "memories.create", 'sentence': "note that my last month's electricity bill was 500 rupees"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember my mom's favorite color is blue"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that my aadhar card number is 1000100010001000"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that my pan card number is BKOQH4947E"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that I gave my STE manual to rugved"})
raw_data_set.append({'class': "memories.create", 'sentence': "note that I spent 120 rupees on my lunch"})
raw_data_set.append({'class': "memories.create", 'sentence': "note that my wallet is in drawer"})
raw_data_set.append({'class': "memories.create", 'sentence': "save my bike lock combo as 1234"})
raw_data_set.append({'class': "memories.create", 'sentence': "remember that I parked my car at G-12"})

raw_data_set.append({'class': "memories.get", 'sentence': "What is my enrollment number"})
raw_data_set.append({'class': "memories.get", 'sentence': "Whom did I give my manual"})
raw_data_set.append({'class': "memories.get", 'sentence': "Where is my book"})
raw_data_set.append({'class': "memories.get", 'sentence': "How much did I spent on my lunch"})
raw_data_set.append({'class': "memories.get", 'sentence': "What did I say about the specific heat of water"})
raw_data_set.append({'class': "memories.get", 'sentence': "Where is my pendrive"})
raw_data_set.append({'class': "memories.get", 'sentence': "What type of ink cartridge does my printer use"})
raw_data_set.append({'class': "memories.get", 'sentence': "Where did I park"})
raw_data_set.append({'class': "memories.get", 'sentence': "Where is my passport"})
raw_data_set.append({'class': "memories.get", 'sentence': "When did I call my mom"})
raw_data_set.append({'class': "memories.get", 'sentence': "When did I water the hermit crabs"})
raw_data_set.append({'class': "memories.get", 'sentence': "Who has my wallet"})

raw_data_set.append({'class': "memories.get_all", 'sentence': "Show all notes"})
raw_data_set.append({'class': "memories.get_all", 'sentence': "What did I ask you to remember"})

raw_data_set.append({'class': "memories.delete", 'sentence': "Forget what I said about my favorite color"})
raw_data_set.append({'class': "memories.delete", 'sentence': "Forget my enrollment number"})
raw_data_set.append({'class': "memories.delete", 'sentence': "Forget about my book"})

raw_data_set.append({'class': "memories.delete_all", 'sentence': "Forget everything you remember"})

raw_data_set.append({'class': "forget_that", 'sentence': "forget that"})
raw_data_set.append({'class': "forget_that", 'sentence': "Do not remember that"})
raw_data_set.append({'class': "forget_that", 'sentence': "delete that"})

raw_data_set.append({'class': "cancel", 'sentence': "cancel it"})
raw_data_set.append({'class': "cancel", 'sentence': "cancel"})
raw_data_set.append({'class': "cancel", 'sentence': "never mind"})
raw_data_set.append({'class': "cancel", 'sentence': "nevermind"})

raw_data_set.append({'class': "confirm", 'sentence': "yes"})
raw_data_set.append({'class': "confirm", 'sentence': "okay"})
raw_data_set.append({'class': "confirm", 'sentence': "yeah"})

raw_data_set.append({'class': "greetings", 'sentence': "Good morning"})
raw_data_set.append({'class': "greetings", 'sentence': "Hello"})
raw_data_set.append({'class': "greetings", 'sentence': "How are you"})
raw_data_set.append({'class': "greetings", 'sentence': "Hey"})

raw_data_set.append({'class': "help", 'sentence': "What can you do"})

raw_data_set.append({'class': "fallback", 'sentence': "Are you dumb"})
raw_data_set.append({'class': "fallback", 'sentence': "What is your name"})
raw_data_set.append({'class': "fallback", 'sentence': "Okay google"})
raw_data_set.append({'class': "fallback", 'sentence': "Hey siri"})
raw_data_set.append({'class': "fallback", 'sentence': "Hey alexa"})
raw_data_set.append({'class': "fallback", 'sentence': "Hey cortana"})
raw_data_set.append({'class': "fallback", 'sentence': "Do not"})
raw_data_set.append({'class': "fallback", 'sentence': "Do not remember something"})
raw_data_set.append({'class': "fallback", 'sentence': "Don't remember"})
raw_data_set.append({'class': "fallback", 'sentence': "Don't"})

words = []
classes = []
documents = []
ignore_words = ["?", "'s"]

for pattern in raw_data_set:
    w = nltk.word_tokenize (pattern['sentence'])
    words.extend (w)
    documents.append ((w, pattern['class']))
    if pattern['class'] not in classes:
        classes.append (pattern['class'])

words = [stemmer.stem (w.lower ()) for w in words if w not in ignore_words]
words = list(set(words))
words.append ("$unknown")
words.append ("$digit")

numpy.savez_compressed ('classifier_vocabulary', words = words, classes = classes, documents = documents)
print ("Vocabulary saved")
