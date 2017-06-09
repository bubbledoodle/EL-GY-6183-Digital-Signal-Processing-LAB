import pyaudio, struct
import wave
import time
import math
from myfunctions import clip16

filename = 'test_vibrato.wav'

RATE = 16000    # sampling rate
CHANNELS = 1    # stereo
WIDTH = 2       # bytes per sample
GAIN = 0.5

# Create a buffer (delay line) for past values
buffer_MAX =  1024                         # Buffer length
buffer = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# Vibrato parameters
f0 = 2
W = 0.2

# Buffer (delay line) indices
n = 0
kr = 0  # read index
kw = int(0.5 * buffer_MAX)      # write index (initialize to middle of buffer)

# Define call back for vibrato effect
def my_callback_fun(input_string, block_size, time_info, status):
    global n, kr, kw

    in_sample = struct.unpack('h'*block_size, input_string)
    output_block = []
    for n in range(0, block_size):
        

        out_sample = buffer[int(kr)]
        buffer[kw] = in_sample[n]

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
        # Note: kr is not integer!

        # Ensure that 0 <= kr < buffer_MAX
        if kr >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr = 0

        # Increment write index    
        kw = kw + 1
        if kw == buffer_MAX:
            # End of buffer. Circle back to front.
            kw = 0

        sample = clip16( GAIN * out_sample )
        output_block.append(sample)


    output_string = struct.pack('h' * block_size, *output_block)
    return (output_string, pyaudio.paContinue)

# Create audio object
p = pyaudio.PyAudio()

# Open stream using callback
stream = p.open(format = pyaudio.paInt16,       # 16 bits/sample
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = 1024,
                stream_callback = my_callback_fun)

stream.start_stream()

print 'The wire will be on for 6 seconds'
# Keep the stream active for 6 seconds by sleeping here
time.sleep(6)

stream.stop_stream()
stream.close()
p.terminate()