import pygame
from pylsl import StreamInfo, StreamOutlet, resolve_byprop
from muselsl import record
import numpy as np
from datetime import datetime
import time
from threading import Thread

LSL_SCAN_TIMEOUT = 5

def start_record():
    record(600)

    # Note: Recording is synchronous, so code here will not execute until the stream has been closed
    print('Recording has ended')

def game_init():
    # Initializing Pygame
    pygame.init()

    # Initializing window
    window = pygame.display.set_mode()

    # get the size of the window or screen
    window_size = pygame.display.get_window_size()

    # Setting name for window
    pygame.display.set_caption('BCI Final Project')

    # create a font object.
    # 1st parameter is the font file which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 128)

    text = []
    textRect = []

    # create a text surface object, on which text is drawn on it.
    text.append(font.render("Ready", True, "black", "white"))
    text.append(font.render("Press Enter to Start", True, "black", "white"))
    text.append(font.render("Can't find EEG stream.", True, "black", "white"))
    text.append(font.render("Finding Streams", True, "black", "white"))

    # create a rectangular object for the text surface object
    textRect.append(text[0].get_rect())
    textRect.append(text[1].get_rect())
    textRect.append(text[2].get_rect())
    textRect.append(text[3].get_rect())

    # set the center of the rectangular object.
    textRect[0].center = (window_size[0] // 2, window_size[1] // 2 - 64)
    textRect[1].center = (window_size[0] // 2, window_size[1] // 2 + 64)
    textRect[2].center = (window_size[0] // 2, window_size[1] // 2)
    textRect[3].center = (window_size[0] // 2, window_size[1] // 2)
    
    # Changing surface color
    window.fill("white")

    # copying the text surface object to the display surface object at the center coordinate.
    window.blit(text[3], textRect[3])
    pygame.display.flip()

    streams = resolve_byprop('type', "EEG", timeout=LSL_SCAN_TIMEOUT)

    if len(streams) == 0:
        print("Can't find %s stream." % ("EEG"))
        flag = False
        window.fill("white")
        window.blit(text[2], textRect[2])
        pygame.display.flip()
    else:
        flag = True
        window.fill("white")
        window.blit(text[0], textRect[0])
        window.blit(text[1], textRect[1])
        pygame.display.flip()

    return window, flag

def game_start(window):
    # Set up LabStreamingLayer stream.
    info = StreamInfo(name='Markers', type='Markers', channel_count=1,
                  channel_format='int32', source_id='myuidw43536')
    outlet = StreamOutlet(info)  # Broadcast the stream.
    pygame.time.delay(5000)

    # Note: an existing Muse LSL stream is required
    record_thread = Thread(target=start_record)
    record_thread.start()
    pygame.time.delay(5000)

    window_size = pygame.display.get_window_size()

    font = pygame.font.Font('freesansbold.ttf', 128)
    text = {}
    textRect = {}
    text["Start"] = font.render("Start", True, "black", "white")
    text["Left"] = font.render("Left", True, "white", "red")
    text["Right"] = font.render("Right", True, "white", "blue")
    text["Idle"] = font.render("Idle", True, "white", "black")
    text["Rest"] = font.render("Rest", True, "white", "black")
    text["End"] = font.render("End", True, "black", "white")
    
    for key, value in text.items():
        textRect[key] = text[key].get_rect()
        textRect[key].center = (window_size[0] // 2, window_size[1] // 2)

    markers = {
        'Left': 1,
        'Right': 2,
        'Idle': 3,
        'Rest': 4, # not marker
        'Start': 99,
        'End': 100
    }
    sequence = np.concatenate((np.ones(50) * 1, np.ones(50) * 2, np.ones(50) * 3), axis=0)
    np.random.shuffle(sequence)
    sequence = np.concatenate((np.ones(1) * 99, sequence, np.ones(1) * 100), axis=0)
    rest = np.ones_like(sequence) * 4
    sequence = np.concatenate((np.expand_dims(sequence, 1), np.expand_dims(rest, 1)), 1)
    sequence = np.reshape(sequence, -1)
    sequence = sequence[:-1]
    #print(sequence)

    for event in sequence:
        #print(time.time())
        if event == markers["Left"]:
            window.fill("red")
            window.blit(text["Left"], textRect["Left"])
            pygame.display.flip()
            outlet.push_sample([markers["Left"]], time.time())
            pygame.time.delay(500)
        elif event == markers["Right"]:
            window.fill("blue")
            window.blit(text["Right"], textRect["Right"])
            pygame.display.flip()
            outlet.push_sample([markers["Right"]], time.time())
            pygame.time.delay(500)
        elif event == markers["Idle"]:
            window.fill("black")
            window.blit(text["Idle"], textRect["Idle"])
            pygame.display.flip()
            outlet.push_sample([markers["Idle"]], time.time())
            pygame.time.delay(2000)
        elif event == markers["Start"]:
            window.fill("white")
            window.blit(text["Start"], textRect["Start"])
            pygame.display.flip()
            outlet.push_sample([markers["Start"]], time.time())
            pygame.time.delay(2000)
        elif event == markers["End"]:
            window.fill("white")
            window.blit(text["End"], textRect["End"])
            pygame.display.flip()
            outlet.push_sample([markers["End"]], time.time())
            pygame.time.delay(2000)
        elif event == markers["Rest"]:
            window.fill("black")
            window.blit(text["Rest"], textRect["Rest"])
            pygame.display.flip()
            pygame.time.delay(2000)

    record_thread.join()