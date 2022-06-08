from utils import *
import sys
import argparse

filenames = ["Ivan.csv", "Ivan_1.csv", "Aubrey.csv"]
folder_path = "./dataset/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="eye movement detection")
    parser.add_argument("-c", "--classifier", default="lda", choices=["svm", "lda"], help="select a classifier")
    parser.add_argument("-s", "--subject", default="Ivan", choices=["Ivan", "Ivan_1", "Aubrey", "All"], help="select the subject")
    parser.add_argument("-lf", "--l_freq", default=1, help="set a value for the lower cutoff frequency", type=int)
    parser.add_argument("-hf", "--h_freq", default=100, help="set a value for the upper cutoff frequency", type=int)
    parser.add_argument("-t", "--threshold", default=None, help="set a value for the ICA threshold", type=float)
    args = parser.parse_args()

    Xs, Ys = preprocess_pipeline(filenames, folder_path, l_freq=args.l_freq, h_freq=args.h_freq, threshold=args.threshold, plot=False)

    classifier = test_classifier(Xs, Ys, args.subject, classifier=args.classifier)

    inference(classifier, args.l_freq, args.h_freq, args.threshold)
    

    