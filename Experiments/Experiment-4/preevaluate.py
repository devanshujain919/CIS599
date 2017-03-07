import os

def read(filePath):
    with open(filePath, "r") as f:
        data = f.read().strip("\r\n").split("\n")
    return data

def write(outputFilePath, data):
    with open(outputFilePath, "w") as f:
        for k,v in data.iteritems():
            for item in v:
                f.write(k)
                f.write(" ||| ")
                f.write(item)
                f.write("\n")

def readData(filePath):
    mapData = {}
    data = readData(filePath)
    for item in data:
        line_num = int(item.split(" ||| ")[0])
        word = item.split(" ||| ")[1]
        if line_num not in mapData:
            mapData[line_num] = []
        mapData[line_num].append(word)
    return mapData

def main(sourceFilePath, intermediateFilePath, targetFilePath, outputFilePath):
    intermediateData = readData(intermediateFilePath)
    targetData = readData(targetFilePath)
    
    finalData = {}
    index = 0
    for k,v in intermediateData.iteritems()
        if k not in finalData:
            finalData[k] = []
        for item in v:
            finalData[k].extend(targetData[index])
            index += 1

    write(outputFilePath, finalData)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Data")
    parser.add_argument('-s', '--sourceFilePath', action='store', dest='sourceFilePath')
    parser.add_argument('-i', '--intermediateFilePath', action='store', dest='intermediateFilePath')
    parser.add_argument('-t', '--targetFilePath', action='store', dest='targetFilePath')
    parser.add_argument('-o', '--outputFilePath', action='store', dest='outputFilePath')

    result = parser.parse_args()

    if not os.path.isfile(result.sourceFilePath):
        print("Directory: %s does not exists\nAborting...\n" % (result.sourceFilePath))
        exit()
    if not os.path.isfile(result.intermediateFilePath):
        print("Directory: %s does not exists\nAborting...\n" % (result.intermediateFilePath))
        exit()
    if not os.path.isfile(result.targetFilePath):
        print("Directory: %s does not exists\nAborting...\n" % (result.targetFilePath))
        exit()
    main(result.sourceFilePath, result.intermediateFilePath, result.targetFilePath, result.outputFilePath)

