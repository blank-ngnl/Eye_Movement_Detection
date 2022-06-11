# Eye_Movement_Detection

## BCI Final Project - EyeLocker

### Authors: Ivan Lim, Christian Lin, Aubrey Tseng
![image](https://user-images.githubusercontent.com/58105978/173184062-202193c5-e286-4e19-854b-d35a3723960b.png)
<br>

## Introduction

This project aims to develop a faster and more efficient way to unlock and control our phones using BCI approach.  <br>
We propose an innovative application that can help you to control your phone by just blinking.  <br>
The eye blinking EEG signals collected by the Muse2 headband are used to train a classifier classifying blinks from right eye and left eye.  <br>
The different blinking EEG signals will be taken as the authentication to the phones and correspond to the different functionalities, like unlocking your phone, playing music, etc. <br>
With our application, everyone can unlock their phone in the blink of an eye.
 <br>
## Video Demo

https://user-images.githubusercontent.com/58105978/173186608-ba85f494-63dc-41ab-bd9f-6de6fa5950fe.mp4



## Application (now supported in iOS)
For the iOS EyeLocker app code, you can refer to the EyeLocker github page: https://github.com/ChristianLin0420/EyeLocker<br>
When the code, app and the Muse2 headband are all connected, the classifier will start predicting the EEG signal sent from the Muse2 headband. <br>
Then, the output prediction: **1: blink right eye**, **2: blink left eye**, **3: idle** will be sent as the classified command to control the app. <br>
Here, we develop some functionalities including unlocking the app, play/pause and replay the music. <br>
`1: blink right eye`: unlocking the app, play and pause the music <br>
`2: blink left eye`: replay the music <br>

## Installation instructions

#### Installing dependencies:

```shell
conda create -n bci python=3.9
conda activate bci
pip install -r requirements.txt
```

After installing, comment out the ```await asyncio.wait_for(event.wait(), timeout=timeout)``` line to avoid TimeoutError. 
Line 268 in anaconda3/envs/bci/Lib/site-packages/bleak/backends/winrt/client.py.

## Dataset

The data is collected from 4 subjects using the Muse2 headband with the experimental paradigm is shown below. <br>
We record 150 trials for each subject, and each event (blink left eye, blink right eye, idle) consists of 50 trials. <br>
The time of the red and blue screen presented on the screen is fixed, and the duration is set to 0.5 seconds, 
while the idle time is set to 2 seconds. <br>
The order in which these events appeared on the screen is random, this means there is no regular pattern, so the subject needs to be highly concentrated during the whole experiment. <br>
As shown in the table below, each arrow represents an event, and there is an idle period for the subject to recover before and after each event because the blinking eye is quite tiring if it is performed frequently. <br>
![image](https://user-images.githubusercontent.com/58105978/173168116-ed4e7b76-a9ea-4c19-a907-9cebe13b99d4.png) <br>
The experiment is designed requiring the participant to sit in front of a monitor and perform eye blinking movements according to the screen’s colour. <br>
The participant is asked to blink his left eye once if the colour red is shown on the screen and blink his right eye once if the colour is blue while remaining idle if the black colour is displayed. <br>
We recorded the EEG sinals of 4 channels: "TP9", "AF7", "AF8", "TP10" with 3 markers: "Blink right eye", "Blink left eye", "idle". <br>
First, use `startmusestream.py` in the `record` folder to connect to the muse headband, then, call `record.py` to record the EEG signal raw data and save them in the csv file format including the timestamps, the 4 channels and the markers. <br>

## Methodology

### EEG Preprocessing

#### Bandpass Filtering
We apply bandpass filter to the EEG signal with low pass and high pass frequency set to 1 to 100 HZ, which can keep the signal data in this frequency range and prevent the noise outside this range. <br>
(The lower and higher cutoff frequency can both be adjustd in `train.py` and `test.py`.) <br>
#### Extract Epoch from Raw Data
The raw data is then extracted according to the 3 events (blink left eye, blink right eye, idle), <br> we extract epoch data 0.25s before the event and 1.75s after the event. <br>
#### Independent Component Analysis (ICA)
We also use ICA to try to extract the independent sources signals (the blinking eog artifact) from the mixed EEG signal data. <br>
The channel AF7 and AF8 are taken as the reference. <br> The lower threshold data will be kept because they are similar to the eog artifact (AF7 and AF8). <br>
The higher threshold data is not taken as the eog artifact and it will reject more component, and the matrix is set to 0 during inverse.

### Feature Extraction

#### Common Spatial Patterns (CSP)
The Common Spatial Patterns (CSP) is a supervised feature extraction method, it uses spatial filters to optimise the variance-ratio and maximize the discriminability of classes. The use of CSP can help to enhance the spatial resolution of EEG. <br>
We only apply CSP with LDA classifier.

### Classifier
In order to classify between the EEG of blinking right eye, left eye and idle. <br>
We train the processed EEG on different classifiers including Support Vector Machine (SVM) and Linear Discriminant Analysis (LDA), and evaluate their performances in accuracy.  

#### Support Vector Machine (SVM)
We first apply SVM to classify the EEG data, and try to find the maximum marginal hyperplane (MMH) that best divides the EEG data into classes.

#### Linear Discriminant Analysis (LDA)
Another approach of our BCI system is Linear Discriminant Analysis (LDA). <br>
LDA is not only a dimensionality reduction technique, but also a commonly used classification algorithm. <br>
Graphically, LDA can insert a hyperplane into the n-dimensional feature space with the aim of separating the means of the point clusters of each class. <br>

## Results

In this section, we show the classification accuracies on subjects' own testing set, inter-subject and general classifier with 3 subjects.<br>
The stratified train test split is used to divide out the testing set of each subject. We set 80% of the data as the training set and 20% as the testing set. <br>
### Subject
The accuracies of three subjects separately train on SVM and CSP+LDA, and test on their own testing set are shown below: <br>
Subject | Ivan | Aubrey | Chritian
--- | --- | --- | ---
CSP+LDA | 1.00  | 0.93 | 0.87
SVM | 0.97 | 0.97 | 0.83

### Inter-Subject
The inter-subject performance is also evaluated. <br>
We train the LDA classifier using Aubrey's and Ivan's data, respectively. Then, use the 2 classifiers to test on Chritian's data. <br>
Training | Testing | Classifier | Accuracy
--- | --- | --- | ---
Aubrey | Christian  | LDA | 0.7266
Ivan | Christian | LDA | 0.6466

### General Classifier
Lastly, we take the training set (80% of each subject's data) of the 3 subjects to train a general classifier, and test it on their testing set together. <br>
General Classifier | Ivan + Ivan_1 + Aubrey | Ivan + Christian + Aubrey
--- | --- | --- 
SVM | 0.9555 | 0.7555
LDA | 0.9333 | 0.8222

## Quick Start

### Training
You can run the training code with:
```shell 
python train.py
```
#### Parameters for train.py
`-c` for choosing the classifier (svm or lda, default: lda) <br>
`-f` for selecting the training subject ("Ivan", "Ivan_1", "Aubrey", "Christian", "Christian_1", "Rena", default: Ivan) <br>
`-s` for selecting the testing subject ("Ivan", "Ivan_1", "Aubrey", "Christian", "Christian_1", "Rena", default: `None`)<br>
`-lf` for setting the lower cutoff frequency (default: 1) <br>
`-hf` for setting the higher cutoff frequency (default: 100)<br>
`-t` for setting the ICA threshold (default: `None`)<br>
`-p` for plotting the five subjects' raw and bandpass filtered data (also plotting the component if the ICA was set) <br>

### Testing
You can run the testing (predict) code with:
```shell 
python test.py
```
#### Parameters for `test.py`
`-c` for choosing the classifier (svm or lda, default: lda) <br>
`-s` for selecting the testing subject ("Ivan", "Ivan_1", "Aubrey", "Christian", "All", default: `None`)<br>
`-lf` for setting the lower cutoff frequency (default: 1) <br>
`-hf` for setting the higher cutoff frequency (default: 100)<br>
`-t` for setting the ICA threshold (default: `None`)<br>
