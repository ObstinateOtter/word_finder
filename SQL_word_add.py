import mysql.connector as sql
import time #built in
db = sql.connect(user = 'root', password='pwd', database = 'word_dataset')
mycur = db.cursor()

file = open(r"words_dataset.txt",'r')
data_set = (((file.read()).lower()).replace('\n',' '))
word_list = data_set.split()


begin = time.time()
print('\nso it begins...')
for i in range(len(word_list)):
    cmd = "INSERT INTO dataset VALUES('{}',0)".format(word_list[i])
    mycur.execute(cmd)
    db.commit()
end = time.time()
print(f'Time taken: {int(end-begin)}')
