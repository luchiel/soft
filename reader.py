import os

LINE_SIZE = 2 ** 10

class Reader(object):
    def __init__(self, filename):
        self.file = open(filename, 'rb')

    def __iter__(self):
        self.line = self.file.read(LINE_SIZE)
        while self.line:
            yield self.line
            self.line = self.file.read(LINE_SIZE)

    def reset(self):
        self.file.seek(0)

    def read(self, size=-1):
        return self.file.read(size)

    def close(self):
        self.file.close()
