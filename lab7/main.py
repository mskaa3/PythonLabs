import re
import datetime
parse = re.compile(
    r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - - "             
    # IP ADRESS group 1
    r'\[(\d{1,2}/[A-Z][a-z]{2}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})] '
    # TIMESTAMP group 2
    r'\"([A-Z]{3,7}) (/.+\.[a-z]*) ([H][T][T][P]/[0-9]?\.?[0-9]?)\" '
    #REQUEST METHOD(group 3) AND RESOURCE(group4) AND HTTP(group5) 
    r'(\d{3}) (\d{3})')
    #HTTP STATUS CODE(group6) AND SIZE(group7)


def run():
    my_list = file_reader("access_log-20201025.txt")
    # print_all(my_list)
    line = '5.45.207.78 - - [18/Oct/2020:04:11:32 +0200] "GET /robots.txt HTTP/1.1" 301 238 "-" ' \
           '"Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"'
    new = logHeader(line)
    print(new.requestedResource)
    print(new.requestType)
    print(new.__str__())
    between_time(my_list, '18/Oct/2020:04:11:32 +0200', '18/Oct/2020:08:07:19 +0200')


def file_reader(new_file):
    new_list = []
    counter = 0
    try:
        with open(new_file) as file:
            for line in file:
                try:
                    new_list.append(line_reader(str(line)))
                except MalformedHTTRequest:
                    counter = counter+1
                    continue
    except FileNotFoundError:
        print('File not found')
        exit()

    print(f'Malformatted requests number: {counter}')
    return new_list


def line_reader(line):
    new_object = logEntry(line)
    return new_object


def time_read(timestamp):
    return datetime.datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')


class logHeader:
    def __init__(self, log):
        parser = re.match(parse, log)
        if parser is not None:
            self.requestType = parser.group(3)
            self.requestedResource = parser.group(3) + parser.group(4)
        else:
            raise MalformedHTTRequest

    def __str__(self):
        return f"Request type: {self.requestType}, Requested resource: {self.requestedResource}"

    def get_request_type(self):
        return self.requestType

    def get_requested_resource(self):
        return self.requestedResource


class logEntry:
    def __init__(self, log):

        parser = re.match(parse, log)
        if parser is not None:
            self.ip_adress = parser.group(1)
            self.timestamp = time_read(parser.group(2))
            self.request_type = parser.group(3)
            self.status = parser.group(6)
            self.size = parser.group(7)
        else:
            raise MalformedHTTRequest

    def print_out(self):
        print(self.__str__())

    def get_timestamp(self):
        return self.timestamp

    def __str__(self):
        return f"IP adress: {self.ip_adress}, timestamp: {self.timestamp}" \
               f", Type of request: {self.request_type}, HTTP status: {self.status}" \
               f", Size of the request: {self.size}"


def between_time(my_list, first_date, second_date):
    t1 = time_read(first_date)
    t2 = time_read(second_date)

    if t1 > t2:
        print("Second date is earlier than a first one")
    else:
        print(f"All requests between {t1} and {t2} are:\n")
        for item in my_list:
            if t1 < item.timestamp < t2 :
                item.print_out()
#im assuming we are printing out all PROPER requests between these times


def print_all(my_list):
    for item in my_list:
        item.print_out()


class MalformedHTTRequest(Exception):
    pass


if __name__ == '__main__':
    run()