import argparse
import os
import random

def readData(filePath):
    print("reading")
    with open(filePath, "r") as f:
        data = f.read().strip().split("\n")
    return data

def writeData(filePath, data):
    print("File: %s\n" %(filePath))
    with open(filePath, "w") as f:
        for line in data:
            f.write(line + "\n")

def handleRep(sourceData, sourceLang, targetData, targetLang, dirPath, perc, assignment):
    inputPath = os.path.join(dirPath, "train-" + str(int(perc * 100)), "input")
    if not os.path.isdir(inputPath):
        os.makedirs(inputPath)
    
    numLines = len(sourceData)

    tfCommand = "source ../../../bin/activate\n"
    tfCommand += "python /nlp/users/devjain/cis599/Experiments/Experiment-6/models/tutorials/rnn/translate/translate.py "
    tfCommand += "--from_train_data " + os.path.abspath(os.path.join(inputPath, "train.hi")) + " "
    tfCommand += "--to_train_data " + os.path.abspath(os.path.join(inputPath, "train.en")) + " "
    tfCommand += "--from_dev_data " + os.path.abspath(os.path.join(inputPath, "test.hi")) + " " 
    tfCommand += "--to_dev_data " + os.path.abspath(os.path.join(inputPath, "test.en")) + "\n"
    tfCommand += "deactivate\n"

    with open(os.path.join(dirPath, "train-" + str(int(perc * 100)), "run.sh"), "w") as f:
        f.write(tfCommand)

    sourceTrainData = [sourceData[i] for i in assignment[:int(numLines * perc)]]
    targetTrainData = [targetData[i] for i in assignment[:int(numLines * perc)]]
    writeData(os.path.join(inputPath, "train." + sourceLang), sourceTrainData)
    writeData(os.path.join(inputPath, "train." + targetLang), targetTrainData)

    sourceRemainingData = [sourceData[i] for i in assignment[int(numLines * perc):]]
    targetRemainingData = [targetData[i] for i in assignment[int(numLines * perc):]]

    sourceTestData = sourceRemainingData
    targetTestData = targetRemainingData
    writeData(os.path.join(inputPath, "test." + sourceLang), sourceTestData)
    writeData(os.path.join(inputPath, "test." + targetLang), targetTestData)

def main(sourceFilePath, sourceLang, targetFilePath, targetLang, outputDir, numRep):
    sourceData = readData(sourceFilePath)
    targetData = readData(targetFilePath)
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
    parser.add_argument('-s', '--sourceFilePath', action='store', dest='sourceFilePath')
    parser.add_argument('-sl', '--sourceLang', action='store', dest='sourceLang', default='hi')
    parser.add_argument('-t', '--targetFilePath', action='store', dest='targetFilePath')
    parser.add_argument('-tl', '--targetLang', action='store', dest='targetLang', default='en')
    parser.add_argument('-o', '--outputDir', action='store', dest='outputDir')
    parser.add_argument('-n', '--numRep', action='store', dest='numRep', default='10')

    result = parser.parse_args()

    if not result.numRep.isdigit():
        print("Number of Folds: %d has to be positive integer\n" % (result.numRep))
        exit()
    if not os.path.isfile(result.sourceFilePath):
        print("File: %s does not exists\nAborting...\n" % (result.sourceFilePath))
        exit()
    if not os.path.isfile(result.targetFilePath):
        print("File: %s does not exists\nAborting...\n" % (result.targetFilePath))
        exit()
    if not os.path.isdir(result.outputDir):
        print("Directory: %s does not exists. Do you want to create one (y/n): " % (result.outputDir))
        response = raw_input("")
        if response == "n" or response == "no":
            exit()
        else:
            os.makedirs(result.outputDir)

    main(result.sourceFilePath, result.sourceLang, result.targetFilePath, result.targetLang, result.outputDir, result.numRep)
