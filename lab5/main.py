import json
import logging

httpMethod = ("PUT", "OPTIONS", "CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "TRACE")
names = {"webserverName",
         "httpName",
         "logLevel",
         "numOfLines",
         "ownParameter"}


def run():
    read_log()


def read_log():
    try:
        with open("configFile.json") as file:
            try:
                newFile = json.load(file)
                try:

                    for key in newFile:
                        if key is None:
                            raise ValueError("Values cannot be empty")
                        if key not in names:
                            raise ValueError("Missing parameter")
                except ValueError as ve:
                    print(ve)
                    quit()
                except FileNotFoundError:
                    print("The logging file doesn't exist")
                    quit()
            except IOError:
                print('Not a proper JSON file')
                quit()
    except FileNotFoundError:
        print('No such file')
        quit()
    setLogger(newFile["logLevel"])
    reader(newFile)
    printAll(newFile)
    websiteRequests(newFile)


def setLogger(typeLog):
    myLogger = logging.getLogger("myLogger")
    myLogger.setLevel(typeLog.upper())
    print("Current logging level is:" + typeLog)


def reader(newFile):
    getList = []
    headerList = []
    for line in open(newFile["webserverName"]):
        #httpMethod = ("PUT", "OPTIONS", "CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "TRACE")
       if any(method in line for method in httpMethod):
        # for method in httpMethod:
        #     if method in line :
                if'index.xml' in line:
                    if line not in getList:
                        getList.append(line)
                        # print("================================================================")
                        # print(line)

    for line in getList:  # for each key in dictionary
        start = line.find(" \"") + len(" \"")
        end = line.find("\" ")
        substring = line[start:end]
        newList = substring.split('/')

        headerList.append(newList)

    for line in headerList:
        start = line[1].find("i")
        end = line[1].find("l") + len("l")
        substring = line[1][start:end]
        print(line[0] + ' ' + substring)


def printAll(newFile):
    method = newFile["httpName"]
    num = newFile["numOfLines"]
    emptyList = []
    counter = -1

    for line in open(newFile["webserverName"]):
        if method.upper() in line:
            emptyList.append(line)

    for line in emptyList:
        counter = counter+1
        if counter == num:
            input("Press anything to continue...")
            counter = 0
        print(line)


def websiteRequests(newFile):
    web = newFile["ownParameter"]

    webList = []

    for line in open(newFile["webserverName"]):
        if web in line:
            webList.append(line)

    if len(webList) == 0:
        print(f"I'm sorry but there is no request for a given website address: {web}")
    for line in webList:
        print(line)
    print(f"Total requests number for the website is {len(webList)}")


if __name__ == '__main__':
    run()
