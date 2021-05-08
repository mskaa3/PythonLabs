import  argparse
import smtplib
import datetime
import requests
from bs4 import BeautifulSoup


def listNames(letter,page_num):

    if page_num==1:
        page=requests.get('https://wiz.pwr.edu.pl/pracownicy?letter='+letter.upper())
    else:
        page = requests.get('https://wiz.pwr.edu.pl/pracownicy/page'+str(page_num)+'.html?letter=' + letter.upper())

    soup = BeautifulSoup(page.text, 'html.parser')

    name_list = soup.find(class_='row columns').find(class_='column-content')
    email_list_items=name_list.find_all('p')
    name_list_items = name_list.find_all('a')
    counter=1
    new_list=[]

    for name in name_list_items:
        if counter>22:
            new_list.append(name)
        counter+=1
    if len(new_list)==0 :
        print("There is no teacher with a surname starting on letter: "+letter.upper())
    for name,email in zip(new_list, email_list_items):
        names=name.contents[0]
        emails=email.contents[0]
        print(f'{names}       {emails}')

    try:
        page_num+=1
        listNames(letter,page_num)
    except:
        pass



def read_log(new_file):
    counter=1
    with open(new_file) as my_file:
        for line in my_file:
            if counter==1:
                e_adress=line
                counter+=1
            elif counter==2:
                password=line
            else:
                print("Sorry, the program takes first line as email and second as password, nothimh more")

    send(e_adress,password)



def send(email, passwd):
    smtpSrv = smtplib.SMTP('smtp.gmail.com', 587)
    smtpSrv.starttls()
    smtpSrv.ehlo()
    smtpSrv.login(email, passwd)
    sender='256519@student.pwr.edu.pl'
    recipient=['j.moskaaa@gmail.com']
    SUBJECT =f" Hello sir, today is a beatufiful day: { datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}"
    TEXT=f"""
    FROM: Julia Moska <256519@student.pwr.edu.pl>\n
    TO: Julia Moska<j.moskaaa@gmail.com>\n
    
    Email sent to check if its working
    """
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    result=smtpSrv.sendmail(sender,recipient,message)
    smtpSrv.quit()






if __name__ == '__main__':
    argument = argparse.ArgumentParser()
    argument.add_argument('--mail', type=str, help="mail command needed", default='def')
    argument.add_argument('--cat-facts', type=int, help="enter cat facts with a number", default=0)
    argument.add_argument('--teachers', type=str, help="enter teachers and a letter", default='def')
    my_args = argument.parse_args()
    print(my_args)
    # if my_args.mail is not 'def' and 'My message to the teacher' in my_args.mail:
    #     print('start')
    #     read_log('personal.txt')
    # if my_args.cat_facts != 0 and type(my_args.cat_facts)==int:
    #     number=my_args.cat_facts
    #     print(number)
    # if my_args.teachers is not 'def' and type(my_args.teachers)==str:
    #     letter=my_args.teachers
        # listNames(letter)


    listNames('e',1)
