# -*- coding: utf-8 -*-
"""
Created on Thu May 20 18:27:50 2021

@author: dheer
"""

import pandas as pd
import numpy as np
from keras.layers import Input, Dense
from keras.models import Model
from sklearn.model_selection import train_test_split

class AutoEncoder():
    
    def PerformOperation():
        #load and prepare data
        input_vecs = np.array(pd.read_csv("inputvector_table.txt", sep =" ", header =None))
        vectors = input_vecs[:,2:]
        labels = input_vecs[:,:2]
        
        vectors = np.asarray(vectors).astype('float32')
        
        x_train, x_test, y_train, y_test = train_test_split(vectors, labels, test_size=0.33, random_state=1)
        
        x_train = np.asarray(x_train).astype('float32')
        x_test = np.asarray(x_test).astype('float32')
        
        #Setup autoencoder structure
        input_vector = Input(shape=(16,)) #Use 16 floats vector as input
        encoded_1 = Dense(500, activation='selu')(input_vector)
        encoded_2 = Dense(250, activation='selu')(encoded_1)
        middle_layer = Dense(2, activation='elu')(encoded_2)
        decoded_1 = Dense(250, activation='selu')(middle_layer)
        decoded_2 = Dense(500, activation='selu')(decoded_1)
        decoded_output = Dense(16, activation='sigmoid')(decoded_2)
        
        
        autoencoder = Model(input_vector, decoded_output)
        autoencoder.compile(optimizer='rmsprop', loss='mae')
        autoencoder.summary()
        
        #Train the autoencoder
        autoencoder.fit(x_train, x_train,
                        epochs=30, #also used many different epoch values/batch sizes
                        batch_size=4,
                        shuffle=True,
                        validation_data=(x_test, x_test))
        
        autofitted = autoencoder.predict(vectors)
        
        #compare to estimate performance
        autofitted[1]
        x_test[1]
        
        #separate encoder
        encoder = Model(input_vector, middle_layer)
        encoder.compile(optimizer='rmsprop', loss='mae')
        
        #predict encoded vectors from input vectors
        encoded_vecs = encoder.predict(vectors)
        
        #separate decoder
        encoded_vector = Input(shape=(2,))
        deco1 = autoencoder.layers[-3](encoded_vector)
        deco2 = autoencoder.layers[-2](deco1)
        decoout = autoencoder.layers[-1](deco2)
        decoder = Model(encoded_vector, decoout)
        
        #predict decoded vectors from encoded vectors
        decoded_vecs = decoder.predict(encoded_vecs)
        
        #Confirm that separate encoding/decoding does the same as the autoencoder
        np.array_equal(autofitted, decoded_vecs)
        
        #Write labels with corresponding encoded values to file
        output = np.concatenate((labels,encoded_vecs), axis=1)
        np.savetxt("encoded_with_labels.txt", output, fmt='%s', delimiter=',')

