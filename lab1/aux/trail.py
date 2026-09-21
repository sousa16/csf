import sys, struct
p = sys.argv[1]; b = open(p, 'rb').read(); end = None
if b[:8] == b'\x89PNG\r\n\x1a\n': end = b.rfind(b'IEND') + 8
elif b[:4] == b'RIFF': end = struct.unpack('<I', b[4:8])[0] + 8
elif b[:2] == b'\xff\xd8': end = b.rfind(b'\xff\xd9') + 2
print(p, 'declared_end', end, 'size', len(b), 'trailing', None if end is None else len(b) - end)
if end and len(b) > end: open(p + '.trailer', 'wb').write(b[end:])
