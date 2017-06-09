# feedbackdelay_circbuffer1.py
# Reads a specified wave file (mono) and plays it with a delay with feedback.
# This implementation uses a circular buffer (of minimum
# length) and one buffer index.

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

wavfile = 'the only thing that changes everything.wav'
print("Play the wave file %s." % wavfile)

# Open the wave file
wf = wave.open( wavfile, 'rb')

# Read the wave file properties
num_channels = wf.getnchannels()        # Number of channels
Fs = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()        # Signal length
width = wf.getsampwidth()               # Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % Fs)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)

# Set parameters of delay system
# feed-back gain
b1 = 0.7
b2 = 0.9 
# direct-path gain     
Gdp = 1.0 
# feed-forward gain
a1 = 0.3
a2 = 0.3      
c1 = 0.4
c2 = 0.4       
# Gff = 0.0         # feed-forward gain (set to zero for no effect)

delay_sec = 0.08 # 50 milliseconds
delay_samples = int( math.floor( Fs * delay_sec ) ) 

print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))

# Create a delay line (buffer) to store past values. Initialize to zero.
buffer_length = delay_samples
buffer1 = [ 0 for i in range(buffer_length) ]
buffer2 = [ 0 for i in range(buffer_length) ]    

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 2,
                rate        = Fs,
                input       = False,
                output      = True )

# Get first frame (sample)
input_string = wf.readframes(1)

# Delay line (buffer) index
k = 0

print ("**** Playing ****")

while input_string != '':

    # Convert string to number
    input_value = struct.unpack('hh', input_string)

    # Compute output value
    output_value1 = Gdp * input_value[0] + c1 * buffer1[k]
    output_value2 = Gdp * input_value[1] + c2 * buffer2[k]

    # Update buffer
    buffer1[k] = b1 / c2 * output_value2 - input_value[1] + a1 * input_value[0]
    buffer2[k] = b2 / c1 * output_value1 - input_value[0] + a1 * input_value[1]

    # Increment buffer index
    k = k + 1
    if k == buffer_length:
        # We have reached the end of the buffer. Circle back to front.
        k = 0

    output_value1 = clip16(output_value1)
    output_value2 = clip16(output_value2)
    # Clip output value to 16 bits and convert to binary string
    output_string = struct.pack('hh', output_value1,output_value2)

    # Write output value to audio stream
    stream.write(output_string)

    # Get next frame (sample)
    input_string = wf.readframes(1)     

print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate()
