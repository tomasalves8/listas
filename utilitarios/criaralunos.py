import MySQLdb as sql
import hashlib
import random
import time
db = sql.connect(host="localhost",  
					 user="root",	   
					 passwd="", 
					 db="lista")  
cur = db.cursor()
then = time.time()
for x in range(1,3000):
	numero = x
	password = random.randint(1, 25564)
	cur.execute("INSERT INTO alunos(numeros,password,votou) VALUES(" + str(numero) + "," + str(password) + ",1);")
	print("Criando aluno " + str(numero))
	numero_de_listas = cur.execute("SELECT * FROM votos")
	lista_pra_votar = random.randint(1, numero_de_listas)
	cur.execute("UPDATE votos SET Votos= Votos + 1 WHERE id = '" + str(lista_pra_votar) + "'")
db.commit()
cur.close()
now = time.time()
print("O programa demorou: ", now-then, " segundos")