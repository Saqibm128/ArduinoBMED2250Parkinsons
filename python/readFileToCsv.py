import sys, os
import pandas as pd
import numpy as np
import traceback
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

fns = os.listdir("/mnt/c/Users/sawer/Google Drive/BMED 2250 Group Folder/P3/data3_31/p3test")
fns = [fn for fn in fns if ".TXT" in fn]
# print(fns)

snrRatios = pd.Series()
stdv = pd.Series()

for fn in fns:
    print(fn[:-4])
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
        # data["uncleanPostureAngle"] = 90 - np.degrees(np.arctan(data["acc1y"] / (data["acc1x"] ** 2 + data["acc1z"] ** 2) ** 0.5))
        data["uncleanPostureAngle"] = 90 - np.degrees(np.arcsin(data["acc1y"]))
        data["uncleanPostureAngle"] = data["uncleanPostureAngle"].fillna(0)

    except Exception as e:
        print(traceback.format_exc())
    data["signalAngle"] = data["uncleanPostureAngle"].rolling(5).mean()
    data["noiseAngle"] =  data["uncleanPostureAngle"] - data["signalAngle"]
    data["logSnrPowerRatio"] = np.log10(data["signalAngle"]/data["noiseAngle"]) * 2
    # data["isIntentional"] =
    # print(data["signalAngle"])
    b = None
    r = None
    try:
        line = plt.plot(-100, -100, "b-")
        line = plt.plot(-100, -100, "r-")
        plt.plot([-100, 1000000], [20, 20], 'k--')
        for i in range(len(data) - 2):
            # print(data.index[i:i+1], data["signalAngle"][i:i+1])
            line = plt.plot(data.index[i:i+2].values, data["signalAngle"][i:i+2].values, 'r-' if data["signalAngle"].iloc[i] > 20 else "b-")
        plt.title(fn[:-4] + " Cleaned Angle Data")
        leg = plt.legend(["ON Period Back Angle < 20", "OFF Period Back Angle > 20"])
        plt.xlabel("Time (Milliseconds)")
        plt.ylabel("Thoracic Lumbar Angle Deviation from Vertical")
        plt.ylim(0, 120)
        plt.xlim(data.index[0], data.index[-1])
        plt.savefig(fn[:-4] + "postureAngle.png", dpi=500)
        plt.clf()
        snrRatios[fn[:-4]] =  20 * data["logSnrPowerRatio"].mean()
        stdv[fn[:-4]] = data["signalAngle"].std()
        print(data["signalAngle"].std(), "hi")
    except Exception:
        print("yolo3")

    # accelTotal = (data['acc1x'] ** 2 + dfBack['acc1y'] ** 2 + dfBack['acc1z'] ** 2) ** 0.5
    # angVelBackTotal = (dfAngBack['gyr1y'] ** 2 + dfAngBack['gyr1p'] ** 2 + dfAngBack['gyr1r'] ** 2) ** 0.5
    # angVelThighTotal = (dfAngThigh['acc2x'] ** 2 + dfAngThigh['acc2y'] ** 2 + dfAngThigh['acc2z'] ** 2) ** 0.5
    # accelThigh =(dfThigh['gyr2y'] ** 2 + dfThigh['gyr2p'] ** 2 + dfThigh['gyr2r'] ** 2) ** 0.5
    #
    # isMoving = ((accelTotal.rolling(10).max() - accelTotal.rolling(10).min()) > 4) &\
    #      ((accelThigh.rolling(10).max() - accelThigh.rolling(10).min()) > 4) & \
    #      ((angVelBackTotal.rolling(10).max() - angVelBackTotal.rolling(10).min()) > 60 / 360 * 2 * np.pi) &\
    #      ((angVelThighTotal.rolling(10).max() - angVelThighTotal.rolling(10).min()) > 60 / 360 * 2 * np.pi)
    #
    # isIntentionalAccel = (accelThigh > 9.8 * 1.05 & accelTotal > 9.8 * 1.05)
    # isIntentionalAngVel = (angVelThighTotal.rolling(10).mean() > np.radians(340))
    # isIntentional = isIntentionalAccel & isIntentionalAngVel

    data.to_csv(fn2)

print(snrRatios)
