import  argparse
import os
import smtplib
import datetime

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
    argument.add_argument('--mail', type=str, help="mail command needed", default='nmnnmnmn')
    my_args = argument.parse_args()
    print(my_args)
    if 'My message to the teacher' in my_args.mail:
        print('start')
        read_log('personal.txt')

