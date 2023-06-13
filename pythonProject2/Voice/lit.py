import tensorflow as tf
import numpy as np
import os
import glob
import pickle
import pyaudio
import time
from numpy import genfromtxt
from keras import backend as K
from keras.models import load_model
import sys

import util
import utils
from username import voice_label

K.set_image_data_format('channels_first')
# np.set_printoptions(threshold=np.nan)
np.set_printoptions(threshold=sys.maxsize)

import pyaudio
from IPython.display import Audio, display, clear_output
import wave
from scipy.io.wavfile import read

from sklearn.mixture import GaussianMixture as GMM
# from sklearn.mixture import GMM
# from sklearn import mixture

import warnings

warnings.filterwarnings("ignore")

from sklearn import preprocessing
# for converting audio to mfcc
import python_speech_features as mfcc


def calculate_delta(array):
    rows, cols = array.shape
    deltas = np.zeros((rows, 20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i - j < 0:
                first = 0
            else:
                first = i - j
            if i + j > rows - 1:
                second = rows - 1
            else:
                second = i + j
            index.append((second, first))
            j += 1
        deltas[i] = (array[index[0][0]] - array[index[0][1]] + (2 * (array[index[1][0]] - array[index[1][1]]))) / 10
    return deltas


# convert audio to mfcc features
def extract_features(audio, rate):
    mfcc_feat = mfcc.mfcc(audio, rate, 0.025, 0.01, 20, appendEnergy=True, nfft=1400)
    mfcc_feat = preprocessing.scale(mfcc_feat)
    delta = calculate_delta(mfcc_feat)

    # combining both mfcc features and delta
    combined = np.hstack((mfcc_feat, delta))
    return combined


def add_user():

    with open('variable_value.pickle', 'rb') as f:
        name = str(pickle.load(f))


    # check for existing database
    if os.path.exists('./voice_database/embeddings.pickle'):
        with open('./voice_database/embeddings.pickle', 'rb') as database:
            db = pickle.load(database)

            if name in db:
                print("Name Already Exists! Try Another Name...")
                return
    else:
        # if database not exists than creating new database
        db = {}

    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 10

    source = "C:\\Users\\swaro\\PycharmProjects\\pythonProject2\\Voice\\voice_database\\" + name

    os.mkdir(source)
    util.msg("Note", "Speak your Aadhar number after 3 seconds and also system will ask you 3 times to record your voice")
    for i in range(3):
        audio = pyaudio.PyAudio()

        if i == 0:
            j = 3
            while j >= 0:
                time.sleep(1.0)
                # print("Speak your Aadhar number in {} seconds".format(j))
                clear_output(wait=True)

                j -= 1


        elif i == 1:
            print("One more time")
            util.msg("Note", "One more time... Click OK to continue")
            time.sleep(0.5)

        else:
            print("One last time")
            util.msg("Note", "One last time... Click OK to continue")
            time.sleep(0.5)

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        print("Recording...")

        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # saving wav file of speaker
        waveFile = wave.open(source + '/' + str((i + 1)) + '.wav', 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        print("Done")

    dest = "C:\\Users\\swaro\\PycharmProjects\\pythonProject2\\Voice\\gmm_models\\"
    count = 1

    for path in os.listdir(source):
        path = os.path.join(source, path)

        features = np.array([])

        # reading audio files of speaker
        (sr, audio) = read(path)

        # extract 40 dimensional MFCC & delta MFCC features
        vector = extract_features(audio, sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))

        # when features of 3 files of speaker are concatenated, then do model training
        if count == 3:
            gmm = GMM(n_components=16, max_iter=200, covariance_type='diag', n_init=33)
            gmm.fit(features)

            # saving the trained gaussian model
            pickle.dump(gmm, open(dest + name + '.GMM', 'wb'))
            util.msg("Note", "Voice registration completed")
            print(name + ' added successfully')

            features = np.asarray(())
            count = 0
        count = count + 1


# name = 'unknown_test'
# dest = "C:\\Users\\swaro\\PycharmProjects\\pythonProject2\\Voice\\gmm_models\\"
# count = 1
# source = "C:\\Users\\swaro\\PycharmProjects\\pythonProject2\\Voice\\voice_database\\" + name
#
#
# for path in os.listdir(source):
#     path = os.path.join(source, path)
#
#     features = np.array([])
#
#     # reading audio files of speaker
#     (sr, audio) = read(path)
#
#     # extract 40 dimensional MFCC & delta MFCC features
#     vector = extract_features(audio, sr)
#
#     if features.size == 0:
#         features = vector
#     else:
#         features = np.vstack((features, vector))
#
#     # when features of 3 files of speaker are concatenated, then do model training
#     if count == 33:
#         gmm = GMM(n_components=16, max_iter=200, covariance_type='diag', n_init=33)
#         gmm.fit(features)
#         print('*')
#
#         # saving the trained gaussian model
#
#         pickle.dump(gmm, open(dest + name + '.GMM', 'wb'))
#         print(name + ' added successfully')
#
#         features = np.asarray(())
#         count = 0
#     count = count + 1


def recognize():
    # Voice Authentication
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 10
    FILENAME = "./test.wav"
    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    util.msg("Note", "Recording... Click OK to continue")
    print("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    util.msg("Note", "Finished Recording... Click OK to continue")
    print("finished recording")
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # saving wav file
    waveFile = wave.open(FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    modelpath = "C:\\Users\\swaro\\PycharmProjects\\pythonProject2\\Voice\\gmm_models\\"
    gmm_files = [os.path.join(modelpath, fname) for fname in
                 os.listdir(modelpath) if fname.endswith('.GMM')]
    models = [pickle.load(open(fname, 'rb')) for fname in gmm_files]
    speakers = [fname.split("/")[-1].split(".GMM")[0] for fname
                in gmm_files]

    if len(models) == 0:
        print("No Users Authorized!")
        return

    # read test file
    sr, audio = read(FILENAME)
    # extract mfcc features
    vector = extract_features(audio, sr)
    log_likelihood = np.zeros(len(models))
    # checking with each model one by one
    for i in range(len(models)):
        gmm = models[i]
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()

    pred = np.argmax(log_likelihood)

    identity = speakers[pred]
    print(identity[63:])
    # voice_iden=identity[-7:]
    # with open('variable_value.pickle', 'wb') as f:
    #     pickle.dump(voice_iden, f)
    # if voice not recognized than terminate the process
    #     print(speakers)
    if identity == 'unknown_test' and 'unknown':
        print("Not Recognized! Try again...")
    elif identity == 'blank':
        print("No voice detected!")
    else:
        utils.msg_box("Note","Voice Recognized as {}".format(identity[63:]))
        print("Recognized as - ", identity[63:])