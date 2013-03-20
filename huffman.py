from collections import Counter

class Node(object):
    def __init__(self, parent):
        self.left = None
        self.right = None
        self.parent = parent
        self.value = None

def add_code(line, s, code):
    for symbol in line:
        s[symbol] = code + s[symbol] if symbol in s else code

def binary_code(symbol):
    s = bin(ord(symbol))[2:]
    if len(s) < 8:
        s = '0' * (8 - len(s)) + s
    return s

def encode(reader, fo):
    c = Counter()
    for line in reader:
        c += Counter(line)
    if c == {}:
        return ''

    l = sorted(zip(c.values(), c.keys()))
    l = map(lambda x: (x[0], x[1], '1' + binary_code(x[1])), l)
    s = {}

    if len(l) == 1:
        add_code(l[0], s, '0')

    while len(l) > 1:
        (n2, s2, t2) = l.pop(0)
        (n1, s1, t1) = l.pop(0)
        add_code(s1, s, '0')
        add_code(s2, s, '1')
        l.append((n1 + n2, s1 + s2, '0' + t1 + t2))
        l.sort()

    encoded = ''
    reader.reset()
    for line in reader:
        for symbol in line:
            encoded += s[symbol]

    encoded = l[0][2] + encoded

    piece = len(encoded) % 8
    stub = (8 - piece) if piece != 0 else 0

    result = bytearray()
    result.append(stub)
    encoded += '0' * stub
    for i in range(0, len(encoded), 8):
        result.append(int(encoded[i : i + 8], 2))
    fo.write(result)

def decode(reader, fo):
    s = {}
    current_code = ''
    root = Node(None)
    node = root

    l = reader.read(1)
    if l == '':
        return ''
    stub = ord(l)

    i = 0
    full_line = reader.read()
    line = ''.join([binary_code(symbol) for symbol in full_line])
    while i < len(line):
        i += 1
        if line[i - 1] == '1':
            node.value = chr(int(line[i : i + 8], 2))
            i += 8
            while node.parent != None and node == node.parent.right:
                node = node.parent
            if node.parent == None:
                break
            node = node.parent
            node.right = Node(node)
            node = node.right
        else:
            node.left = Node(node)
            node = node.left

    decoded = ''
    while i < len(line) - stub:
        node = root
        j = 0
        while node.value == None:
            node = node.left if line[i + j] == '0' else node.right
            j += 1
        decoded += node.value
        i += j if j > 0 else 1
    fo.write(decoded)
