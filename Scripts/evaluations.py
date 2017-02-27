import argparse
import re
import os
import Levenshtein

def dispLevenshteinError(refData, predData):
    distanceList = []
    for ref,pred in zip(refData, predData):
        ref = re.sub("\\s+", "", ref)
        pred = re.sub("\\s+", "", pred)
        dist = Levenshtein.distance(ref, pred)
        distanceList.append(dist / float(len(ref)))
    return sum(distanceList) / float(len(distanceList))

def main(refFilePath, predFilePath):
    refData = []
    with open(refFilePath, "r") as f:
        refData = f.read().strip().split('\n')
    predData = []
    with open(predFilePath, "r") as f:
        predData = f.read().strip().split('\n')

    error = dispLevenshteinError(refData, predData)
    print("Averaged Normalised Edit Distance with Reference: %f\n" % (error))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Data")
    parser.add_argument('-t', '--trueFilePath', action='store', dest='trueFilePath')
    parser.add_argument('-e', '--estimateFilePath', action='store', dest='estimateFilePath')

    result = parser.parse_args()

    if not os.path.isfile(result.trueFilePath):
        print("Directory: %s does not exists\nAborting...\n" % (result.trueFilePath))
        exit()
    if not os.path.isfile(result.estimateFilePath):
        print("Directory: %s does not exists\nAborting...\n" % (result.estimateFilePath))
        exit()

    main(result.trueFilePath, result.estimateFilePath)