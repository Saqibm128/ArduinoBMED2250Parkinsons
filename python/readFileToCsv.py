import sys, os
import pandas as pd
import numpy as np
import traceback
import matplotlib.pyplot as plt

fns = os.listdir("/mnt/c/Users/sawer/Google Drive/BMED 2250 Group Folder/P3/data3_31/p3test")
fns = [fn for fn in fns if ".TXT" in fn]
# print(fns)

for fn in fns:
    fn2 = fn[:-4] + ".csv"
    data = pd.DataFrame(columns=["gyr1y", "gyr1p", "gyr1r", "acc1x", "acc1y", "acc1z", "gyr2y", "gyr2p", "gyr2r", "acc2x", "acc2y", "acc2z", "uncleanPostureAngle", "signalAngle", "noiseAngle"])
    startTime = None
    currTime = None
    fileObj = open(fn)
    for line in fileObj:
        try:
            if "Time" in line:
                parsedTime = int(line.split(" ")[1][:-1])
                if startTime is None:
                    startTime = parsedTime
                currTime = parsedTime
            if startTime is not None and "gyro" in line:
                points = line.split("\t")
                if len(points) >= 17:
                    index = currTime - startTime
                    data.loc[index] = pd.Series()
                    data.loc[index]["gyr1y"] = float(points[1])
                    data.loc[index]["gyr1p"] = float(points[2])
                    data.loc[index]["gyr1r"] = float(points[3])
                    data.loc[index]["acc1x"] = float(points[5])
                    data.loc[index]["acc1y"] = float(points[6])
                    data.loc[index]["acc1z"] = float(points[7])
                    data.loc[index]["gyr2y"] = float(points[10])
                    data.loc[index]["gyr2p"] = float(points[11])
                    data.loc[index]["gyr2r"] = float(points[12])
                    data.loc[index]["acc2x"] = float(points[14])
                    data.loc[index]["acc2y"] = float(points[15])
                    data.loc[index]["acc2z"] = float(points[16][:-1])
        except Exception:
            print("yolo")
    try:
        data = data.astype(np.float64)
        data["uncleanPostureAngle"] = 90 - np.degrees(np.arctan(data["acc1y"] / (data["acc1x"] ** 2 + data["acc1z"] ** 2) ** 0.5))
    except Exception as e:
        print(traceback.format_exc())
    data["signalAngle"] = data["uncleanPostureAngle"].rolling(5).mean()
    data["noiseAngle"] =  data["uncleanPostureAngle"] - data["signalAngle"]
    data["logSnrPowerRatio"] = np.log10(data["signalAngle"]/data["noiseAngle"]) * 2
    # data["isIntentional"] =
    # print(data["signalAngle"])
    plt.plot(data.index[data["signalAngle"] < 20], data["signalAngle"][data["signalAngle"] < 20], 'bo')
    plt.plot(data.index[data["signalAngle"] >= 20], data["signalAngle"][data["signalAngle"] >= 20], 'ro')
    plt.title(fn[:-4] + " Cleaned Angle Data")
    plt.legend(["OFF Period Back Angle < 20", "ON Period Back Angle > 20"])
    plt.xlabel("Time (Milliseconds)")
    plt.ylabel("Thoracic Lumbar Angle Deviation from Vertical")
    plt.ylim(0, 120)
    plt.savefig(fn[:-4] + "postureAngle.png", dpi=500)
    plt.clf()

    data.to_csv(fn2)
