import MySQLdb as sql
import hashlib
import time

db = sql.connect(host="localhost",  
					 user="root",	   
					 passwd="", 
					 db="lista")  
cur = db.cursor()
then = time.time()

cur.execute("SELECT password,numeros FROM alunos")
data = cur.fetchall()
for password,numero in data:
	print("A encryptar password do aluno " + str(numero))
	password = hashlib.md5(password.encode('utf-8')).hexdigest()
	cur.execute("UPDATE alunos SET password= '" + password + "' WHERE numeros = " + str(numero) + "")
db.commit()
cur.close()

now = time.time()
print("O programa demorou: ", now-then, " segundos")