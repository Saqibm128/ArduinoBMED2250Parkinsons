import pandas as pd
import time
import numpy as np
from multiprocessing import Process

class TTYLReader():
    def __init__(self, fn, delay=None, debug=False):
        self.fn = fn
        self.data = pd.DataFrame(columns=["yaw", "pitch", "roll", "x", "y", "z"])
        self.currIndex = None
        self.delay = delay
        self.debug = debug

    def debugPrint(self, data):
        if self.debug:
            print(data)
    def _readDataAsyncProcessHelper(self):
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
                self.currIndex = int(rawSerialStrings[1])
                self.data[self.currIndex] = pd.Series(index=self.data.columns)
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
                self.debugPrint(self.data)
            except Exception as e:
                self.debugPrint("exception occurred")
                self.debugPrint(e)

    def readDataAsyncProcess(self):

        p = Process(target=self._readDataAsyncProcessHelper)
        p.start()
        return p



if __name__ == "__main__":
    f = TTYLReader("/dev/ttyS5")
    f.readDataAsyncProcess()
