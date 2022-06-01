import pandas as pd

def import_data(filename, path):
    data = pd.read_csv(path + filename)
    return data

def extract_epoch(raw_data):
    srate = 256
    markers = {
        'Left': 1,
        'Right': 2,
        'Idle': 3,
        'Rest': 4, # not marker
        'Start': 99,
        'End': 100
    }
    selected_channels = ["TP9", "AF7", "AF8", "TP10"]
    duration = [-0.25, 1.75]

    X = []
    Y = []
    count = 0
    events = raw_data["Marker0"]
    for i, event in enumerate(events):
        if event == markers["Right"]:
            new_trial = []
            for channel in selected_channels:
                new_trial = raw_data[channel][i+duration[0]*srate:i+duration[1]*srate]

if __name__ == "__main__":
    raw_data = import_data("Ivan_EEG_recording_2022-05-29-13.06.19.csv", "./record/")
    extract_epoch(raw_data)