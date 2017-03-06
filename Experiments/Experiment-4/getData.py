import argparse
import os
import re
import codecs
import json

def readData(inputFilePath):
    print("reading")
    with open(inputFilePath, "r") as f:
        data = f.read()
    return data

def parseData(data, limit):
    print("parsing")
    lines = data.strip("\r\n").split('\n')
    parse_data = []

    if len(lines) == 0:
        print("File contains empty string")
        return parse_data

    heading = lines[0]
    tags = heading.strip().split()

    cnt = 0
    for line in lines:
        print("%d / %d\n" % (cnt, len(lines)))
        cnt += 1
        if limit >= 0 and cnt > limit:
            break
        line_data = line.split('\t')
        dict_data = {}
        for j in range(len(line_data)):
            dict_data[tags[j]] = line_data[j].strip()
        parse_data.append(dict_data)
    return parse_data

def main(languages, inputFile, outputDir):
    data = readData(inputFile)
    parse = parseData(data, -1)[1:]
    print("cleaning")
    cleanData = []
    for item in parse:
        cnt = 0
        for lang in languages:
            if item[lang] != "":
                cnt += 1
        if cnt >= 2:
            cleanData.append(item)
    print("writing")
    for lang in languages:
        with open(os.path.join(outputDir, lang), "w") as f:
            for item in cleanData:
                try:
                    f.write(item[lang])
                    f.write("\n")
                except KeyError as err:
                    print(lang)
                    print(item)
                    print(err)
                    exit()
    print("done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Data - k Fold Cross [60, 70, 80, 90]")
    parser.add_argument('-l', '--languages', nargs='*', action='store', dest='languages')
    parser.add_argument('-i', '--inputFile', action='store', dest='inputFile')
    parser.add_argument('-o', '--outputDir', action='store', dest='outputDir')

    result = parser.parse_args()

    if not os.path.isfile(result.inputFile):
        print("File: %s does not exists\nAborting...\n" % (result.inputFile))
        exit()
    if len(result.languages) < 3:
        print("[%d]: Have to specify at least 3 languages" % (len(result.languages)))
        exit()
    if not os.path.isdir(result.outputDir):
        print("Directory: %s does not exists. Do you want to create one (y/n): " % (result.outputDir))
        response = raw_input("")
        if response == "n" or response == "no":
            exit()
        else:
            os.makedirs(result.outputDir)

    main(result.languages, result.inputFile, result.outputDir)
