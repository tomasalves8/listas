import MySQLdb as sql
import hashlib
import time

db = sql.connect(host="localhost",  
					 user="root",	   
					 passwd="", 
					 db="lista")  
cur = db.cursor()
then = time.time()

cur.execute("SELECT Lista,Votos FROM votos")
data = cur.fetchall()
for Lista,Votos in data:
	cur.execute("UPDATE votos SET Votos= 0 WHERE Lista = '" + str(Lista) + "'")
	Lista = Lista.upper()
	print("A remover votos da lista " + str(Lista))
db.commit()
cur.close()
	
now = time.time()
print("O programa demorou: ", now-then, " segundos")