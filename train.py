from utils import *

preprocess = True
filenames = ["Ivan.csv", "Aubrey.csv"]
folder_path = "./dataset/"

if __name__ == "__main__":
    Xs, Ys = preprocess_pipeline(filenames, folder_path, l_freq=1, h_freq=100, threshold=None, plot=True)

    train_classifier(Xs["Ivan"], Ys["Ivan"])
    train_classifier(Xs["Aubrey"], Ys["Aubrey"])
    