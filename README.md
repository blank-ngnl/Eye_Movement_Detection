# Eye_Movement_Detection

## BCI Final Project - EyeLocker

### Authors: Ivan Lim, Christian Lin, Aubrey Tseng

<br>

## Introduction
This project aims to develop a faster and more efficient way to unlock and control our phones using BCI approach.  <br>
We propose an innovative application that can help you to control your phone by just blinking.  <br>
The eye blinking EEG signals collected by the Muse2 headband are used to train a classifier classifying blinks from right eye and left eye.  <br>
The different blinking EEG signals will be taken as the authentication to the phones and correspond to the different functionalities, like unlocking your phone, playing music, etc. <br>
With our application, everyone can unlock their phone in the blink of an eye.
 <br>
## Video Demo

## Quick Start
### Application (now first supported in ios)

### Training
You can run the training code with:
```shell 
python train.py
```
#### Parameters for train.py
`-c` for choosing the classifier (svm or lda, default: lda) <br>
`-f` for selecting the training subject ("Ivan", "Aubrey", "Christian", "Christian_1", "Rena", default: Ivan) <br>
`-s` for selecting the testing subject ("Ivan", "Aubrey", "Christian", "Christian_1", "Rena", default: `None`)<br>
`-lf` for setting the lower cutoff frequency (default: 1) <br>
`-hf` for setting the higher cutoff frequency (default: 100)<br>
`-t` for setting the ICA threshold (default: `None`)<br>
`-p` for plotting the five subjects' raw and bandpass filtered data (also plotting the component if the ICA was set) <br>

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
The data is collected from 4 subjects using the Muse2 headband (channels: "TP9", "AF7", "AF8", "TP10") with the experimental paradigm is shown below. <br>
We record 150 trials for each subject, and each event (blink left eye, blink right eye, idle) consists of 50 trials. <br>
The time of the red and blue screen presented on the screen is fixed, and the duration is set to 0.5 seconds, 
while the idle time is set between 1.5 seconds and 2.5 seconds. <br>
The order in which these events appeared on the screen is random, this means there is no regular pattern, so the subject needs to be highly concentrated during the whole experiment. <br>
As shown in the table below, each arrow represents an event, and there is an idle period for the subject to recover before and after each event because the blinking eye is quite tiring if it is performed frequently. <br>
![image](https://user-images.githubusercontent.com/58105978/172196351-78588c07-7da3-42a0-8302-0191aef7e923.png) <br>
The experiment is designed requiring the participant to sit in front of a monitor and perform eye blinking movements according to the screen’s colour. <br>
The participant is asked to blink his left eye once if the colour red is shown on the screen and blink his right eye once if the colour is blue while remaining idle if the black colour is displayed. <br>
We recorded the EEG sinals of 4 channels: "TP9", "AF7", "AF8", "TP10" with 3 markers: "Blink right eye", "Blink left eye", "idle". <br>
The EEG data is saved in the csv file format including the timestamps, the 4 channels and the markers. <br>

## Methodology

### EEG Preprocessing

#### Bandpass Filtering

#### Extract Epoch from Raw Data

#### Independent Component Analysis (ICA)

### Feature Extraction

#### Common Spatial Patterns

### Classifier

#### SVM

#### Linear Discriminant Analysis (LDA)

## Results
