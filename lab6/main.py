import re
import logging

headerList = ["\\[Display]", "\\[Config]", "\\[LogFile]"]
parse = re.compile(
    "(\\d{1,3}.\\d{1,3}.\\d{1,3}.\\d{1,3}) - - "
    "\\[(\\d{1,2}/[A-Z][a-z]{2}/\\d{4}:\\d{2}:\\d{2}:\\d{2} \\+\\d{4})] "
    "\"([A-Z]{3,7}) (.*[1-9]\" )(\\d{3}) (\\d{3})")


def run():
    read_log()


def read_log():
    # try:
    file_content = re.compile("(.*)=(.*\\.[A-Za-z]*)")
    content = re.compile("(.*)=(.*)")
    matcher = ""
    what_do_i_have = []
    dictionary = {}
    try:
        with open("lab6.config") as file:
            for line in file:
                cont = content.match(line)
                file_match = file_content.match(line)
                if "[Display]" in matcher and cont is not None:
                    dictionary[cont.group(1)] = cont.group(2)
                    what_do_i_have.append('dictionary')

                elif "[LogFile]" in matcher and file_match is not None:
                    file_name = cont.group(2)
                    print(file_name)
                    what_do_i_have.append('filename')

                elif "[Config]" in matcher and cont is not None:
                    my_logger = logging.getLogger("my_logger")
                    log_level = cont.group(2)
                    my_logger.setLevel(log_level)
                    print(f"Current logging level is: {my_logger.level}")
                    what_do_i_have.append('loglevel')

                else:
                    for item in headerList:
                        header = re.compile(item)
                        if header.match(line) is not None:
                            matcher = item

    except FileNotFoundError:
        print('File not found')
        exit()

    if 'filename' not in what_do_i_have:
        file_name = "access_log-20201025.txt"
        print(f"Default file: {file_name}")
        # print(dictionary.items())
    if 'loglevel' not in what_do_i_have:
        my_logger = logging.getLogger("my_logger")
        my_logger.setLevel("INFO")
        print("Default logging level:Info")
        # print(dictionary.items())
    if 'dictionary' not in what_do_i_have:
        dictionary = {'lines': 3, 'separator': '-', 'filter': 'GET'}
        print(f"Default dictionary {dictionary.items()}")
    else:
        print(dictionary.items())

    use = reader(file_name)
    parse_lines(use)
    print_requests(use, '193.27.228.27', dictionary['lines'])
    bytes_number(use, dictionary['filter'], dictionary['separator'])


def reader(new_file):
    new_list = []
    try:
        with open(new_file) as file:
            for line in file:
                new_list.append(str(line))

    except FileNotFoundError:
        print('File not found')
        exit()

    return new_list


def parse_lines(new_list):
    tuples_list = []
    for line in new_list:
        if parse_line(line) is not None:
            tuples_list.append(parse_line(line))
    for line in tuples_list:
        print(line)


def parse_line(line):
    # parse in the head of the file
    try:
        result = re.search(parse, str(line))
        line_list = (result.group(1), result.group(2),
                     result.group(3), int(result.group(5)),
                     int(result.group(6)))
        return line_list
    except AttributeError:
        line_list = None


def print_requests(new_file, new_ip, lines):
    dictionary = {}

    for line in new_file:
        split_line = line.split(" - - ")
        dictionary.setdefault(split_line[0], []).append(split_line[1])
    ip_num = '193.27.228.11'
    # hardcoded means written directly, not changing depending on the situation
    subnet_mas_len = 256519 % 16 + 8
    print(subnet_mas_len)
    counter = -1
    if new_ip in dictionary:
        for item in dictionary[new_ip]:
            counter = counter + 1
            if counter == int(lines):
                input("Press anything to continue...")
                counter = 0
            print(item)
    ip_num_bit = change_ip(ip_num)
    new_ip_bit = change_ip(new_ip)
    # print(ipNumBit)
    # print(newIpBit)
    print(check_subnet(ip_num_bit, new_ip_bit, subnet_mas_len))


def check_subnet(ip1, ip2, subnet):
    counter = 0
    for elem, elem2 in zip(ip1, ip2):
        if elem == elem2:
            counter += 1
            if counter == subnet:
                return True
        else:
            return False


def change_ip(ip_num):
    n = 0
    val = 1
    little_array = []
    powers_array = []
    ip_parse = re.compile("(\\d{1,3}).(\\d{1,3}).(\\d{1,3}).(\\d{1,3})")
    result = re.search(ip_parse, ip_num)
    array = [int(result.group(1)), int(result.group(2)),
             int(result.group(3)), int(result.group(4))]
    print(array)
    for elem in array:
        while elem != 0:
            while val * 2 <= elem:
                val = val * 2
                n += 1

            elem = elem - val
            little_array.append(n)
            val = 1
            n = 0
        powers_array.append(little_array)
        little_array = []
    bit_array = []
    little_bit_array = []
    count = 0
    for elem in powers_array:
        elem.reverse()
        for num in elem:
            while count < num:
                little_bit_array.append(0)
                count += 1
            little_bit_array.append(1)
            count += 1
        count = 0
        while len(little_bit_array) < 8:
            little_bit_array.append(0)
        little_bit_array.reverse()
        bit_array = bit_array + little_bit_array
        little_bit_array = []
    return bit_array


def bytes_number(new_file, my_filter, separator):
    my_sum = 0
    for line in new_file:
        try:
            header = re.compile(my_filter)
            if header.search(str(line)):
                result = re.search(parse, str(line))
                my_sum = my_sum + int(result.group(6))
        except AttributeError:
            continue
    print(f"{my_filter} {separator} {my_sum}")


if __name__ == '__main__':
    run()


# FIRST RUN:
# (venv) C:\Users\julia\PycharmProjects\lab6>pycodestyle main.py
# main.py:6:80: E501 line too long (115 > 79 characters)
# main.py:30:80: E501 line too long (85 > 79 characters)
# main.py:100:80: E501 line too long (115 > 79 characters)
# main.py:134:13: E117 over-indented
# main.py:149:80: E501 line too long (100 > 79 characters)
#
#
#
#
#
#
#
# LAST RUN(ALL PROBLEMS RESOLVED):
# (venv) C:\Users\julia\PycharmProjects\lab6>

