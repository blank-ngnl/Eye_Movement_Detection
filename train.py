from utils import *
import sys
import argparse

preprocess = True
filenames = ["Ivan.csv", "Aubrey.csv", "Christian.csv", "Christian_1.csv", "Rena.csv"]
folder_path = "./dataset/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="eye movement detection")
    parser.add_argument("-c", "--classifier", default="lda", choices=["svm", "lda"], help="select a classifier")
    parser.add_argument("-f", "--first_subject", default="Ivan", choices=["Ivan", "Aubrey", "Christian", "Christian_1", "Rena"], help="select the first subject")
    parser.add_argument("-s", "--second_subject", default=None, choices=["Ivan", "Aubrey", "Christian", "Christian_1", "Rena"], help="select the second subject")
    parser.add_argument("-lf", "--l_freq", default=1, help="set a value for the lower cutoff frequency", type=int)
    parser.add_argument("-hf", "--h_freq", default=100, help="set a value for the upper cutoff frequency", type=int)
    parser.add_argument("-t", "--threshold", default=None, help="set a value for the ICA threshold", type=float)
    parser.add_argument("-p", "--plot", help="plot data", action="store_true")
    args = parser.parse_args()

    Xs, Ys = preprocess_pipeline(filenames, folder_path, l_freq=args.l_freq, h_freq=args.h_freq, threshold=args.threshold, plot=args.plot)

    if args.second_subject == None:
        train_classifier(Xs[args.first_subject], Ys[args.first_subject], classifier=args.classifier)
    else:
        train_classifer_cross_subject(Xs, Ys, args.first_subject, args.second_subject, classifier=args.classifier) 

    