import mysql.connector as sql
from collections import Counter #built in
from tabulate import tabulate #pip install tabulate
import time #built in
from tkinter import filedialog as fd #pip install tk


def pwd_check():
    wrong_pwd = True
    global pwd

    while wrong_pwd:
        pwd = input('Enter SQL password for authorization: ')
        try:
            auth = sql.connect(user = 'root', password = pwd)
            if auth.is_connected():
                print('<Authorized>')
                wrong_pwd = False
                break
        except:
            print('Incorrect Password : Access Denied\n')

def file_check():
    file_not_found = True
    global file
    global word_list

    file_auth_key = "auth:13â€‹7b8â€‹9â€‹3f9â€‹2câ€‹1b28â€‹24â€‹138câ€‹17â€‹816â€‹3eâ€‹2644â€‹dâ€‹3f6â€‹5fâ€‹49d9â€‹2eâ€‹1cc0â€‹41â€‹2aa8"
    while file_not_found:
        try:
            print('Open Dataset file...')
            adr = fd.askopenfilename(title='Open Dataset file')
            if not adr:
                exit()
            print('Authenticating...')
            file = open(adr,'r')
            data_set = (((file.read()).lower()).replace('\n',' '))
            word_list = data_set.split()
            if word_list[0] == file_auth_key:   #authentication of correct file
                file_not_found = False
                word_list.remove(file_auth_key)
                print('File contains valid auth key.\n')
                break
            else:
                print('File does not seem to have a valid auth key.')
                time.sleep(30)
        except:
            print('\nError : File address seems to be incorrect.\n')

def db_check():
    try:    #checks for database and creates if not found
        con = sql.connect(user = 'root', password = pwd)
        cur = con.cursor()
        cur.execute('CREATE DATABASE word_dataset;')
        print('Database not found')
        print('Creating Database...')
        con.commit()
        cur.execute('USE word_dataset;')
        con.commit()
        print('Created Database')
    except:
        print('Given Database matches all criteria.')

def tb_check():
    try:    #checks for table and creates if not found
        db = sql.connect(user = 'root', password=pwd, database = 'word_dataset')
    
        mycur = db.cursor()
        mycur.execute('create table dataset(id int PRIMARY KEY, words varchar(200), popularity tinyint);')
        print('Table not found')
        print('Creating Table...')
        print('Created Table')
    except:
        print("Given Table matches all criteria.")

def rec_check():
    try:    #tries to input words into the database
        print('Searching SQL records...')
        time.sleep(1)
        db = sql.connect(user = 'root', password=pwd, database = 'word_dataset')
        mycur = db.cursor()
        

        begin = time.time()
        
        count = 0
        id = 1

        for i in range(len(word_list)):
            word = word_list[i]
            try:
                cmd = f"INSERT INTO dataset VALUES({id},'{word}',0)"
                mycur.execute(cmd)
                db.commit()
                if i == 0:
                    print('SQL records not detected.\nEntering SQL records...(this may take several minutes)\n')
                if i % 4000 == 0:
                    count += 1
                    print(f'{count}% out of 100')
                id += 1
            except:
                raise Exception
        
        end = time.time()
        print(f'Completed in {(int(end-begin))//60} minutes.')
    except:
        print('Words have already been entered into the database.')

def coldStart():
    pwd_check()

    file_check()
    
    db_check()

    tb_check()

    rec_check()

    global db,mycur

    db = sql.connect(user = 'root', password= pwd , database = 'word_dataset')
    mycur = db.cursor()

    print('Initializing done.\n\n')

def find_word():
    msg = input("Enter the word[replace missing letters with '-']: ").lower()
    start = time.time()         #it records the current time
    if msg == '':
        ch = (input("\nExit?[yes/no]: ")).lower()
        if ch == 'yes':
            file.close()
            exit()
        else:
            pass         
        
    lst = list(msg)
    rmsg = msg.replace('-','')  #removes the hyphens
    rst = list(rmsg)
    ans = []
    for i in range(len(word_list)):
        word = list(word_list[i])
        if len(word) == len(lst):  #checks number of letters is same for both words
            if set(rst).issubset(set(word)): #checks if the letters in given word are present in searched word
                for a in range(len(lst)):
                    if lst[a] == word[a]: #checks if the letters indexes are same
                        ans.append(word_list[i])

    c_ans = Counter(sorted(list((ans)))).most_common()#finds most common out of the sorted list
    f_ans = []
    for q in range(len(c_ans)):
        item = list(c_ans[q])
        if item[1] == len(rmsg):    #checks if 'frequncy' attribute is equal to the number of letters in `rmsg`
            f_ans.append(item)

    for e in range(len(f_ans)):
        del f_ans[e][1] #removes the 'frequency' attribute of the most_common() function

    if len(f_ans) != 0 :      #checks if its not empty
        print("\nSearching...\n")
        for i in range(len(f_ans)):
            value = (str(f_ans[i])).replace('[','').replace(']','')
            cmd = f"UPDATE dataset SET popularity = popularity + 1 WHERE words={value};"
            mycur.execute(cmd)
            db.commit()
        end = time.time()       #records the current time
        time_taken = int(end - start)   #amount of time taken; int() removes the decimals
        print(f'{len(f_ans)} results match out of {len(word_list)} ({time_taken}s)')  
        print(tabulate(f_ans,headers=['Possible Words'],tablefmt='fancy_grid'))
    else:
        print("\nNo words were found :/")
    file.close()
    
def most_popular():
    cmd = 'SELECT words,popularity FROM dataset ORDER BY popularity DESC LIMIT 10;'
    mycur.execute(cmd)
    rows = mycur.fetchall()     #list of tuples
    print('\n\t  Top 10 Most Searched Words\n')
    print(tabulate(rows,headers=['Word','Amount Of Times It Was Searched'],tablefmt='fancy_grid'))   #type: ignore


coldStart()         


while True:
    print(f"Searching {len(word_list)} words to help you!")
    ch = input('1.Find word \n2.find Top 10 most searched words \n3.Exit \nEnter choice:')
    if ch == '1':
        find_word()
    elif ch == '2':
        most_popular()
    elif ch == '3':
        input('Exited')
        exit()
    else:
        print('Invalid Input!!!\n')
