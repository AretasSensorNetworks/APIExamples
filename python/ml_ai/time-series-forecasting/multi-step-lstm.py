import aretas_query_data as adq
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from matplotlib import pyplot


# split a univarate sequence into samples
def split_sequence(sequence, steps_in, steps_out):

    X, y = list(), list()

    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + steps_in
        out_end_ix = end_ix + steps_out
        # check if we are beyond the sequence
        if out_end_ix > len(sequence):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i: end_ix], sequence[end_ix:out_end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


def main():
    data = adq.get_data()

    if data is not None:

        raw_sequence = np.array([x['data'] for x in data])

        print("Number of data points:{0}".format(len(raw_sequence)))

        # get a test train split
        train_size = int(len(raw_sequence) * 0.7)
        test_size = len(raw_sequence) - train_size

        train, test = raw_sequence[0:train_size], raw_sequence[train_size:len(raw_sequence)]

        num_steps_in: int = 50
        num_steps_out: int = 20

        X_train, y_train = split_sequence(train, num_steps_in, num_steps_out)
        X_test, y_test = split_sequence(test, num_steps_in, num_steps_out)

        show_data = False

        if show_data is not False:
            for i in range(len(X_train)):
                print(X_train[i], y_train[i])

            for i in range(len(X_test)):
                print(X_test[i], y_test[i])

        n_features = 1
        # reshape from [samples, timesteps] to [samples, timesteps, features]
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], n_features))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], n_features))

        y_train = y_train.reshape((y_train.shape[0], y_train.shape[1], n_features))
        y_test = y_test.reshape((y_test.shape[0], y_test.shape[1], n_features))

        # print(X)

        model = Sequential()
        model.add(LSTM(200, activation='relu', return_sequences=True, input_shape=(num_steps_in, n_features)))
        model.add(LSTM(200, activation='relu'))
        model.add(Dense(num_steps_out))
        model.compile(optimizer='adam', loss='mse')

        print("Fitting model")
        # fit the model
        model.fit(X_train, y_train, epochs=50, verbose=0)
        print("Model fitted")

        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)

        print(test_predictions)

        lag_padding = [np.nan for i in range(num_steps_in)]
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


