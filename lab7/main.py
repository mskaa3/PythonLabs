import re
import datetime
parse = re.compile(
    r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - - "             
    # IP ADRESS
    "\[(\d{1,2}/[A-Z][a-z]{2}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})] "
    # TIMESTAMP
    "\"([A-Z]{3,7}) (\/.+\.[a-z]*) ([H][T][T][P])/(?:[0-9].[0-9])?"
    #REQUEST METHOD AND RESOURCE
    "\" (\d{3}) (\d{3})")
    #HTTP CODE AND SIZE


def run():
    # reader("access_log-20201025.txt")
    line='45.148.121.85 - - [18/Oct/2020:03:22:43 +0200] "HEAD /robots.txt HTTP/1.0" 301 - "-" "-"'
    new=log_header(line)
    print(new.requestedResource)
    print(new.requestType)
    print(new.__str__())

# def reader(new_file):
#     new_list = []
#     try:
#         with open(new_file) as file:
#             for line in file:
#
#                 new_list.append(str(line))
#
#     except FileNotFoundError:
#         print('File not found')
#         exit()
#
#     return new_list

def timeRead(timestamp):

    return datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')


class log_header:
    def __init__(self,log):
        try:
            parser = re.match(parse, log)
            self.requestType=parser.group(3)
            self.requestedResource=parser.group(3)+parser.group(4)

        except:
            print("error gonna fix later the exception")

    def __str__(self):
        return f"Request type: {self.requestType}, Requested resource: {self.requestedResource}"


    def get_request_type(self):
        return  self.requestType


    def get_requested_resource(self):
        return  self.requestedResource


class log_entry:
    def __init__(self,log):
        try:
            parser = re.match(parse, log)
            self.ip_adress=parser.group(1)
            self.timestamp=parser.group(2)
            self.requestType = parser.group(3)
            self.size=parser.group()

        except:
            print("error gonna fix later the exception")




if __name__ == '__main__':
    run()