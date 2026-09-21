import sys, wave
w = wave.open(sys.argv[1], 'rb'); sw = w.getsampwidth(); raw = w.readframes(w.getnframes())
bits = [x & 1 for x in raw[0::sw]]
def pack(bits, msb):
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        byte = bits[i:i+8] if msb else bits[i:i+8][::-1]
        v = 0
        for x in byte: v = (v << 1) | x
        out.append(v)
    return bytes(out)
for msb in (True, False):
    d = pack(bits, msb); print('MSB' if msb else 'LSBfirst', d[:100])
    open('lsb_%s.bin' % ('msb' if msb else 'lsbfirst'), 'wb').write(d)
