# Eye_Movement_Detection

## BCI Final Project

### Authors: Ivan Lim, Christian Lin, Aubrey Tseng

## Introduction

This project aims to develop a faster and more efficient way to unlock and control our phones using BCI approach.  <br>
We propose an innovative application that can help you to control your phone by just blinking.  <br>
The eye blinking EEG signals collected by the Muse2 headband are used to train a classifier classifying blinks from right eye and left eye.  <br>
The different blinking EEG signals will be taken as the authentication to the phones and correspond to the different functionalities, like unlocking your phone, playing music. <br>
Therefore, with our application, everyone can unlock their phone in the blink of an eye.
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
`-c` for choosing the classifier (svm or lda) <br>
`-f` for selecting the training subject ("Ivan", "Aubrey", "Christian", "Christian_1", "Rena")
`-s` <br>
`-lf` <br>
`-hf` <br>
`-t` <br>
`-p` <br>
#### example:


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

## Methodology

## Results
