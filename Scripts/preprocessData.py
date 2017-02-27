import argparse
import os
import json
import re
import shutil

from collections import defaultdict

def readData(dir):
    data = {}
    allFiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    for f in allFiles:
        with open(os.path.join(dir, f), "r") as input:
            temp = input.read().strip().split('\n')[1:]
            data[f] = temp
    return data

def processData(rawData):
    processedData = {}
    for key in rawData:
        processedData[key] = []
        v = rawData[key]
        for value in v:
            value = re.sub("\\s+", "$_$", value)
            value = re.sub("^", "$", value)
            value = re.sub("$", "$", value)
            value = list(value)
            processedData[key].append(value)
    return processedData

def writeData(processedData, dir):
    if os.path.isdir(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    for key in processedData:
        print(key)
        with open(os.path.join(dir, key), "w") as f:
            v = processedData[key]
            for value in v:
                unicodeStr = u" ".join(value)
                f.write(unicodeStr)
                f.write("\n")

def main(inputDir, outputDir):
    print(inputDir)
    allDirs = [d for d in os.listdir(inputDir) if os.path.isdir(os.path.join(inputDir, d))]
    for d in allDirs:
        print("Processing: %s" % (d))
        rawData = readData(os.path.join(inputDir, d))
        processedData = processData(rawData)
        writeData(processedData, os.path.join(outputDir, d))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess Data")
    parser.add_argument('-i', '--inputDir', action='store', dest='inputDir')
    parser.add_argument('-o', '--outputDir', action='store', dest='outputDir')

    result = parser.parse_args()

    if not os.path.isdir(result.inputDir):
        print("Directory: %s does not exists\nAborting...\n" % (result.inputDir))
        exit()
    if not os.path.isdir(result.outputDir):
        print("Directory: %s does not exists. Do you want to create one (y/n): " % (os.path.join(result.outputDir)))
        response = raw_input("")
        if response == "n":
            exit()
        else:
            os.mkdir(result.outputDir)

    main(result.inputDir, result.outputDir)
