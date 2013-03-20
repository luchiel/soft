MAX_NUMBER = 255

def encode(reader, fo):
    prev = None
    number = 0
    encoded = bytearray()
    for line in reader:
        for symbol in line:
            if prev != symbol or number == MAX_NUMBER:
                if prev != None:
                    encoded.append(number)
                    encoded.append(prev)
                number = 1
                prev = symbol
            else:
                number += 1
        fo.write(encoded)
        encoded = bytearray()

    if prev != None:
        encoded.append(number)
        encoded.append(prev)
    fo.write(encoded)

def decode(reader, fo):
    for line in reader:
        i = 0
        decoded = ''
        while i < len(line):
            decoded += line[i + 1] * ord(line[i])
            i += 2
        fo.write(decoded)
