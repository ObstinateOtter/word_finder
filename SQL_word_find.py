import mysql.connector as sql
from collections import Counter #built in
from tabulate import tabulate #pip install tabulate
import time #built in
db = sql.connect(user = 'root', password='db pwd', database = 'word_dataset')
mycur = db.cursor()

file = open(r"file address",'r')
data_set = (((file.read()).lower()).replace('\n',' '))
word_list = data_set.split()

h = ['Possible Words']

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
        print(f'{len(f_ans)} results match out of {len(word_list)} ({time_taken}s)')   #print('L bozo',value) -> print(f'L bozo {value}')
        print(tabulate(f_ans,headers=h,tablefmt='fancy_grid'))
    else:
        print("\nNo words were found 🐣")
    file.close()
    
def most_popular():
    cmd = 'SELECT words,popularity FROM dataset ORDER BY popularity DESC LIMIT 10;'
    mycur.execute(cmd)
    rows = mycur.fetchall()     #list of tuples
    print('\n\t  Top 10 Most Searched Words\n')
    print(tabulate(rows,headers=['Word','Amount Of Times It Was Searched'],tablefmt='fancy_grid'))   #type: ignore
    


while True:
    ch = int(input('1.Find word \n2.find Top 10 most searched words \n3.Exit \nEnter choice:'))
    if ch == 1:
        find_word()
    elif ch == 2:
        most_popular()
    elif ch == 3:
        exit()
    else:
        print('Invalid Input!!!\n')
