import sys
print "priori information of my_voice02.wav"
print "channel count: 1"
print "wav sampling rate: 16kHz"
print "wav byte per frame: 2bytes"
str_wavfile_name = "my_voice02.wav"
str_folder_path = sys.path[0]
str_wavfile_path = str_folder_path + "/" + str_wavfile_name
print str_wavfile_path
print "="*40

print "information readed"
import wave
wf = wave.open('my_voice02.wav')
#read the properties of the wav file
num_channel = wf.getnchannels()
fs = wf.getframerate()
length_signal = wf.getnframes()
width = wf.getsampwidth()

print "wav channel count: " + `num_channel`
print "wav sampling rate: " + `fs` + "Hz"
print "wav signal length: " + `length_signal`
print "wav byte per frame: " + `width` +"bytes"
