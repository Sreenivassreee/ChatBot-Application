import matplotlib.pyplot as plt
import pandas as pd
import tensorflow
from tensorflow import keras
import tflearn
import nltk
import random
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from nltk.tokenize import word_tokenize
import json
import numpy as np
import pickle

from nltk.tokenize import TweetTokenizer
tokens = TweetTokenizer()

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()

with open("data.json") as file:
    data=json.load(file)

'''try:
    words = pickle.load(open("words_mat.pkl", "rb"))'''

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    #print(intent)
    for pattern in intent['patterns']:
        wrds = tokens.tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])
    if intent["tag"] not in labels:
        labels.append(intent["tag"])

        # Beginning of second tutorial

    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))
    #labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    # end of second tutorial

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

#tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    hist = keras.models.load_model("main_project_model.h5")
    hist = model.fit(training, output, n_epoch=500, batch_size=8, show_metric=True)
    model.save("main_project_model_output.h5")


except Exception as e:
    print(e)
    print("This falls under exception block")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = tokens.tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return np.array(bag)


def chat(inp):
    if inp.lower() == "quit":
        break
    results = model.predict([bag_of_words(inp, words)])[0]

    results_index = np.argmax(results)

    tag = labels[results_index]

    print(results)
    print(results_index)
    print(labels)
    print(tag)
    #print(data["intents"])
    print(results[results_index])


    if results[results_index] > 0.7:
        for tg in data["intents"]:
            if tg["tag"]==tag:
                responces = tg["responces"]
                output=random.choice(responces)
                return output
                break
        #print(random.choice(responces))
        #print(labels)

    else:
        return "I didn't get that ,try again !"










