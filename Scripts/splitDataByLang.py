import argparse
import os
import codecs
import json

from collections import defaultdict

def readData(inputFilePath):
    print("reading")
    with open(inputFilePath, "r") as f:
        data = f.read()
    return data

def parseData(data, limit):
    print("parsing")
    lines = data.strip().split('\n')
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
    return tags,parse_data

def writeSpecificData(data, sourceFile, targetFile):
    f_source = open(sourceFile, "w")
    f_target = open(targetFile, "w")

    for item in data:
        f_source.write(item[0] + "\n")
        f_target.write(item[1] + "\n")

    f_source.close()
    f_target.close()

def writeData(tags, data, outputDir, targetLang):
    print("writing")
    for tag in tags:
        print(tag)
        if tag != targetLang:
            path = os.path.join(outputDir, targetLang, tag + "_" + targetLang)
            if os.path.isdir(path):
                continue
            os.mkdir(path)
            specific_lang_data = []
            for item in data:
                if tag in item:
                    if item[tag] != "" and item[targetLang] != "":
                        specific_lang_data.append([item[tag], item[targetLang]])
            writeSpecificData(specific_lang_data, os.path.join(outputDir, tag + "_" + targetLang, tag), os.path.join(outputDir, tag + "_" + targetLang, targetLang))

def main(inputFilePath, outputDir, targetLang):
    data = readData(inputFilePath)
    (tags_data,parsed_data) = parseData(data, -1)
    if targetLang not in tags_data:
        print("Not a valid target language")
        return 1
    writeData(tags_data, parsed_data, outputDir, targetLang)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Data")
    parser.add_argument('-i', '--inputFile', action='store', dest='inputFilePath')
    parser.add_argument('-o', '--outputFile', action='store', dest='outputDir')
    parser.add_argument('-t', '--targetLang', action='store', dest='targetLang', default='en')

    result = parser.parse_args()

    if not os.path.isfile(result.inputFilePath):
        print("File: %s does not exists\nAborting...\n" % (result.inputFilePath))
        exit()
    if not os.path.isdir(result.outputDir):
        print("Directory: %s does not exists. Do you want to create one (y/n): " % (os.path.join(result.outputDir, targetLang)))
        response = raw_input("")
        if response == "n":
            exit()
        else:
            os.mkdir(os.path.join(result.outputDir, targetLang))

    main(result.inputFilePath, result.outputDir, result.targetLang)



