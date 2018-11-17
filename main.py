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
listas = {}

@app.route("/")
def home():
    cur = mysql.connection.cursor()

    cur.execute("SELECT Lista FROM votos")
    data = cur.fetchall()

    for x in data:
        x = x['Lista']
        cur.execute("SELECT Votos FROM votos WHERE Lista =  '" + x + "'" )
        data = cur.fetchone()
        listas[x] = data['Votos']

    cur.close()

    return render_template("index.html", listas=listas)


if __name__ == '__main__':
    app.run(debug=True)
