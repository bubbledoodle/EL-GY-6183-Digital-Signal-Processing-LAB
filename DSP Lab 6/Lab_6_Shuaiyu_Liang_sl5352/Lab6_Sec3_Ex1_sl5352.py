import pyaudio
import wave
import struct
import math
import time
from myfunctions import clip16
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('roomresponse3.pdf')


wavfile = 'roomresponse.wav'
#PARAMETERS
CHANNELS = 1
RATE = 16000
WAITING_TIME = 30
RECORDING_TIME = 3
WIDTH = 2
BLOCKSIZE = 1024
THRESHOLD = 10000

plt.ion()
plt.figure(1)
plt.ylim(-2**15,2**15)
plt.ylabel('Amplitude')
plt.xlim(0,RECORDING_TIME * RATE)
plt.xlabel('points')
plt.grid(True)
line, =plt.plot([],[],color = 'blue')


waiting_num_blocks = int(math.floor(WAITING_TIME * RATE/BLOCKSIZE))
recording_num_blocks = int(math.floor(RECORDING_TIME * RATE/BLOCKSIZE))
output_block = [0.0 for n in range(0, BLOCKSIZE)]
output_list = []

p = pyaudio.PyAudio()
stream = p.open(format      = p.get_format_from_width(WIDTH),
                channels    = CHANNELS,
                rate        = RATE,
                input       = True,
                output      = True)

for i in range(WAITING_TIME * RATE):
    input_string = stream.read(1)
    input_sig = struct.unpack('h', input_string)
    if input_sig[0] > THRESHOLD:
        print 'Real time signal Amplitude = ',input_sig[0]
        break

print('recording...')
output_wavefile = wavfile
print 'Writing to wave file', output_wavefile
wf = wave.open(output_wavefile, 'w')      # wave file
wf.setnchannels(1)      # one channel (stereo)
wf.setsampwidth(WIDTH)      # two bytes per sample
wf.setframerate(RATE)   # samples per second

for i in range(0, recording_num_blocks):
    input_string = stream.read(BLOCKSIZE)
    input_block = struct.unpack('h' * BLOCKSIZE, input_string)
    for n in range(BLOCKSIZE):
        output_block[n] = clip16(input_block[n])
        output_list.append(output_block[n])
    output_string = struct.pack('h' * BLOCKSIZE, *output_block)
    stream.write(output_string)
    wf.writeframes(output_string)

length = len(output_list)
x = [n for n in range(length)]
line.set_xdata(x)
line.set_ydata(output_list)
plt.draw()
plt.savefig(pp, format='pdf')
pp.close()


stream.stop_stream()
stream.close()
p.terminate()
wf.close()
print('* Done')