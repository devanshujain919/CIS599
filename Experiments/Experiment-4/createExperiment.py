import argparse
import os
import random

def readData(filePath):
    print("reading")
    with open(filePath, "r") as f:
        data = f.read().split("\n")
    return data

def writeData(filePath, data):
    print("File: %s\n" %(filePath))
    with open(filePath, "w") as f:
        for line in data:
            f.write(line + "\n")

def handleRep(sourceData, sourceLang, intermediateData, intermediateLang, targetData, targetLang, dirPath, perc):
    inputPath = os.path.join(dirPath, "train-" + str(int(perc * 100)), "input")
    if not os.path.isdir(inputPath):
        os.makedirs(inputPath)
    outputPath = os.path.join(dirPath, "train-" + str(int(perc * 100)), "source-intermediate")
    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)
    outputPath = os.path.join(dirPath, "train-" + str(int(perc * 100)), "intermediate-target")
    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)
    numTestableLines = 0
    for (sl,tl) in zip(sourceData, targetData):
        if sl != "" and tl != "":
            numTestableLines += 1
    assignment = random.sample(range(numTestableLines), numTestableLines)

    """
    will put `numTestLines` for testing
    have to select training data from rest 
    """

    joshuaCommand = "/nlp/users/devjain/joshua-6.0.5/bin/pipeline.pl " \
        "--rundir ./ " \
        "--source " + sourceLang + " " \
        "--target " + intermediateLang + " " \
        "--type hiero " \
        "--corpus ../input/train." + sourceLang + "-" + intermediateLang + " " \
        "--tune ../input/tune." + sourceLang + "-" + intermediateLang + " " \
        "--lm-order 8 " \
        "--lm-gen berkeleylm " \
        "--lm berkeleylm " \
        "--aligner berkeley"
    with open(os.path.join(dirPath, "train-" + str(int(perc * 100)), "source-intermediate", "run_source_intermediate.sh"), "w") as f:
        f.write(joshuaCommand)

    joshuaCommand = "/nlp/users/devjain/joshua-6.0.5/bin/pipeline.pl " \
        "--rundir ./ " \
        "--source " + intermediateLang + " " \
        "--target " + targetLang + " " \
        "--type hiero " \
        "--corpus ../input/train" + intermediateLang + "-" + targetLang + " " \
        "--tune ../input/tune" + intermediateLang + "-" + targetLang + " " \
        "--lm-order 8 " \
        "--lm-gen berkeleylm " \
        "--lm berkeleylm " \
        "--aligner berkeley"
    with open(os.path.join(dirPath, "train-" + str(int(perc * 100)), "intermediate-target", "run_intermediate_target.sh"), "w") as f:
        f.write(joshuaCommand)

    numTestLines = int(0.5 * (1.0 - perc) * numTestableLines)
    
    sourceTestData = []
    intermediateTestData = []
    targetTestData = []
    cnt = 0
    for i in assignment:
        if cnt >= numTestLines:
            break
        if sourceData[i] != "" and targetData[i] != "":
            cnt += 1
            sourceTestData.append(sourceData[i])
            intermediateTestData.append(intermediateData[i])
            targetTestData.append(targetData[i])
    writeData(os.path.join(inputPath, "test." + sourceLang), sourceTestData)
    writeData(os.path.join(inputPath, "test." + intermediateLang), intermediateTestData)
    writeData(os.path.join(inputPath, "test." + targetLang), targetTestData)
    
    sourceIntermediateTrainData_source = []
    sourceIntermediateTrainData_intermediate = []
    for i in assignment[cnt:]:
        if sourceData[i] != "" and intermediateData[i] != "":
            sourceIntermediateTrainData_source.append(sourceData[i])
            sourceIntermediateTrainData_intermediate.append(intermediateData[i])
    sourceIntermediateTrainData_source_tune = sourceIntermediateTrainData_source[:numTestLines]
    sourceIntermediateTrainData_intermediate_tune = sourceIntermediateTrainData_intermediate[:numTestLines]
    sourceIntermediateTrainData_source_train = sourceIntermediateTrainData_source[numTestLines:]
    sourceIntermediateTrainData_intermediate_train = sourceIntermediateTrainData_intermediate[numTestLines:]
    writeData(os.path.join(inputPath, "train." + sourceLang + "-" + intermediateLang + "." + sourceLang), sourceIntermediateTrainData_source_train)
    writeData(os.path.join(inputPath, "train." + sourceLang + "-" + intermediateLang + "." + intermediateLang), sourceIntermediateTrainData_intermediate_train)
    writeData(os.path.join(inputPath, "tune." + sourceLang + "-" + intermediateLang + "." + sourceLang), sourceIntermediateTrainData_source_tune)
    writeData(os.path.join(inputPath, "tune." + sourceLang + "-" + intermediateLang + "." + intermediateLang), sourceIntermediateTrainData_intermediate_tune)

    intermediateTargetTrainData_intermediate = []
    intermediateTargetTrainData_target = []
    for i in assignment[cnt:]:
        if intermediateData[i] != "" and targetData[i] != "":
            intermediateTargetTrainData_intermediate.append(intermediateData[i])
            intermediateTargetTrainData_target.append(targetData[i])
    intermediateTargetTrainData_intermediate_tune = intermediateTargetTrainData_intermediate[:numTestLines]
    intermediateTargetTrainData_target_tune = intermediateTargetTrainData_target[:numTestLines]
    intermediateTargetTrainData_intermediate_train = intermediateTargetTrainData_intermediate[numTestLines:]
    intermediateTargetTrainData_target_train = intermediateTargetTrainData_target[numTestLines:]
    writeData(os.path.join(inputPath, "train." + intermediateLang + "-" + targetLang + "." + intermediateLang), intermediateTargetTrainData_intermediate_train)
    writeData(os.path.join(inputPath, "train." + intermediateLang + "-" + targetLang + "." + targetLang), intermediateTargetTrainData_target_train)
    writeData(os.path.join(inputPath, "tune." + intermediateLang + "-" + targetLang + "." + intermediateLang), intermediateTargetTrainData_intermediate_tune)
    writeData(os.path.join(inputPath, "tune." + intermediateLang + "-" + targetLang + "." + targetLang), intermediateTargetTrainData_intermediate_tune)

def main(sourceFilePath, sourceLang, intermediateFilePath, intermediateLang, targetFilePath, targetLang, outputDir, numRep):
    sourceData = readData(sourceFilePath)
    intermediateData = readData(intermediateFilePath)
    targetData = readData(targetFilePath)
    numLines = len(sourceData)
    if numLines != len(targetData) or len(intermediateData) != len(targetData) or numLines != len(intermediateData):
        print("Number of lines in source, intermediate and target files not same")
        return
    division = [0.6, 0.7, 0.8, 0.9]
    for rep in range(int(numRep)):
        for percentage in division:
            handleRep(sourceData, sourceLang, intermediateData, intermediateLang, targetData, targetLang, os.path.join(outputDir, "rep-" + str(rep)), percentage)
            with open(os.path.join(outputDir, "run.sh"), "a") as f:
                f.write("cd " + os.path.join("rep-" + str(rep), "train-" + str(int(percentage * 100)), "source-intermediate") + "\n")
                f.write("qsub -cwd run_source_intermediate.sh\n")
                f.write("cd -\n")
                f.write("cd " + os.path.join("rep-" + str(rep), "train-" + str(int(percentage * 100)), "intermediate-target") + "\n")
                f.write("qsub -cwd run_intermediate_target.sh\n")
                f.write("cd -\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Data - k Fold Cross [60, 70, 80, 90]")
    parser.add_argument('-s', '--sourceFilePath', action='store', dest='sourceFilePath')
    parser.add_argument('-sl', '--sourceLang', action='store', dest='sourceLang', default='devnagri')
    parser.add_argument('-t', '--targetFilePath', action='store', dest='targetFilePath')
    parser.add_argument('-tl', '--targetLang', action='store', dest='targetLang', default='en')
    parser.add_argument('-i', '--intermediateFilePath', action='store', dest='intermediateFilePath')
    parser.add_argument('-il', '--intermediateLang', action='store', dest='intermediateLang', default='en')
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
    if not os.path.isfile(result.intermediateFilePath):
        print("File: %s does not exists\nAborting...\n" % (result.intermediateFilePath))
        exit()
    if not os.path.isdir(result.outputDir):
        print("Directory: %s does not exists. Do you want to create one (y/n): " % (result.outputDir))
        response = raw_input("")
        if response == "n" or response == "no":
            exit()
        else:
            os.makedirs(result.outputDir)

    main(result.sourceFilePath, result.sourceLang, result.intermediateFilePath, result.intermediateLang, result.targetFilePath, result.targetLang, result.outputDir, result.numRep)
