import sounddevice as sd
import numpy as np
import wave
import math
import pyaudio
import random

#clan names
DARK_FOREST = "dark_forest"
SHADOW_CLAN = "shadow_clan"
SKY_CLAN = "sky_clan"
WIND_CLAN = "wind_clan"
RIVER_CLAN = "river_clan"
THUNDER_CLAN = "thunder_clan"

class Sorting_Hat:
    """
    a sorting hat but for warrior cats
    """

    def __init__(self) -> None:
        self.names_order = 0
        self.proof = self.record2array()
        self.names = list(range(52))
        random.shuffle(self.names)

    def not_rand_proof(self):
        """
        this is proof that the sorting is not random
        """
        sorted_clan = self.number2clan(self.array2number(self.proof))
        print(sorted_clan)

    def record2array(self, duration=3):
        """
        records audio in 5 second segments and turns it into an array using
        framerate of 44100

        Input: duration int the duration of the audio recording in seconds
        returns np array
        """
        #44100 is a common framerate
        fs = 44100
        meow = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
        print("recording audio")
        sd.wait()
        print("finished recording audio")

        return meow
    
    def array2number(self, sound_arr):
        """
        calculates a consitent number given the sound array I think its based
        off of loudness and frequency

        Input
            sound_arr (np.array)

        Returns int a numerber reflecting the array
        """
        mean = np.mean(sound_arr)
        mean = mean * 1000000
        print(mean)
        return mean
    
    def number2clan(self, num):
        """
        takes a number and gives a clan from quietess shadow clan, sky clan, 
        wind clan, river clan, thunderclan. In human levels will be darkforest
        and bloodclan

        Input num (int): a number

        return (str) the clan associated
        """
        if num < -200:
            return DARK_FOREST
        elif num < -15:
            return SHADOW_CLAN
        elif num < 0:
            return SKY_CLAN
        elif num < 20:
            return WIND_CLAN
        elif num < 30:
            return RIVER_CLAN
        elif num > 30:
            return THUNDER_CLAN

    def sort(self, duration=3):
        """
        calls function to sort a person into a warrior clan based on a recording
        of the meow is to be used during the showcase also gives the person
        a warrior cat name. i++ the name attribute so that people don't get
        the same name twice

        Input:
            duration (int): the duration of meow in seconds

        Returns None
        """
        special_number = self.array2number(self.record2array())
        sorted_clan = self.number2clan(special_number)

        #inbetween random
        rand_inbetween()
        #clan recording
        play_clan(sorted_clan)
        #name
        play("recordings/name_is.wav")
        self.play_name()
        self.names_order += 1
        if self.names_order > 52:
            self.names_order = 0

    def play_name(self):
        """
        plays name of cat based off of the number in names irder
        """
        play("recordings/names/n" + str(self.names[self.names_order]) + ".wav")

def rand_inbetween():
    """
    """
    num = random.randint(0, 9)
    play("recordings/inbetweens/rec" + str(num) + ".wav")

def play_clan(clan):
    """
    """
    if clan == SHADOW_CLAN:
        play("recordings/clans/" + SHADOW_CLAN + ".wav")
    elif clan == SKY_CLAN:
        play("recordings/clans/" + SKY_CLAN + ".wav")
    elif clan == WIND_CLAN:
        play("recordings/clans/" + WIND_CLAN + ".wav")
    elif clan == RIVER_CLAN:
        play("recordings/clans/" + RIVER_CLAN + ".wav")
    elif clan == THUNDER_CLAN:
        play("recordings/clans/" + THUNDER_CLAN + ".wav")

#non class code
def play(filename):
    """
    """
    chunk = 1024
    # Open the WAV file
    f = wave.open(filename, "rb")

    # Initialize PyAudio
    p = pyaudio.PyAudio() 

    # Open a new audio stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)

    #read data  
    data = f.readframes(chunk)

    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()