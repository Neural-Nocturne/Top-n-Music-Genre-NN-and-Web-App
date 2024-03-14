import json
import numpy as np
from sklearn.model_selection import train_test_split
import keras


DATA_PATH = 'mfcc.json'


def load_data(data_path):
    """
    """

    with open(data_path, 'r') as fp:
        data = json.load(fp)

    X = np.array(data['mfcc'])
    y = np.array(data['labels'])
    return X, y


def prepare_datasets(test_size, validation_size):
    """
    """

    # load data
    X, y = load_data(DATA_PATH)

    # create train/test split
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=test_size)

    # create train/validation split from the train/test split
    X_train, X_validation, y_train, y_validation = train_test_split(X_train,
                                                                    y_train,
                                                                    test_size=validation_size)

    # tensorflow expects a 3d array -> (130, 13, 1) - 13 for mfccs
    # cont. - for each sample, CNN expects 3 dimensional arrays,
    # cont. - 3rd dimension is the channel. Channel is 1 for greyscale.
    # cont. - ... means give me what is already in the array.
    X_train = X_train[..., np.newaxis]  # 4d array -> (num_samples, 130, 13, 1)
    X_validation = X_validation[..., np.newaxis]
    X_test = X_test[..., np.newaxis]

    return X_train, X_validation, X_test, y_train, y_validation, y_test


def build_model(input_shape):
    """
    """

    # create model
    model = keras.Sequential()

    # 1st conv layer, (3,3) size for kernel is kindof customary.
    model.add(keras.layers.Conv2D(128, (3, 3), activation='relu', input_shape=input_shape))
    model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding='same'))
    model.add(keras.layers.BatchNormalization())  # Helps speed up training significantly.
    # cont. - also makes the models way more reliable. This is on BatchNormalization.

    # 2nd conv layer
    model.add(keras.layers.Conv2D(256, (3, 3), activation='relu', input_shape=input_shape))
    model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding='same'))
    model.add(keras.layers.BatchNormalization())

    # 3rd conv layer, I believe maxpooling window has to match the conv2d window/filter?
    model.add(keras.layers.Conv2D(512, (2, 2), activation='relu', input_shape=input_shape))
    model.add(keras.layers.MaxPool2D((2, 2), strides=(2, 2), padding='same'))
    model.add(keras.layers.BatchNormalization())

    # flatten the output and feed it into dense layer
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(512, activation='relu'))
    model.add(keras.layers.Dropout(0.3))  # to prevent overfitting.
    # output layer
    model.add(keras.layers.Dense(512, activation='relu'))
    model.add(keras.layers.Dropout(0.3))  # to prevent overfitting.
    model.add(keras.layers.Dense(10, activation='softmax'))
    # softmax creates a probability distribution for each genre choice, taking the max.

    return model


def predict(model, X, y):
    """
    """

    X = X[np.newaxis, ...]

    # prediction = [ [0.1, 0.2, ...] ] we get the ten values for prediction on 10 different genres.
    prediction = model.predict(X)  # X -> (1, 130, 13, 1) expects 4 dimensions, first dimension is number of samples to predict.

    # extract index with max value, axis tells us to get max on first dimension which are genre choices.
    predicted_index = np.argmax(prediction, axis=1) # [3]
    print(f'Expected index: {y}, Predicted index: {predicted_index}')


if __name__ == '__main__':
    # create train, validation and test sets, X is input, y is the target.
    X_train, X_validation, X_test, y_train, y_validation, y_test = prepare_datasets(0.25, 0.2)

    # build the CNN net, we start at index 1 because refer to notes in prepare_dataset
    # cont. - function, each index of X_train is for one sample, which has a 
    # cont. = shape of 130, 13, 1 - which is 130 time bins, 13 mfccs and 1 channel (power color)
    input_shape = (X_train.shape[1], X_train.shape[2], X_train.shape[3])
    print(f'input shape is: {input_shape}')
    model = build_model(input_shape)

    # compile the network
    optimizer = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    # train the CNN
    model.fit(X_train, y_train, validation_data=(X_validation, y_validation), batch_size=32, epochs=30)

    # evaluate the CNN on the test set
    test_error, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
    print(f'Accuracy on test set is: {test_accuracy}')

    # make prediction on a sample
    X = X_test[100]
    y = y_test[100]

    predict(model, X, y)
