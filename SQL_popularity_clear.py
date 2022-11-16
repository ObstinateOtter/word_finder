import mysql.connector as sql
import time #built in
db = sql.connect(user = 'root', password='db pwd', database = 'word_dataset')
mycur = db.cursor()

mycur.execute('SELECT * FROM dataset WHERE popularity > 0;')
amount = mycur.fetchall()
begin = time.time()
print('\nso it begins...')

for i in range(len(amount)):   #type: ignore
    cmd = 'UPDATE dataset SET popularity = 0 WHERE popularity > 0;'
    mycur.execute(cmd)
    db.commit()

end = time.time()
print(f'Time taken: {end-begin}')
