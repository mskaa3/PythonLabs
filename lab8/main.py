import argparse
import csv
import re
import xlsxwriter


# https://www.kaggle.com/mylesoneill/world-university-rankings

parse = re.compile(r'.+\.[c][s][v]')


class elem:
    def __init__(self, line):
        self.world_rank = int(line['world_rank'])
        self.uni_name = str(line['institution'])
        self.country = str(line['country'])
        self.national_rank = int(line['national_rank'])
        self.quality_ed = int(line['quality_of_education'])
        self.employment = int(line['alumni_employment'])
        self.publications = int(line['publications'])
        self.citations = int(line['citations'])
        self.patents = int(line['patents'])
        self.total_score = float(line['score'])

    def getName(self):
        return self.uni_name

    def getCountry(self):
        return self.country

    def getWorldRank(self):
        return self.world_rank

    def getNationalRank(self):
        return self.national_rank

    def getQualityEducation(self):
        return self.quality_ed

    def getEmployment(self):
        return self.employment

    def getPublications(self):
        return self.publications

    def getCitations(self):
        return self.citations

    def getTotalScore(self):
        return self.total_score

    def getPatents(self):
        return self.patents

    def __str__(self):
        return f' World Rank: {self.world_rank}, Univeristy name: {self.uni_name} with total score of {self.total_score}, '\
               f'Country Name: {self.country}, National Rank: {self.national_rank}, Alumni employment rank: {self.employment} '\
               f'Educational quality rank: {self.quality_ed}, number of publications rank: {self.publications}, ' \
               f'number of citations rank: {self.citations}, number of patents raank: {self.patents}'\



# all my data are basically rankings so it was hard to find anything avarage for whole set od data, therefore
# i've decided to make more specified assumption
def avarageOfRank(my_list):
    counter = 0
    new_sum = 0
    for line in my_list:
        if 'USA' in line.getCountry():
            new_sum = new_sum+line.getWorldRank()
            counter += 1
    avg = round(new_sum / counter)
    print(f"Avarage world rank for all {counter} Universities placed in America is {avg}")
    return avg


# number of universties from each country
def numOfUniversities(my_list):
    dictionary = {}
    for obj in my_list:
        if obj.getCountry() not in dictionary:
            dictionary[obj.getCountry()] = 1
        else:
            dictionary[obj.getCountry()] += 1

    for line in dictionary:
        print(f'Number of universities in {line} is {dictionary[line]}')
    return dictionary


# Total number of countries in ranking
def summary(my_list):
    new_list = []
    counter = 0
    for obj in my_list:
        if obj.getCountry() not in new_list:
            new_list.append(obj.getCountry())
            counter += 1
    return f'Total number of countries in ranking {counter}'


#General summary for a given country
def countrySummary(my_list, country_name):
    counter = 0
    world_sum = 0
    points_sum = 0
    higher_rank = 10000
    best_uni = ''
    employee_sum = 0
    patents_sum = 0
    publications = 0
    citations = 0
    for line in my_list:
        if str(country_name) in line.getCountry():
            if line.getWorldRank() < higher_rank:
                higher_rank = line.getWorldRank()
                best_uni = str(line.getName())

            world_sum = world_sum + line.getWorldRank()
            points_sum = points_sum+line.getTotalScore()
            employee_sum = employee_sum+line.getEmployment()
            patents_sum = patents_sum+line.getPatents()
            publications = publications+line.getPublications()
            citations = citations+line.getCitations()
            counter += 1

    score = points_sum / counter
    avg_rank = round(world_sum / counter)
    avg_patents = round(patents_sum / counter)
    avg_employees = round(employee_sum / counter)
    avg_publications = round(publications / counter)
    avg_citations = round(citations / counter)
    # print( f'Summary for {country_name}. The best uni is {best_uni} with a world rank: {higher_rank}. Avarage total score for ' \
    #        f'all universities is {score} and avarage ranking is {avg_rank}. Avarage rank in: ' \
    #        f'employment ranking is :{avg_employees}, in patents ranking is: {avg_patents},' \
    #        f'in publications ranking: {avg_publications}, in citations ranking: {avg_citations}. ')

    return [best_uni,score,avg_rank]


def read_log(new_file):
    new_list = []
    parser = re.match(parse, new_file)
    if parser is not None:
        try:
            with open(new_file) as my_file:
                reader = csv.DictReader(my_file)
                for line in reader:
                     new_object = elem(line)
                     new_list.append(new_object)

        except FileNotFoundError:
            print('File not found')
            exit()

        return new_list
    else:
        print("Required extension is .csv")
        raise wrongExtensionType


class wrongExtensionType(Exception):

    pass

def excelFile(file,excel_name):
    workbook = xlsxwriter.Workbook(excel_name)
    bold = workbook.add_format({'bold': True})
    font_format = workbook.add_format()
    font_format.set_font_color('red')
    cell_format=workbook.add_format()
    cell_format.set_bg_color('green')
    italic=workbook.add_format({'italic':True})
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Country',bold)
    worksheet.write('B1', 'Avg total score',cell_format)
    worksheet.write('C1', 'Avg world ranking',italic)
    worksheet.write('D1', 'Best Uni',font_format)
    i=2
    n=[]
    countrylist=[]
    for line in file:
        if line.getCountry() not in countrylist:
            n=countrySummary(file,line.getCountry())
            worksheet.write('A'+str(i), line.getCountry(),bold)
            worksheet.write('B' + str(i), n[1],cell_format)
            worksheet.write('C' + str(i), n[2],italic)
            worksheet.write('D' + str(i), n[0],font_format)
            countrylist.append(line.getCountry())
            n.clear()
            i+=1

    workbook.close()

if __name__ == '__main__':
    argument = argparse.ArgumentParser()
    argument.add_argument('file_name', type=str, help="Name of the file needed")
    argument.add_argument('-o', help="Save result in excel")
    my_args = argument.parse_args()

    my_file = my_args.file_name
    mylist=read_log(my_file)
    if 'o' in my_args and my_args.o is not None:
        excel_name = my_args.o
        print(f'I entered the if condition and i want my excel file to be names as:{excel_name}')
        excelFile(mylist,excel_name)
    else:
        print(summary(mylist))

    # for line in mylist:
    #     print(line.__str__())
    # numOfUniversities(mylist)
    avarageOfRank(mylist)
    # countrySummary(mylist, 'Poland')
    # countrySummary(mylist, 'Brazil')
    # countrySummary(mylist, 'USA')





