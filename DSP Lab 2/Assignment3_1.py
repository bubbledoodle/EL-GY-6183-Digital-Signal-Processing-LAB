import pyaudio
import struct

WIDTH = 1
print pyaudio.paInt8
print pyaudio.get_format_from_width(WIDTH)
sl = struct.pack('i',-1);
print `sl`
