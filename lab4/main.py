def run():
    x = read_log()
    # y = ip_requests_number(x)
    # print(ip_find(y))
    # print(ip_find(x, False))
    # print()
    # print(longest_request(x))
    print(non_existent(x))


def read_log():
    dictionary = {}

    with open("access_log-20201025.txt") as file:
        for line in file:
            splitted = line.split(" - - ")



            dictionary.setdefault(splitted[0], []).append(splitted[1])
    #
    # for i in dictionary:
    #     print(i, dictionary[i])
    #     print()
    # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    return dictionary


def ip_requests_number(dictionary):
    newDictionary = {}
    for ip in dictionary:
        newDictionary[ip] = len(dictionary[ip])

    # for i in newDictionary:
    #     print("result" ,i, newDictionary[i])
    #     print()
    return newDictionary


def ip_find(dictionary, mostActive=True):
    for line in dictionary:
        if type(dictionary[line]) is int:  # if we pass a dictionary with a number of requests for each ip
            # print("Dictionary with number of requests as a parameter")
            break
        else:
            # print("Dictionary with list of requests as a parameter redirected to counting requests...")
            return ip_find(ip_requests_number(dictionary),
                           False)  # if we pass a dictionary with just ip's and list of requests
    list = []
    if mostActive:

        maxVal = max(dictionary.values())
        # max_key = max(dictionary, key=dictionary.get)
        for line in dictionary:
            if dictionary[line] == maxVal:
                list.append(line)
        print("With the biggest number of ip requests:")
        return list
    else:
        minVal = min(dictionary.values())
        for line in dictionary:
            if dictionary[line] == minVal:
                list.append(line)
        print("With the smallest number of ip requests:")
        return list

def longest_request(dictionary):

    maxVal=0
    lineMaxVal=0
    globalMaxVal=0
    ip=0
    myRequest=""

    for line in dictionary:   #for each key in dictionary
        for request in dictionary[line]:  #for each request in values of key
            s = request
            start = s.find(" \"")+ len(" \"")
            end = s.find("\" ")
            substring = s[start:end]
            maxVal=len(substring)
            if maxVal>lineMaxVal:
                lineMaxVal=maxVal
                myRequest=request
        if lineMaxVal>globalMaxVal:
            globalMaxVal=lineMaxVal
            ip=line
    return ip +" with a string " + myRequest

def non_existent(dictionary):
    list=[]

    for line in dictionary:  # for each key in dictionary
        for request in dictionary[line]:  # for each request in values of key
            s = request
            start = s.find("\" ") + len(" \"")
            end= start+3
            substring = s[start:end]
            # print(substring)
            if substring=="404":
                if request not in list:
                    list.append(request)

    return list



if __name__ == '__main__':

    run()
