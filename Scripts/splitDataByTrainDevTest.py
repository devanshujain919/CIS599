import argparse
import os
import codecs
import json
import re
import shutil

from collections import defaultdict

def writeData(source, target, sourceFilePath, targetFilePath):
    if os.path.isfile(sourceFilePath):
        os.remove(sourceFilePath)
    if os.path.isfile(targetFilePath):
        os.remove(targetFilePath)

    with open(sourceFilePath, "w") as f:
        for val in source:
            f.write(val)
            f.write("\n");
    with open(targetFilePath, "w") as f:
        for val in target:
            f.write(val)
            f.write("\n");

def main(sourceFilePath, targetFilePath, outputDir):
    source = []
    with open(sourceFilePath, "r") as f:
        source = f.read().strip().split('\n')
    target = []
    with open(targetFilePath, "r") as f:
        target = f.read().strip().split('\n')

    partition = [0.8,0.1,0.1]
    if sum(partition) != 1:
        print("Wrong partition specified\nAborting\n")
        exit(1)

    sourceTrain = []
    targetTrain = []
    sourceDev = []
    targetDev = []
    sourceDevTest = []
    targetDevTest = []

    totalNum = min(len(source), len(target))
    trainCount = int(partition[0] * totalNum)
    sourceTrain = source[:trainCount]
    targetTrain = target[:trainCount]
    devCount = int(partition[1] * totalNum)
    sourceDev = source[trainCount:trainCount+devCount]
    targetDev = target[trainCount:trainCount+devCount]
    sourceDevTest = source[trainCount+devCount:]
    targetDevTest = target[trainCount+devCount:]

    writeData(sourceTrain, targetTrain, os.path.join(outputDir, "train." + os.path.basename(sourceFilePath)), os.path.join(outputDir, "train." + os.path.basename(targetFilePath)))
    writeData(sourceDev, targetDev, os.path.join(outputDir, "dev." + os.path.basename(sourceFilePath)), os.path.join(outputDir, "dev." + os.path.basename(targetFilePath)))
    writeData(sourceDevTest, targetDevTest, os.path.join(outputDir, "devtest." + os.path.basename(sourceFilePath)), os.path.join(outputDir, "devtest." + os.path.basename(targetFilePath)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Data")
    parser.add_argument('-s', '--sourceFile', action='store', dest='sourceFilePath')
    parser.add_argument('-t', '--targetFile', action='store', dest='targetFilePath')
    parser.add_argument('-o', '--outputDir', action='store', dest='outputDir')

    result = parser.parse_args()

    if not os.path.isfile(result.sourceFilePath):
        print("Directory: %s does not exists\nAborting...\n" % (result.sourceFilePath))
        exit()
    if not os.path.isfile(result.targetFilePath):
        print("Directory: %s does not exists\nAborting...\n" % (result.targetFilePath))
        exit()
    if not os.path.isdir(result.outputDir):
        print("Directory: %s does not exists. Do you want to create one (y/n): " % (result.outputDir))
        response = raw_input("")
        if response == "n":
            exit()
        else:
            os.makedirs(result.outputDir)

    main(result.sourceFilePath, result.targetFilePath, result.outputDir)
