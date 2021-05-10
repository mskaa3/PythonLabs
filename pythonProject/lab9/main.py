import argparse
import smtplib
import datetime
import requests
from bs4 import BeautifulSoup


def listNames(letter, page_num):

    if page_num == 1:
        page = requests.get('https://wiz.pwr.edu.pl/pracownicy?letter='+letter.upper())
    else:
        page = requests.get('https://wiz.pwr.edu.pl/pracownicy/page'+str(page_num)+'.html?letter=' + letter.upper())

    soup = BeautifulSoup(page.text, 'html.parser')
    last_links = soup.find(class_='row columns clearfix')
    last_links.decompose()
    menu=soup.find(class_='side-menu')
    menu.decompose()
    main = soup.find(class_='home')
    main.decompose()

    name_list = soup.find(class_='row columns').select('a',class_='col-text text-content')
    mail_list = soup.find(class_='row columns').select('p', class_='col-text text-content')

    if len(name_list) == 0:
         print("There is no teacher with a surname starting on letter: "+letter.upper())
    for name, email in zip(name_list, mail_list):
        names = name.contents[0]
        emails = email.contents[0]
        print(f'{names}       {emails}')

    try:
        page_num += 1
        listNames(letter, page_num)
    except:
        pass


def facts(num):
    r = requests.get('https://cat-fact.herokuapp.com/facts')
    fact_list = []
    for fact in r.json():
        fact_list.append(fact['text'])
    if num < 0 or num > len(fact_list):
        print('invalid number of facts')
    else:
        i = 1
        for fact in fact_list:
            if i <= num:
                print(fact)
                i += 1


def read_log(new_file):
    counter = 1
    with open(new_file) as my_file:
        for line in my_file:
            if counter == 1:
                e_adress = line
                counter += 1
            elif counter == 2:
                password = line
            else:
                print("Sorry, the program takes first line as email and second as password, nothimh more")

    send(e_adress, password)


def send(email, passwd):
    smtpSrv = smtplib.SMTP('smtp.gmail.com', 587)
    smtpSrv.starttls()
    smtpSrv.ehlo()
    smtpSrv.login(email, passwd)
    sender = '256519@student.pwr.edu.pl'
    recipient = ['j.moskaaa@gmail.com']
    SUBJECT = f" Hello sir, today is a beatufiful day with a date: " \
              f"{ datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}"
    TEXT = f"""
    FROM: Julia Moska <256519@student.pwr.edu.pl>\n
    TO: Julia Moska<j.moskaaa@gmail.com>\n
    
    Im so happy to announce, that my code is working
    """
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    result = smtpSrv.sendmail(sender, recipient, message)
    smtpSrv.quit()


if __name__ == '__main__':
    argument = argparse.ArgumentParser()
    argument.add_argument('--mail', type=str, help="mail command needed", default='def')
    argument.add_argument('--cat-facts', type=int, help="enter cat facts with a number", default=0)
    argument.add_argument('--teachers', type=str, help="enter teachers and a letter", default='def')
    my_args = argument.parse_args()
    print(my_args)
    if my_args.mail != 'def' and 'My message to the teacher' in my_args.mail:
        print('start')
        read_log('personal.txt')
    if my_args.cat_facts != 0 and type(my_args.cat_facts) == int:
        number = my_args.cat_facts
        facts(number)
    if my_args.teachers != 'def' and type(my_args.teachers) == str:
        letter = my_args.teachers
        listNames(letter, 1)



