import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
tokens = TweetTokenizer()
print("all headers executed")


from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense , Activation , Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

print("everything from tensorflow has been imported")


intents = json.loads(open("/Users/reddivaridamu/Desktop/chatbot/chat/data.json").read())


words = []
classes = []
documents = []
ignore_letters = ["?","!",".",","]


for intent in intents["intents"]:
  for pattern in intent["patterns"]:
    word_list = tokens.tokenize(pattern)
    words.extend(word_list)
    documents.append((word_list,intent["tag"]))
    if intent["tag"] not in classes:
      classes.append(intent["tag"])

print(documents)


words = [ps.stem(word) for word in words if word not in ignore_letters ]
words = sorted(set(words))
classes = sorted(set(classes))
pickle.dump(words,open("words.pkl","wb"))
pickle.dump(classes,open("classes.pkl","wb"))
print(words)


training = []
output_empty = [0]*len(classes)

for document in documents:
  bag = []
  word_patterns = document[0]
  word_patterns = [ps.stem(word.lower()) for word in word_patterns]
  for word in words:
      bag.append(1) if word in word_patterns else bag.append(0)
      output_row = list(output_empty)
      output_row[classes.index(document[1])]=1
      training.append([bag,output_row])


random.shuffle(training)
training = np.array(training)


train_x = list(training[:,0])
train_y = list(training[:,1])


model = Sequential()
model.add(Dense(128, input_shape = (len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation = "softmax"))


sgd = SGD(lr=0.01 , decay=1e-6, momentum=0.9,nesterov=True)
model.compile(loss="categorical_crossentropy",optimizer=sgd,metrics=["accuracy"])
for i in range(100):
    if i==1:
        hist=model.fit(np.array(train_x),np.array(train_y),epochs=100,batch_size=5,verbose=1)

    if i==99:
        model.save("main_project_model.h5",hist)
print("done")