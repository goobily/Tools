import os
import sys

def parseFile(searchRule, inputFile):
    with open(inputFile, 'r') as f:
        file_content = f.read()
        file_content.replace(' ','')
        if searchRule in file_content:
            result = inputFile+'\n'
            md5Pos = file_content.find('"md5"', 0, 10000)
            #print 'md5Pos:', md5Pos

           # md5Be = file_content.find(':',md5Pos, md5Pos+8)
           # print 'md5Be:', md5Be
            if md5Pos!= -1:
                md5Pos = md5Pos + len('"md5":')
                #print 'md5Pos:', md5Pos
                md5Be = file_content.find('"', md5Pos, md5Pos+20)
               # print 'md5Be:', md5Be
               # md5Be2 = md5Be+1
                md5End = file_content.find('}', md5Be)
                #print 'md5End:', md5End

            else:
                md5Be = file_content.find('<md5>')
                #print 'md5Be:', md5Be
                md5Be = md5Be+len('<md5>')
                md5End = file_content.find('</md5>', md5Be)
            md5 = file_content[md5Be:md5End]
            #print 'md5:', md5
            result = inputFile+'\tmd5:'+ md5 + '\n'
            return result
    return ""

def parse(searchRule, input, output_file):
    fw = open(output_file, 'w')
    if os.path.isfile(input):
        fw.write(parseFile(searchRule, input))
    elif os.path.isdir(input):
        for root, dirs, files in os.walk(input):
            for file in files:
                filePath = os.path.join(root, file)
                fw.write(parseFile(searchRule,filePath))
    else:
        print "input not exist"
    fw.close()

def main():
    if len(sys.argv)!=4:
        print 'Args: searchRule, inputFile outputFile'
        return
    parse(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()