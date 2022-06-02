from utils import *

preprocess = True
filename = "Ivan_EEG_recording_2022-05-29-13.06.19.csv"
folder_path = "./dataset/"

if __name__ == "__main__":
    raw_data = import_data(filename, folder_path)
    raw_data = raw_data.to_numpy(copy=True)

    if preprocess == True:
        # bandpass filter (l_freq-h_freq Hz)
        timestamps, raw_eeg_data, markers = preprocess_raw(raw_data, l_freq=1, h_freq=100, plot=True)
    else:
        timestamps = raw_data[:, 0]
        raw_eeg_data = np.moveaxis(raw_data[:, 1:5], [0, 1], [1, 0])
        markers = raw_data[:, 6]
    print("timestamps: ", timestamps.shape, ", raw_eeg_data: ", raw_eeg_data.shape, ", markers: ", markers.shape)

    X, Y = extract_epoch(timestamps, raw_eeg_data, markers)

    # X = ICA(X)
    # visualize_data(X, Y)

    train_classifier(X, Y)
    