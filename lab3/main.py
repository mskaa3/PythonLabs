import logging
import sys
logging.basicConfig(level=logging.DEBUG)
adresses=[]
num=[]
bytes=[]
time=[]



def run():
    read_log()

def read_log():
       count = 0
       entriesCount = 0
       wrongCount=0
       list=[]

       for line in sys.stdin:

            splitted = line.split(" ")
            if len(splitted) == 4 and "/" in splitted[0]:
                adresses=str(splitted[0])
                num=int(splitted[1])
                bytes=(int(splitted[2]))
                time=(int(splitted[3]))
                newList=(adresses, num,bytes,time)
                count=count+1

                entriesCount=entriesCount+1

                list.append(newList)
            elif line == "\n":
                count = count + 1

            else:
                count = count + 1
                wrongCount=wrongCount+1
                logging.error(f"wrong format of a line number {count} : {line}.Should contain 4 atributes")




       logging.debug(f"Total number of lines(includig empty and wrong formatting) {count}")
       logging.debug(f"Total number of lines(without the wrong formatting) {count-wrongCount}")
       logging.debug(f"Number of entries {entriesCount}")
       successful_reads(list)
       failed_reads(list)
       print_html_entries(list)


def successful_reads(list):

    newList=[]
    for part in list:
        if part[1]/100==2:
            newList.append(part[1])
    logging.info(f"Num of proper entries: {len(newList)}")
    return newList

def failed_reads(list):
    newList4 = []
    newList5 = []
    for part in list:
        if int(part[1] / 100) == 4:
            newList4.append(part[1])
        elif int(part[1] / 100) == 5:
            newList5.append(part[1])

    newList=newList4+newList5
    logging.info(f"Num of failed entries with 4xx code: {len(newList4)}")
    logging.info(f"Num of failed entries with 5xx code: {len(newList5)}")
    return newList

def html_entries(list):
    newList=[]
    for part in list:
        if ".html" in part[0]:   #endswith
            newList.append(part[0])
    # logging.info(f"HTML entries are {newList}")
    return newList

def print_html_entries(list):
    print(html_entries(list))

if __name__ == '__main__':
    run()

    # ones with a reading from standard input might be used just once, others multiple times.


