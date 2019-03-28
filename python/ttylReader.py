import pandas as pd
import time
import numpy as np
from multiprocessing import Process

from multiprocessing.managers import BaseManager

class TTYLReader():
    def __init__(self, fn, delay=None, debug=False):
        self.fn = fn
        self.data = pd.DataFrame(columns=["yaw", "pitch", "roll", "x", "y", "z"])
        self.currIndex = None
        self.delay = delay
        self.debug = debug

    def getData(self):
        return self.data.fillna(method="bfill").fillna(method="ffill").fillna(0)

    def debugPrint(self, data):
        if self.debug and (self.delay is not None or (self.currIndex is not None and self.currIndex % 10 == 0)):
            print(data)
    def readDataAsyncProcessHelper(self):
        f = open(self.fn, 'rb')
        timeFound = False
        if self.delay is not None:
            time.sleep(self.delay)
        while (not timeFound):
            rawSerialString = f.readline()
            self.debugPrint(rawSerialString)
            rawSerialString = str(rawSerialString)[:-4] if rawSerialString is not None else None
            if rawSerialString is not None and "Time" in rawSerialString:
                rawSerialStrings = rawSerialString.split()
                possibleCurrIndex = int(rawSerialStrings[1])
                if int(possibleCurrIndex) > self.currIndex: # sanity check
                    self.currIndex = int(rawSerialStrings[1])
                self.data.loc[self.currIndex] = pd.Series(index=self.data.columns)
            timeFound = True
        while (timeFound):
            try:
                if self.delay is not None:
                    time.sleep(self.delay)
                rawSerialString = f.readline()
                self.debugPrint(rawSerialString)
                rawSerialString = str(rawSerialString)[:-4] if rawSerialString is not None else None
                if "Time" in rawSerialString:
                    rawSerialString = rawSerialString.split()
                    self.currIndex = int(rawSerialString[1])
                    self.data.loc[self.currIndex] = pd.Series()
                elif "ypr" in rawSerialString:
                    splitRawString = rawSerialString.split("\\t")
                    self.data.loc[self.currIndex]['yaw'] = np.float32(splitRawString[1])
                    self.data.loc[self.currIndex]['pitch'] = np.float32(splitRawString[2])
                    self.data.loc[self.currIndex]['roll'] = np.float32(splitRawString[2])
                elif "aaWG" in rawSerialString:
                    splitRawString = rawSerialString.split("\\t")
                    self.data.loc[self.currIndex]['x'] = np.float32(splitRawString[1])
                    self.data.loc[self.currIndex]['y'] = np.float32(splitRawString[2])
                    self.data.loc[self.currIndex]['z'] = np.float32(splitRawString[2])
                self.debugPrint(self.getData())
            except Exception as e:
                self.debugPrint("exception occurred")
                self.debugPrint(e)

def readDataAsyncProcess(fn="/dev/ttyS5"):
    BaseManager.register('TTYLReader', TTYLReader)
    manager = BaseManager()
    manager.start()
    reader = manager.TTYLReader(fn, debug=False)
    p = Process(target=reader.readDataAsyncProcessHelper)
    p.start()
    return reader, p



if __name__ == "__main__":
    reader, process = readDataAsyncProcess()
    time.sleep(4)
    process.terminate()
    print(reader.getData())
