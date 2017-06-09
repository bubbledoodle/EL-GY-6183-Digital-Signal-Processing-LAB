# linear interpolation vibrato
# For stereo recorded real time sound
import pyaudio
import wave
import struct
import math
from myfunctions import clip16

wavfile = 'mysound.wav'

# Read wave file properties
CHANNELS = 2              # Number of channels
RATE = 16000              # Sampling rate (frames/second)
RECORD_SECONDS = 5        # Signal length
WIDTH = 2                 # Number of bytes per sample
LEN = RATE * RECORD_SECONDS
BLOCKSIZE = 64
print('The recording has %d channel(s).'         % CHANNELS)
print('The recording has %d frames/second.'      % RATE)
print('The recording has %d frames.'             % LEN)
print('The recording has %d bytes per sample.'   % WIDTH)

# Vibrato parameters
f0 = 4
f1 = 2
W0 = 0.2
W1 = 0
# W = 0 # for no effct

# Create a buffer (delay line) for past values
buffer_MAX =  1024                          # Buffer length
buffer0 = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
buffer1 = [0.0 for i in range(buffer_MAX)]

# Buffer (delay line) indices
kr0 = 0  # read index
kr1 = 0
kw0 = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
kw0 = buffer_MAX/2
kw1 = int(0.5 * buffer_MAX)
kw1 = buffer_MAX/2
# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(buffer_MAX)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = p.get_format_from_width(WIDTH),
                channels    = CHANNELS,
                rate        = RATE,
                input       = True,
                output      = True )

# output parameters
GAIN0 = 1
GAIN1 = 0.5
output_block = [0 for i in range(0,BLOCKSIZE * 2)] #initializing output_block
#output_all = ''            # output signal in all (string)

print ('* recording & playing...')
num_blocks = int(LEN / BLOCKSIZE)

# Loop through
for n in range(0, num_blocks):

    # Get sample from wave file
    input_string = stream.read(BLOCKSIZE)

    # Convert string to number
    input_tuple = struct.unpack('hh' * BLOCKSIZE, input_string)

    for i in range(0, BLOCKSIZE):

        # Get previous and next buffer values (since kr is fractional)
        kr_prev0 = int(math.floor(kr0))               
        kr_next0 = kr_prev0 + 1
        frac0 = kr0 - kr_prev0    # 0 <= frac < 1
        if kr_next0 >= buffer_MAX:
            kr_next0 = kr_next0 - buffer_MAX

        kr_prev1 = int(math.floor(kr1))               
        kr_next1 = kr_prev1 + 1
        frac1 = kr1 - kr_prev1    # 0 <= frac < 1
        if kr_next1 >= buffer_MAX:
            kr_next1 = kr_next1 - buffer_MAX

        # Compute output value using interpolation
        output_block[2*i] = (1-frac0) * buffer0[kr_prev0] + frac0 * buffer0[kr_next0]
        output_block[2*i+1] = (1-frac1) * buffer1[kr_prev1] + frac1 * buffer1[kr_next1]
        output_block[2*i] = clip16(GAIN0 * output_block[2*i])
        output_block[2*i+1] = clip16(GAIN1 * output_block[2*i+1]) #bounded

        # Update buffer (pure delay)
        buffer0[kw0] = input_tuple[2*i]
        buffer1[kw1] = input_tuple[2*i+1]

        # Increment read index
        kr0 = kr0 + 1 + W0 * math.sin( 2 * math.pi * f0 * i / RATE )
        kr1 = kr1 + 1 + W1 * math.sin( 2 * math.pi * f1 * i / RATE )
            # Note: kr is fractional (not integer!)

        # Ensure that 0 <= kr < buffer_MAX
        if kr0 >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr0 = 0
        if kr1 >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr1 = 0

        # Increment write index

        if kw0 == buffer_MAX:
            # End of buffer. Circle back to front.
            kw0 = 0
        if kw1 == buffer_MAX:
            # End of buffer. Circle back to front.
            kw1 = 0
            
    # Clip and convert output value to binary string
    output_string = struct.pack('hh' * BLOCKSIZE, *output_block)

    # Write output to audio stream
    stream.write(output_string)

    #output_all = output_all + output_string     # append new to total

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()

output_wavefile = wavfile[:-4] + '_vibrato.wav'
print 'Writing to wave file', output_wavefile
wf = wave.open(output_wavefile, 'w')      # wave file
wf.setnchannels(2)      # one channel (stereo)
wf.setsampwidth(WIDTH)      # two bytes per sample
wf.setframerate(RATE)   # samples per second
#wf.writeframes(output_all)
wf.close()
print('* Done')