from mne.decoding import CSP
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

class my_clf():
    def __init__(self, classifier):
        if classifier == "svm":
            self.clf = my_svm()
        elif classifier == "lda":
            self.clf = my_lda()
    
    def fit(self, X_train, Y_train):
        self.clf.fit(X_train, Y_train)
    
    def predict(self, X_test):
        return self.clf.predict(X_test)

class my_svm():
    def __init__(self):
        self.clf = make_pipeline(StandardScaler(), SVC(kernel='linear', gamma='auto'))

    def fit(self, X_train, Y_train):
        X_train = X_train.reshape(X_train.shape[0], -1)
        self.clf.fit(X_train, Y_train)
    
    def predict(self, X_test):
        X_test = X_test.reshape(X_test.shape[0], -1)
        return self.clf.predict(X_test)

class my_lda():
    def __init__(self):
        self.csp_decoding = CSP(n_components=4)
        self.std_scaler = StandardScaler()
        self.lda_clf = LinearDiscriminantAnalysis()
    
    def fit(self, X_train, Y_train):
        X_train = self.csp_decoding.fit_transform(X_train, Y_train)
        X_train = X_train.reshape(X_train.shape[0], -1)
        X_train = self.std_scaler.fit_transform(X_train)
        self.lda_clf.fit(X_train, Y_train)
    
    def predict(self, X_test):
        X_test = self.csp_decoding.transform(X_test)
        X_test = X_test.reshape(X_test.shape[0], -1)
        X_test = self.std_scaler.transform(X_test)
        return self.lda_clf.predict(X_test)