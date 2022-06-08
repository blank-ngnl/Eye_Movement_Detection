import pandas as pd
import numpy as np
import mne
from mne.preprocessing import ICA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from model import *
from pylsl import StreamInlet, resolve_byprop
import time
from threading import Thread

srate = 256
res = []
timestamps = []
stop = False

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
        raw.plot(block=True, clipping=None, scalings={"eeg": 200}, title="raw")
    raw.filter(l_freq=l_freq, h_freq=h_freq)
    if plot:
        raw.plot(block=True, clipping=None, scalings={"eeg": 200}, title="bandpass filtered")
        plt.show()

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
def apply_ICA(X, threshold, plot=True):
    ch_names = ["TP9", "AF7", "AF8", "TP10"]
    ch_types = ['eeg'] * 4
    info = mne.create_info(ch_names, ch_types=ch_types, sfreq=srate)
    info.set_montage('standard_1020')
    X = mne.EpochsArray(X, info)
    if plot:
        X.plot(n_epochs=1, block=True, scalings={"eeg": 200}, title="epochs")

    ica = ICA(max_iter='auto', random_state=97)
    ica.fit(X)
    if plot:
        ica.plot_sources(X, block=True, title="sources")
        ica.plot_components(title="components")
    
    eog_indices, eog_scores = ica.find_bads_eog(X, ch_name=["AF7", "AF8"], threshold=threshold)
    print("eog_indices: ", eog_indices)

    exclude_indices = list(range(ica.n_components_))
    for index in eog_indices:
        if index in exclude_indices:
            exclude_indices.remove(index)

    if plot:
        ica.plot_scores(eog_scores, eog_indices)
        ica.plot_properties(X, picks=eog_indices)
    X_eog = ica.apply(X.copy(), exclude=exclude_indices)
    if plot:
        X_eog.plot(n_epochs=1, block=True, scalings={"eeg": 200}, title="eog epochs")

    return X_eog.get_data()

"""
Visualize data
"""
def visualize_data(X, Y):
    None

"""
Process data from multiple subjects 
import data -> bandpass filter -> extract epochs -> ICA -> store data using dictionary
"""
def preprocess_pipeline(filenames, path, l_freq=None, h_freq=None, threshold=None, plot=True):
    Xs, Ys = {}, {}

    for filename in filenames:
        print(filename)

        raw_data = import_data(filename, path)
        raw_data = raw_data.to_numpy(copy=True)

        # bandpass filter
        if l_freq == None and h_freq == None:
            timestamps = raw_data[:, 0]
            raw_eeg_data = np.moveaxis(raw_data[:, 1:5], [0, 1], [1, 0])
            markers = raw_data[:, 6]
        else:
            timestamps, raw_eeg_data, markers = preprocess_raw(raw_data, l_freq=l_freq, h_freq=h_freq, plot=plot)
        
        print("timestamps: ", timestamps.shape, ", raw_eeg_data: ", raw_eeg_data.shape, ", markers: ", markers.shape)

        X, Y = extract_epoch(timestamps, raw_eeg_data, markers)

        if threshold is not None:
            X = apply_ICA(X, threshold, plot=plot)

        # visualize_data(X, Y)

        Xs[filename[:-4]] = X
        Ys[filename[:-4]] = Y

    return Xs, Ys

"""
Train and evaluate classifer
"""
def train_classifier(X, Y, classifier="svm"):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=42)

    clf = my_clf(classifier)
    clf.fit(X_train, Y_train)
    Y_hat = clf.predict(X_test)
    print("using classifier: ", classifier)
    print("test accuracy: ", accuracy_score(Y_test, Y_hat))

def train_classifer_cross_subject(Xs, Ys, train_subject, test_subject, classifier="svm"):
    X_train, Y_train = Xs[train_subject], Ys[train_subject]
    X_test, Y_test = Xs[test_subject], Ys[test_subject]

    clf = my_clf(classifier)
    clf.fit(X_train, Y_train)
    Y_hat = clf.predict(X_test)
    print("using classifier: ", classifier)
    print("test accuracy: ", accuracy_score(Y_test, Y_hat))

"""
Train a classifier for inference
"""
def test_classifier(Xs, Ys, subject, classifier="svm"):
    X_train, Y_train, X_test, Y_test = [], [], [], []
    if subject == "All":
        for key in Xs.keys():
            x_train, x_test, y_train, y_test = train_test_split(Xs[key], Ys[key], test_size=0.2, stratify=Ys[key], random_state=42)
            X_train.append(x_train)
            Y_train.append(y_train)
            X_test.append(x_test)
            Y_test.append(y_test)
    else:
        X_train, X_test, Y_train, Y_test = train_test_split(Xs[subject], Ys[subject], test_size=0.2, stratify=Ys[subject], random_state=42)

    X_train, Y_train, X_test, Y_test = np.array(X_train), np.array(Y_train), np.array(X_test), np.array(Y_test)
    X_train = X_train.reshape(-1, X_train.shape[-2], X_train.shape[-1])
    Y_train = Y_train.reshape(-1)
    X_test = X_test.reshape(-1, X_test.shape[-2], X_test.shape[-1])
    Y_test = Y_test.reshape(-1)

    # print(X_train.shape)
    # print(Y_train.shape)
    # print(X_test.shape)
    # print(Y_test.shape)

    clf = my_clf(classifier)
    clf.fit(X_train, Y_train)
    Y_hat = clf.predict(X_test)
    print("using classifier: ", classifier)
    print("test accuracy: ", accuracy_score(Y_test, Y_hat))

    return clf

"""
Collect data
"""
def collect_data():
    global res, timestamps, stop

    data_source = "EEG"
    chunk_length = 12
    LSL_SCAN_TIMEOUT = 5

    print("Looking for a %s stream..." % (data_source))
    streams = resolve_byprop('type', data_source, timeout=LSL_SCAN_TIMEOUT)

    if len(streams) == 0:
        print("Can't find %s stream." % (data_source))
        stop = True
        return

    print("Started acquiring data.")
    inlet = StreamInlet(streams[0], max_chunklen=chunk_length)
    # eeg_time_correction = inlet.time_correction()

    info = inlet.info()
    description = info.desc()

    Nchan = info.channel_count()

    ch = description.child('channels').first_child()
    ch_names = [ch.child_value('label')]
    for i in range(1, Nchan):
        ch = ch.next_sibling()
        ch_names.append(ch.child_value('label'))

    res = np.zeros((10*srate, 4))
    timestamps = np.zeros((10*srate, 1))
    t_init = time.time()
    time_correction = inlet.time_correction()
    print('Start recording at time t=%.3f' % t_init)
    print('Time correction: ', time_correction)
    while not stop:
        data, timestamp = inlet.pull_chunk(
            timeout=1.0, max_samples=chunk_length)
        data = np.array(data)[:, :4]
        timestamp = np.expand_dims(np.array(timestamp), axis=1)
        #print(data.shape)
        #print(timestamp.shape)

        if len(timestamp) != 0:
            res = np.concatenate((res, data), axis=0)
            timestamps = np.concatenate((timestamps, timestamp), axis=0)
            res = res[-10*srate:, :]
            timestamps = timestamps[-10*srate:]

"""
Inference
"""
def inference(clf, l_freq=None, h_freq=None, threshold=None):
    global stop
    # collect data
    collect_thread = Thread(target=collect_data)
    collect_thread.start()
    time.sleep(5)

    try:
        while not stop:
            if len(res) == 10*srate and len(timestamps) == 10*srate: 
                #print(res)
                #print(timestamps)
                raw_data = np.concatenate((timestamps, res, np.zeros((res.shape[0], 2))), axis=1)
                #print(raw_data.shape)

                # bandpass filter
                if l_freq == None and h_freq == None:
                    local_timestamps = raw_data[:, 0]
                    raw_eeg_data = np.moveaxis(raw_data[:, 1:5], [0, 1], [1, 0])
                    markers = raw_data[:, 6]
                else:
                    local_timestamps, raw_eeg_data, markers = preprocess_raw(raw_data, l_freq=l_freq, h_freq=h_freq, plot=False)
                
                print("timestamps: ", local_timestamps.shape, ", raw_eeg_data: ", raw_eeg_data.shape, ", markers: ", markers.shape)

                X = raw_eeg_data[:, -srate*2:]
                X = np.expand_dims(X, axis=0)
                for i in range(int(srate/8), srate, int(srate/8)):
                    new_data = raw_eeg_data[:, -srate*2-i:-i]
                    new_data = np.expand_dims(new_data, axis=0)
                    X = np.concatenate((X, new_data), axis=0)
                X = np.array(X)

                if threshold is not None:
                    X = apply_ICA(X, threshold, plot=False)

                # inteference
                Y_hat = clf.predict(X)
                print(Y_hat)
                output = np.zeros((3))
                for i in Y_hat:
                    output[int(i)-1] += 1
                print(np.argmax(output)+1)

                print(time.time())
                time.sleep(1)
                print(time.time())

                # send output
                
    except KeyboardInterrupt:
        stop = True
        print("exiting...")
        collect_thread.join()
