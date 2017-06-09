import pyaudio
import struct
import bound

Fs = 8000
T = 1
N = T * Fs
fs = 400
f = fs / Fs

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                channels = 1,
                rate = Fs,
                input = False,
                output = True,
                frames_per_buffer = 1)

#parameters for differential equation
a1 = -1.8999
a2 = 0.9977
y1 = 0
y2 = 0
k1 = 0
k2 = 0
gain = 46
gain = bound.bound4Order(gain)

#differential equation
for i in range(0,N):
    if i == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    y0 = x0 - a1 * y1 - a2 * y2
    y2 = y1
    y1 = y0

    k0 = y0 - a1 * k1 - a2 * k2
    k2 = k1
    k1 = k0
    
    out = gain * k0
    str_out = struct.pack('h',out)
    stream.write(str_out,1)
print("*** done ***")

stream.stop_stream()
stream.close()
p.terminate()
    
