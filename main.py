from flask import Flask, render_template, request, flash, redirect, url_for
import MySQLdb as sql
import re
import hashlib
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField

app = Flask(__name__)
app.config['SECRET_KEY'] = "Your_secret_string"

# Definir Listas como um dicionario.
listas = {}

def get_listas():
	db = sql.connect(host="localhost",  
					 user="root",	   
					 passwd="", 
					 db="lista")  
	cur = db.cursor()

	cur.execute("SELECT Lista FROM votos")
	data = cur.fetchall()
	listas = {}
	for x in data:
		x = str(x)
		# Remover Caracteres Especiais. Exemplo( ('g',) -> g )
		x = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,']", "", x)

		cur.execute("SELECT Votos FROM votos WHERE Lista =  '" + x + "'" )
		data = cur.fetchone()
		data = str(data)
		
		# Remover Caracteres Especiais. Exemplo( (41,) -> 41 )
		data = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,']", "", data)
		
		# Mudar a letra para letra maiscula. Exemplo ( g -> G )
		x = x.upper()

		listas[x] = data
	return listas

	
class voto(Form):
	numero = StringField(u'Numero Cartão', validators=[validators.input_required()])
	listaselecao = SelectField(u'Lista', choices=listas)
	password = PasswordField('Password', [
		validators.DataRequired(),
	])
	
@app.route("/", methods=['GET', 'POST'])
def home():
	db = sql.connect(host="localhost",  
					 user="root",	   
					 passwd="", 
					 db="lista")  
	cur = db.cursor()
	lista_id = []
	numerolista = []
	numero_listas = 0
	form = voto(request.form)
	listas = get_listas()
	form.listaselecao.choices = [(0,"Escolher Lista")]
	
	for lista in listas:
		# Atribuir seleção a um ID specifico.
		lista_id.append(lista)
		numero_listas += 1
		# Adicionar Opção ao form
		form.listaselecao.choices.append((numero_listas,"Lista " + lista))
		
	if request.method == "POST":
		# Encryptar
		password = hashlib.md5(form.password.data.encode('utf-8')).hexdigest()
		# Atribuir o numero de cartão a uma variavel
		numero_cartao = str(form.numero.data)
		
		# Encontrar aluno
		encontrado = cur.execute("SELECT * FROM alunos WHERE numeros = %s", [numero_cartao])
		# Se encontrar aluno
		if encontrado > 0:
			data = cur.fetchone()
			password_encryptada = data[1]

			# Se encontrar aluno && password correta && seleção valida (Não é selecionar Lista)
			if password == password_encryptada and form.listaselecao.data != "0":
				# Apatir do ID recebido atribir à letra da lista
				lista_escolhida = lista_id[int(form.listaselecao.data)-1]

				# Mudar a letra para letra maiscula
				lista_escolhida = lista_escolhida.lower()

				# Variavel votou na database atribuida a uma variavel
				votou = data[2]

				# Se ainda não votou
				if votou == 0:
					# Adicionar voto
					cur.execute("UPDATE votos SET Votos= Votos + 1 WHERE Lista = '" + lista_escolhida + "'")
					db.commit()
					# Colocar na base de dados que o aluno votou com sucesso
					cur.execute("UPDATE alunos SET votou = 1 WHERE numeros = %s", [numero_cartao])
					db.commit()
					flash('Voto Introduzido', 'success')
					return redirect(url_for('home'))
				
				# Senão é porque ja votou.
				else:
					flash('O Aluno já votou', 'danger')
					return redirect(url_for('home'))
				
			else:
				#Verificar que a lista escolhida não é "Escolher Lista"
				if form.listaselecao.data == "0":
					flash('Lista não existe', 'danger')
				# A unica opção que sobra é o aluno e a sua password não forem encontrados na base de dados.
				else:
					flash('Password incorreta', 'danger')
				return redirect(url_for('home'))
		else:
			flash('Aluno/a não encontrado/a', 'danger')
			return redirect(url_for('home'))

	cur.close()
	db.close()
	return render_template("index.html", form=form, listas=listas)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port='5000')
