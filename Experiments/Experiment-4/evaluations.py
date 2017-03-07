import argparse
import re
import os
import Levenshtein

def getLevenshteinError(data):
    distanceList = []
    for key in data.keys():
        ref = key
        pred = data[key][0]
        dist = Levenshtein.distance(ref, pred)
        distanceList.append(dist / float(len(ref)))
    return sum(distanceList) / float(len(distanceList))

def getAccuracy(data):
    errorList = []
    for key in data.keys():
        ref = key
        pred = data[key][0]
        if ref.lower() == pred.lower():
            errorList.append(1)
        else:
            errorList.append(0)
    return sum(errorList) / float(len(errorList))

def getFScore(data):
    precisionList = []
    recallList = []
    for key in data.keys():
        ref = key
        distances = [Levenshtein.distance(ref, pred) for pred in data[key]]
        mostAccuratePred = data[key][distances.index(min(distances))]
        LCS = 0.5 * (len(ref) + len(mostAccuratePred) - min(distances))
        recallList.append(LCS / float(len(mostAccuratePred)))
        precisionList.append(LCS / float(len(ref)))
    fScore = [2*p*r/(p+r) for p,r in zip(precisionList, recallList)]
    return sum(fScore) / float(len(fScore))

def getMRR(data):
    mrrList = []
    for key in data.keys():
        ref = key
        rr = 0.0
        for i, pred in enumerate(data[key]):
            if ref.lower() == pred.lower():
                rr = 1.0 / float(i + 1)
                break
        mrrList.append(rr)
    return sum(mrrList) / float(len(mrrList))

def getMAP(data):
    mapList = []
    for key in data.keys():
        ref = key
        apList = []
        correct = 0
        for i, pred in enumerate(data[key]):
            if ref.lower() == pred.lower():
                correct += 1
                apList.append(correct / float(i + 1))
        if not apList:
            mapList.append(0)
        else:    
            mapList.append(sum(apList) / float(len(apList)))
    return sum(mapList) / float(len(mapList))

def parseFile(refFilePath, predFilePath, n):
    rankMap = {}
    indexMap = {}
    with open(predFilePath) as predFile:
        for i, line in enumerate(predFile):
            index = int(line.strip().split(" ||| ")[0])
            target = line.strip().split(" ||| ")[1]
            target = re.sub("\\s+", "", target)
            if index not in indexMap:
                indexMap[index] = []
            indexMap[index].append(target)

    with open(refFilePath) as refFile:
        for index, line in enumerate(refFile):
            if index in indexMap:
                rankMap[re.sub("\\s+", "", line)] = indexMap[index]
    
    for key in rankMap.keys():
        rankMap[key] = rankMap[key][0:n]

    return rankMap

def main(refFilePath, predFilePath, n):
    data = parseFile(refFilePath, predFilePath, n)

    # Avg Normalised Edit Distance
    edit_distance = getLevenshteinError(data)

    # Accuracy
    accuracy = getAccuracy(data)

    # F Score
    f_score = getFScore(data)

    # MRR
    mrr_score = getMRR(data)

    # MAP
    map_score = getMAP(data)
    print("%f, %f, %f, %f, %f" %(edit_distance, accuracy, f_score, mrr_score, map_score))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Data")
    parser.add_argument('-t', '--trueFilePath', action='store', dest='trueFilePath')
    parser.add_argument('-e', '--estimateFilePath', action='store', dest='estimateFilePath')
    parser.add_argument('-n', '--top-n', action='store', dest='n')

    result = parser.parse_args()

    if not os.path.isfile(result.trueFilePath):
        print("Directory: %s does not exists\nAborting...\n" % (result.trueFilePath))
        exit()
    if not os.path.isfile(result.estimateFilePath):
        print("Directory: %s does not exists\nAborting...\n" % (result.estimateFilePath))
        exit()
    if not result.n.isdigit():
        print("%s: not a valid number\nAborting...\n" %(result.n))
        exit()

    main(result.trueFilePath, result.estimateFilePath, int(result.n))
