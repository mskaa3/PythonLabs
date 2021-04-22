import re
import datetime

parse_time = re.compile(
    r"\[(\d{1,2})/([A-Z][a-z]{2})/(\d{4}):(\d{2}):(\d{2}):(\d{2}) \+(\d{4})] ")
def run():
    reader("access_log-20201025.txt")


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

def timeRead(new_list):
    for line in new_list:
        try:
            result = re.search(parse_time, str(line))

        except AttributeError:
            continue




if __name__ == '__main__':
    run()