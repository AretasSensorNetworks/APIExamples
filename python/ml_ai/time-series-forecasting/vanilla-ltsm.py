import aretas_query_data as adq
from numpy import array
from keras.models import Sequential
from keras.layers import LTSM
from keras.layers import Dense


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
    return array(X), array(y)


def main():
    data = adq.get_data()

    if data is not None:
        raw_sequence = [x['data'] for x in data]

        num_steps: int = 30

        X, y = split_sequence(raw_sequence, num_steps)

        for i in range(len(X)):
            print(X[i], y[i])

        n_features = 1
        X = X.reshape((X.shape[0], X.shape[1], n_features))

        print(X)
        model = Sequential()
        model.add(LTSM(50, activation='relu', input_shape=(num_steps, n_features)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        # fit the model
        model.fit(X, y, epochs=200, verbose=0)

    else:
        print("Could not fetch any data!")


if __name__ == "__main__":
    main()


