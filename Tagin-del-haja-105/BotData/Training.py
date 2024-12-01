import random
import json
import numpy as np
import pickle
import nltk
#returning the word into its stem origin work working works worker same word
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential 
from keras.layers import Dense , Activation , Dropout
from keras.optimizers.legacy import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('./BotData/Data.json',encoding='utf-8').read())

words = []
classes = []
documents = []
ignore_letters = ['?','!','.',',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        #seperates the words from the patterns and then adding them
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list , intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
 
classes = sorted(set(classes))

pickle.dump(words,open('./BotData/words_test.pkl','wb'))
pickle.dump(classes,open('./BotData/classes_test.pkl','wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag,output_row])
    
random.shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:,0])
train_y = list(training[:,1])

model = Sequential()

model.add(Dense(128,input_shape = (len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)

model.compile(loss='categorical_crossentropy',optimizer=sgd, metrics = ['accuracy'])
model.fit(np.array(train_x),np.array(train_y),epochs= 200,batch_size= 5,verbose=1)

model.save('./BotData/test_model.   ')
print('done')