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
	print("A remover aluno " + str(numero))
	cur.execute("DELETE FROM alunos WHERE numeros = " + str(numero) + "")
db.commit()
cur.close()

now = time.time()
print("O programa demorou: ", now-then, " segundos")