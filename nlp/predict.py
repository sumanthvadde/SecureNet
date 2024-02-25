import keras
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
import sys
import os

classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 16, kernel_initializer = 'uniform', activation = 'relu', input_dim = 30))

# Adding the second hidden layer
classifier.add(Dense(units = 16, kernel_initializer = 'uniform', activation = 'relu'))

# Adding the output layer
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))


json_file = open('classifier.json', 'r')
loaded_classifier_json = json_file.read()
json_file.close()
loaded_classifier = model_from_json(loaded_classifier_json)
# load weights into new classifier
loaded_classifier.load_weights("classifier.h5")
print(sys.argv[1].split(','))
predict = sys.argv[1].split(',')
print(predict)
length = predict.length / 30
print(length)
features = []
for(i in range(0,length)):
    predict.slice(i*30,i*30+30)
    
loaded_classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
output = loaded_classifier.predict(predict)
print(output)