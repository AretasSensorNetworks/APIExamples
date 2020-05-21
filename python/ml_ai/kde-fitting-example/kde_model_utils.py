from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
import numpy as np
import time


def now_ms():
    return int(time.time() * 1000)


def kde_model_selection(data_n):

    # kernel_selection = ['gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine']
    kernel_selection = ['gaussian', 'tophat', 'epanechnikov']

    kernel_bandwidth_space = np.geomspace(0.1, 100, 10)

    print("First kernel_bandwidth_space: {}".format(kernel_bandwidth_space))

    startMs = now_ms()

    # very basic estimate for best bandwidth selection
    grid = GridSearchCV(KernelDensity(), {'bandwidth': kernel_bandwidth_space,
                                          'kernel': kernel_selection}, cv=5, iid=False)
    grid.fit(data_n)
    bw = grid.best_params_

    # get the best bandwidth and run one more tuning step
    index = None
    for i in range(len(kernel_bandwidth_space)):
        if kernel_bandwidth_space[i] == bw['bandwidth']:
            index = i

    start_idx = index - 1
    end_idx = index + 1

    if start_idx < 0:
        start_idx = 0

    if end_idx > (len(kernel_bandwidth_space) - 1):
        end_idx = len(kernel_bandwidth_space) - 1

    kernel_bandwidth_space = np.geomspace(kernel_bandwidth_space[start_idx], kernel_bandwidth_space[end_idx], 10)

    print("Second kernel_bandwidth_space: {}".format(kernel_bandwidth_space))

    print(bw)

    model = KernelDensity(bandwidth=bw['bandwidth'], kernel=bw['kernel'])
    model.fit(data_n)

    print("Took {} ms to perform GridSearch/fit".format(now_ms() - startMs))

    # print(model)

    return model


def get_probability(start_value, end_value, eval_points, fitted_model):

    # Number of evaluation points
    N = eval_points
    step = (end_value - start_value) / (N - 1)  # Step size

    x = np.linspace(start_value, end_value, N)[:, np.newaxis]  # Generate values in the range
    kd_vals = np.exp(fitted_model.score_samples(x))  # Get PDF values for each x
    probability_est = np.sum(kd_vals * step)  # Approximate the integral of the PDF
    return probability_est.round(4)
