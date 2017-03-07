import argparse
import os
import random
import json
import itertools
import re

def readData(filePath):
    print("reading")
    with open(filePath, "r") as f:
        data = json.load(f)
    return data

def writeData(filePath, data):
    print("File: %s\n" %(filePath))
    with open(filePath, "w") as f:
        for line in data:
            l = re.sub("\\s+", "_", line)
            f.write(" ".join(list(l)).encode("utf-8"))
            f.write("\n")

def handleRep(sourceData, sourceLang, targetData, targetLang, dirPath, perc, assignment):
    inputPath = os.path.join(dirPath, "train-" + str(int(perc * 100)), "input")
    if not os.path.isdir(inputPath):
        os.makedirs(inputPath)
    
    numLines = len(sourceData)

    joshuaCommand = "/nlp/users/devjain/joshua-6.0.5/bin/pipeline.pl " \
        "--rundir ./ " \
        "--source " + sourceLang + " " \
        "--target " + targetLang + " " \
        "--type hiero " \
        "--corpus input/train " \
        "--tune input/tune " \
        "--test input/test " \
        "--lm-order 8 " \
        "--lm-gen berkeleylm " \
        "--lm berkeleylm " \
        "--aligner berkeley"
    with open(os.path.join(dirPath, "train-" + str(int(perc * 100)), "run.sh"), "w") as f:
        f.write(joshuaCommand)

    sourceTrainData = [sourceData[i] for i in assignment[:int(numLines * perc)]]
    targetTrainData = [targetData[i] for i in assignment[:int(numLines * perc)]]
    writeData(os.path.join(inputPath, "train." + sourceLang), sourceTrainData)
    writeData(os.path.join(inputPath, "train." + targetLang), targetTrainData)

    sourceRemainingData = [sourceData[i] for i in assignment[int(numLines * perc):]]
    targetRemainingData = [targetData[i] for i in assignment[int(numLines * perc):]]

    sourceDevTestData = sourceRemainingData[:int(0.5 * len(sourceRemainingData))]
    targetDevTestData = targetRemainingData[:int(0.5 * len(targetRemainingData))]
    writeData(os.path.join(inputPath, "tune." + sourceLang), sourceDevTestData)
    writeData(os.path.join(inputPath, "tune." + targetLang), targetDevTestData)

    sourceTestData = sourceRemainingData[int(0.5 * len(sourceRemainingData)):]
    targetTestData = targetRemainingData[int(0.5 * len(targetRemainingData)):]
    writeData(os.path.join(inputPath, "test." + sourceLang), sourceTestData)
    writeData(os.path.join(inputPath, "test." + targetLang), targetTestData)

def main(filePath, sourceLang, targetLang, outputDir, numRep):
    data = readData(filePath)
    sourceData = []
    targetData = []
    for item in data:
        if "hi" in item and "en" in item:
            cross_product = list(itertools.product(item["hi"], item["en"]))
            sourceData.extend([k for k,v in cross_product])
            targetData.extend([v for k,v in cross_product])
    numLines = len(sourceData)
    if numLines != len(targetData):
        print("Number of lines in source and target files not same")
        return
    division = [0.6, 0.7, 0.8, 0.9]
    for rep in range(int(numRep)):
        assignment = random.sample(range(numLines), numLines)
        for percentage in division:
            handleRep(sourceData, sourceLang, targetData, targetLang, os.path.join(outputDir, "rep-" + str(rep)), percentage, assignment)
            with open(os.path.join(outputDir, "run.sh"), "a") as f:
                f.write("cd " + os.path.join("rep-" + str(rep), "train-" + str(int(percentage * 100))) + "\n")
                f.write("qsub -cwd run.sh\n")
                f.write("cd -\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Data - k Fold Cross [60, 70, 80, 90]")
    parser.add_argument('-f', '--filePath', action='store', dest='filePath')
    parser.add_argument('-sl', '--sourceLang', action='store', dest='sourceLang', default='hi')
    parser.add_argument('-tl', '--targetLang', action='store', dest='targetLang', default='en')
    parser.add_argument('-o', '--outputDir', action='store', dest='outputDir')
    parser.add_argument('-n', '--numRep', action='store', dest='numRep', default='10')

    result = parser.parse_args()

    if not result.numRep.isdigit():
        print("Number of Folds: %d has to be positive integer\n" % (result.numRep))
        exit()
    if not os.path.isfile(result.filePath):
        print("File: %s does not exists\nAborting...\n" % (result.filePath))
        exit()
    if not os.path.isdir(result.outputDir):
        print("Directory: %s does not exists. Do you want to create one (y/n): " % (result.outputDir))
        response = raw_input("")
        if response == "n" or response == "no":
            exit()
        else:
            os.makedirs(result.outputDir)

    main(result.filePath, result.sourceLang, result.targetLang, result.outputDir, result.numRep)

