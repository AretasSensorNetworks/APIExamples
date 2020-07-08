import aretas_query_data as adq
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from matplotlib import pyplot


# split a univarate sequence into samples
def split_sequence(sequence, n_steps):

    X, y = list(), list()

    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i: end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


def main():
    data = adq.get_data()

    if data is not None:
        raw_sequence = np.array([x['data'] for x in data])

        # get a test train split
        train_size = int(len(raw_sequence) * 0.7)
        test_size = len(raw_sequence) - train_size

        train, test = raw_sequence[0:train_size], raw_sequence[train_size:len(raw_sequence)]

        num_steps: int = 30

        X_train, y_train = split_sequence(train, num_steps)
        X_test, y_test = split_sequence(test, num_steps)

        for i in range(len(X_train)):
            print(X_train[i], y_train[i])

        n_features = 1
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], n_features))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], n_features))

        # print(X)

        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(num_steps, n_features)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        print("Fitting model")
        # fit the model
        model.fit(X_train, y_train, epochs=200, verbose=0)
        print("Model fitted")

        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)

        lag_padding = [np.nan for i in range(num_steps)]
        test_predictions = [x[0] for x in test_predictions]
        train_predictions = [x[0] for x in train_predictions]

        plot_predictions = lag_padding + train_predictions + lag_padding + test_predictions

        # print(model.predict(X_test))
        pyplot.plot(raw_sequence)
        pyplot.plot(plot_predictions)
        pyplot.show()

    else:
        print("Could not fetch any data!")


if __name__ == "__main__":
    main()


