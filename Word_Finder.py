from collections import Counter
from tabulate import tabulate
import time
h = ['Possible Words']

file = open(r"C:\Users\MysticMeerkat\Desktop\Desktop\Code Projects\Python programs\word_finder\words_dataset.txt",'r')
data_set = (((file.read()).lower()).replace('\n',' '))
word_list = data_set.split()




def find_word():
    msg = input("Enter the word[replace missing letters with '-']: ").lower()
    if msg == '':
        ch = (input("\nExit?[yes/no]: ")).lower()
        if ch == 'y':
            file.close()
            exit()
        else:
            pass         

        
    lst = list(msg)
    rmsg = msg.replace('-','')
    rst = list(rmsg)
    ans = []
    for i in range(len(word_list)):
        word = list(word_list[i])
        if len(word) == len(lst):  #checks number of letters is same for both words
            if all(a in word for a in rst): #checks if the letters in given word are present in searched word
                for a in range(len(lst)):
                    if lst[a] == word[a]: #checks if the letters indexes are same
                        ans.append(word_list[i])

    c_ans = Counter(sorted(list((ans)))).most_common()#finds most common out of the sorted list
    f_ans = []
    for q in range(len(c_ans)):
        item = list(c_ans[q])
        if item[1] >= len(rmsg):    
            f_ans.append(item)

    for e in range(len(f_ans)):
        del f_ans[e][1] #removes the 'frequency' attribute of the most_common() function

    print("\nSearching...\n")
    time.sleep(1)               #just for sum 'anticipation'

    count = len(f_ans)
    print(count,"results match out of",len(word_list))
    if len(ans) != 0 :
        print(tabulate(f_ans,headers=h,tablefmt='fancy_grid'))
    else:
        print("\nNo words were found(>_<)")
    file.close()
    find_word()
            
find_word()
