import argparse
import os
import json

def readFromFile(filePath):
    print("reading")
    with open(filePath, "r") as f:
        data = json.load(f)
    return data

def writeData(outputDir, data):
    for k,v in data.iteritems():
        filePath = os.path.join(outputDir, str(k))
        print("File: %s\n" %(filePath))
        with open(filePath, "w") as f:
            json.dump(v, f, sort_keys=True, indent=4)

def augmentNationalities(nationalities):
    indian_set = {"india", "indian", "hindi", "hindustan", "pakistani", "bangladeshi", "lankan", "tamil", "bengali", "marathi"}
    english_set = {"states", "united states", "english", "american", "british", "australian", "canadian", "us", "pennsylvania"}
    augmentedNationalities = {}
    for item in nationalities:
        if item.lower() in indian_set:
            for syn in indian_set:
                if syn in augmentedNationalities:
                    break
                augmentedNationalities[syn] = nationalities.index(item)
        elif item.lower() in english_set:
            for syn in english_set:
                if syn in augmentedNationalities:
                    break
                augmentedNationalities[syn] = nationalities.index(item)
        else:
            if item.lower() not in augmentedNationalities:
                augmentedNationalities[item.lower()] = nationalities.index(item)
    return augmentedNationalities

def main(inputFilePath, nationalities, outputDir):
    data = readFromFile(inputFilePath)
    nationalities = augmentNationalities(nationalities)
    print(nationalities)
    outputData = {}
    for item in data:
        if "nationality" in item:
            if item["nationality"].lower() in nationalities:
                if nationalities[item["nationality"].lower()] not in outputData:
                    outputData[nationalities[item["nationality"].lower()]] = []
                outputData[nationalities[item["nationality"].lower()]].append(item)
    writeData(outputDir, outputData)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Data by nationalities")
    parser.add_argument('-i', '--inputFilePath', action='store', dest='inputFilePath')
    parser.add_argument('-n', '--nationalities', action='store', dest='nationalities', nargs='+')
    parser.add_argument('-o', '--outputDir', action='store', dest='outputDir')

    result = parser.parse_args()

    if not os.path.exists(result.inputFilePath):
        print("Error %s: does not exists" %(result.inputFilePath))
        exit()
    if not os.path.isdir(result.outputDir):
        print("Directory: %s does not exists. Do you want to create one (y/n): " % (result.outputDir))
        response = raw_input("")
        if response == "n" or response == "no":
            exit()
        else:
            os.makedirs(result.outputDir)

    main(result.inputFilePath, result.nationalities, result.outputDir)
