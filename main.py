from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lista'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)

@app.route("/")
def home():
    cur = mysql.connection.cursor()

    # -- LISTA V --
    cur.execute("SELECT Votos FROM votos WHERE Lista = 'V'")
    data = cur.fetchone()
    listav = data['Votos']

    # -- LISTA M --
    data = cur.execute("SELECT Votos FROM votos WHERE Lista = 'M'")
    data = cur.fetchone()
    listam = data['Votos']
    cur.close()
    return render_template("index.html", listav=listav, listam=listam)



if __name__ == '__main__':
    app.run(debug=True)
