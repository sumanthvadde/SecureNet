# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 12:18:32 2019

@author: rajat bothra
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 22:27:56 2019

@author: rajat bothra
"""
#importing the libraries 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('final2.csv')
X = dataset.iloc[:, :30].values
y = dataset.iloc[:, 30].values
 
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling using normalization
print(X_test[0])
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

# Part 2 - Now let's make the ANN!
# Importing the Keras libraries and packages for applying deep learning algorithim
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 16, kernel_initializer = 'uniform', activation = 'relu', input_dim = 30))

# Adding the second hidden layer
classifier.add(Dense(units = 16, kernel_initializer = 'uniform', activation = 'relu'))

# Adding the output layer
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


classifier.fit(X_train, y_train, batch_size = 10, epochs = 100)
#serialize classifier to JSON
classifier_json = classifier.to_json()
with open("classifier.json", "w") as json_file:
    json_file.write(classifier_json)

# serialize weights to HDF5
classifier.save_weights("classifier.h5")
print("Saved classifier to disk")
 
# later...
 
# load json and create classifier
json_file = open('classifier.json', 'r')
loaded_classifier_json = json_file.read()
json_file.close()
loaded_classifier = model_from_json(loaded_classifier_json)
# load weights into new classifier
loaded_classifier.load_weights("classifier.h5")
print("Loaded classifier from disk", loaded_classifier)
# # Fitting the ANN to the Training set

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix for test data
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

