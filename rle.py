MAX_NUMBER = 255

def encode(reader):
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
    if prev != None:
        encoded.append(number)
        encoded.append(prev)
    return encoded

def decode(reader):
    decoded = ''
    for line in reader:
        i = 0
        while i < len(line):
            decoded += ''.join([line[i + 1]] * ord(line[i]))
            i += 2
    return decoded
