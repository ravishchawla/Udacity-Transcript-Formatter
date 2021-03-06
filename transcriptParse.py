import os
from zipfile import ZipFile

#Place all .zip files from Udacity in the directory you specify below:
inputDirectory = "transcripts/"

#The formatted .txt files from each of the lessons will be saved in the directory you specify below:
outputDirectory = "parsedTranscripts/"

def parseTranscript(inputLines, outputFile, justify = True, length = 105):
    if leftJustify:
        data = [""] + [line.decode("utf8").strip() for line in inputLines]
    else:
        data = [""] + [line.decode("utf8") for line in inputLines]
        
    lines = [""]
    line_num = 1
    for i in range(len(data)):
        line = data[i]
        if line.find("-->") > -1:
            continue;
        elif line.strip() == str(line_num):
            line_num = line_num + 1;
        else:
            lines.append(line.replace('\n', '') + " ")
    
    text = " ".join(lines)
    
    if justify:
        lines = leftJustify(text, length)
        
    for line in lines:
        line = line.strip();
        if len(line) > 0:
            outputFile.write(str(line.encode('ascii', 'ignore')))

def leftJustify(text, lineLength):
    done = False
    output = []
    words = text.split(" ")
    while not done:
        line = ""
        
        while len(line) < lineLength:
            line += words.pop(0) + " "
            if len(words) == 0:
                break

        output.append(line + "\n")
            
        if len(" ".join(words)) < lineLength:
            done = True
            output.append(" ".join(words))

    return output
        


def checkOrMake(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
lessonZips = []

for root, dirs, files in os.walk(inputDirectory):
    for f in files:
        if f.endswith(".zip"):
            lessonZips.append(f[:-4])

checkOrMake(outputDirectory)

for lesson in lessonZips:
    checkOrMake(outputDirectory + lesson + "/")
    zipFile = ZipFile(inputDirectory + lesson + ".zip", "r")
    transcriptList = ZipFile.namelist(zipFile)
    for transcript in transcriptList:
        transcriptName = transcript[:-4]
        
        inputFile = zipFile.open(transcript, "r")
        inputLines = inputFile.readlines()
        outputFile = open(outputDirectory + lesson + "/" + transcriptName + ".txt", "w")
        
        parseTranscript(inputLines, outputFile)
        
        inputFile.close()
        outputFile.close()