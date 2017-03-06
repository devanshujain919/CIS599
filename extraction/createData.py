# -*- coding: <utf-8> -*-
import argparse
import os
import json
import codecs

def getLangList(inputFile):
    with open(inputFile) as f:
        line = f.readline().strip("\r\n").split("\t")
        return line

def createData(inputFile, languages):
    jsonData = []
    with open(inputFile, "r") as f:
        data = f.read()
    lines = data.strip("\r\n").split("\n")
    for i,content in enumerate(lines):
        if not i == 0:
            parse = dict()
            line = content.split("\t")
            for j,word in enumerate(line):
                if not word == "":
                    if languages[j] not in parse:
                        parse[languages[j]] = []
                    try:
                        parse[languages[j]].append(word)
                    except UnicodeEncodeError as err:    
                        print(word)
                        print(i)
                        print(languages[j])
                        print(err)
                        exit()
            jsonData.append(parse)
    return jsonData

def includeBacklinks(dataDir, languages, jsonData):
    for lang in languages:
        fileName = os.path.join(dataDir, "backlinks." + lang)
        if not os.path.isfile(fileName):
            print("ERROR")
            exit()
        with codecs.open(fileName, "r", encoding="utf-8") as f:
            for index,content in enumerate(f):
                if not index == 0:
                    line = content.strip("\r\n").split("\t")
                    count = int(line[0])
                    if count > 1:
                        if lang not in jsonData[index - 1]:
                            jsonData[index - 1][lang] = []
                        jsonData[index - 1][lang].extend(line[2:])
    return jsonData

def readMapFile(mapFile):
    mapping = {}
    with open(mapFile, "r") as f:
        for index,content in enumerate(f):
            line = content.strip("\r\n").split("\t")
            if line[1].startswith("data/articles/en/"):
                mapping[int(line[0])] = line[1]
    return mapping

def readNationalityFile(nationalityFile):
    mapping = {}
    with open(nationalityFile, "r") as f:
        for index,content in enumerate(f):
            line = content.strip("\r\n")
            if not line == "":
                line = line.split("\t")
                mapping[line[0]] = line[1]
    return mapping

def includeNationality(mapFile, nationalityFile, jsonData):
    mapping = readMapFile(mapFile)
    nationality = readNationalityFile(nationalityFile)
    for key,value in mapping.iteritems():
        if value in nationality:
            jsonData[key - 1]["nationality"] = nationality[value].strip()
    return jsonData

"""
1. Have to read the wikipedia_names file
2. For each line, have to make a document which has keys as languages and value as an array of name variants
3. Have to take the nationalities.txt and store nationality too in the document
"""
def main(inputFile, dataDir, mapFile, nationalityFile, outputFile):
    languages = getLangList(inputFile)
    jsonData = createData(inputFile, languages)
#    jsonData = includeBacklinks(dataDir, languages, jsonData)
#    jsonData = includeNationality(mapFile, nationalityFile, jsonData)
    with open("pretty-" + outputFile, "w") as f:
        json.dump(jsonData, f, sort_keys=True, indent=4)
    with open(outputFile, "w") as f:
        json.dump(jsonData, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess Data")
    parser.add_argument('-i', '--inputFile', action='store', dest='inputFile')
    parser.add_argument('-d', '--dataDir', action='store', dest='dataDir')
    parser.add_argument('-m', '--mapFile', action='store', dest='mapFile')
    parser.add_argument('-n', '--nationalityFile', action='store', dest='nationalityFile')
    parser.add_argument('-o', '--outputFile', action='store', dest='outputFile')

    result = parser.parse_args()

    if not os.path.isfile(result.inputFile):
        print("File: %s does not exists\nAborting...\n" % (result.inputFile))
        exit()
    if not os.path.isdir(result.dataDir):
        print("File: %s does not exists\nAborting...\n" % (result.dataDir))
        exit()
    if not os.path.isfile(result.mapFile):
        print("File: %s does not exists\nAborting...\n" % (result.mapFile))
        exit()
    if not os.path.isfile(result.nationalityFile):
        print("File: %s does not exists\nAborting...\n" % (result.nationalityFile))
        exit()

    main(result.inputFile, result.dataDir, result.mapFile, result.nationalityFile, result.outputFile)
