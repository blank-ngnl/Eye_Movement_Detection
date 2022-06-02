import pandas as pd
import numpy as np
import mne
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

srate = 256

"""
Import data from CSV file
"""
def import_data(filename, path):
    data = pd.read_csv(path + filename)
    return data

"""
Apply bandpass filter
"""
def preprocess_raw(raw_data, l_freq, h_freq, plot=True):
    ch_names = ["TP9", "AF7", "AF8", "TP10"]
    ch_types = ['eeg'] * 4
    info = mne.create_info(ch_names, ch_types=ch_types, sfreq=srate)
    info.set_montage('standard_1020')

    timestamps = raw_data[:, 0]
    raw_eeg_data = np.moveaxis(raw_data[:, 1:5], [0, 1], [1, 0])
    markers = raw_data[:, 6]

    raw = mne.io.RawArray(raw_eeg_data, info)
    if plot:
        raw.plot(block=True, clipping=None, scalings={"eeg": 200})
    raw.filter(l_freq=l_freq, h_freq=h_freq)
    if plot:
        raw.plot(block=True, clipping=None, scalings={"eeg": 200})

    return timestamps, raw.get_data(), markers

"""
Extract epoch from raw data
"""
def extract_epoch(timestamps, raw_eeg_data, markers):
    # channels: ["TP9", "AF7", "AF8", "TP10"]
    selected_channels = [0, 1, 2, 3]
    selected_markers = [1, 2, 3]
    duration = [-0.25, 1.75]

    X = []
    Y = []

    for index, event in enumerate(markers):
        if event in selected_markers:
            current_trial = None
            for channel in selected_channels:
                new_trial = np.expand_dims(np.array(raw_eeg_data[channel, index+int(duration[0]*srate):index+int(duration[1]*srate)]), axis=0)
                #print(event, index+int(duration[0]*srate), index, index+int(duration[1]*srate), raw_eeg_data[channel, index])
                if current_trial is None:
                    current_trial = new_trial
                else:
                    current_trial = np.concatenate((current_trial, new_trial), axis=0)
            #print(current_trial.shape)
            X.append(current_trial)
            Y.append(event)
    
    X = np.array(X)
    Y = np.array(Y)
    print("X: ", X.shape, ", Y: ", Y.shape)

    return X, Y

"""
Apply Independent Component Analysis (ICA)
"""
def ICA(X):
    ch_names = ["TP9", "AF7", "AF8", "TP10"]
    ch_types = ['eeg'] * 4
    info = mne.create_info(ch_names, ch_types=ch_types, sfreq=srate)
    info.set_montage('standard_1020')
    X = mne.EpochsArray(X, info)
    X.plot(n_epochs=1)

    return X

"""
Visualize data
"""
def visualize_data(X, Y):
    None

"""
Train and evaluate classifer
"""
def train_classifier(X, Y):
    X = X.reshape(X.shape[0], -1)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=42)
    clf = make_pipeline(StandardScaler(), SVC(kernel='linear', gamma='auto'))
    clf.fit(X_train, Y_train)
    Y_hat = clf.predict(X_test)
    print("test accuracy: ", accuracy_score(Y_test, Y_hat))