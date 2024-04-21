from datetime import date

import psycopg2 as psycopg2
from flask import Flask, render_template, g, flash, abort, request, redirect, url_for, session

from database_model import FDataBase

DATABASE="mybase"
DEBUG=True
SECRET_KEY='j6eXxzoQkGIwj61DJ1r7AcOwDTxv4HqV'
PASSWORD="P_yuriko2000"
HOST="localhost"
USER = "postgres"

app = Flask(__name__)

app.secret_key = SECRET_KEY


@app.route('/')
def admin():
    db = get_db()
    dbase=FDataBase(db)
    session['loggedin'] = True
    session['access'] = 'admin'
    return render_template('admin.html')


def connect_db():
    conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD,
                            host=HOST)
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/add_client", methods=["POST", "GET"])
def addClient():
    db = get_db()
    dbase = FDataBase(db)
    print(session['access'])

    if request.method == "POST":
        res = dbase.addClient(request.form['fam'], request.form['name'],request.form['ot'], request.form['number'], request.form['note'])
        if not res:
            flash('Ошибка добавления клиента', category='error')
        else:
            flash('Клиент добавлен успешно', category='success')
    return render_template('add_client.html',title='Добавление клиента')



@app.route("/showclient")
def showClient():
    db = get_db()
    dbase = FDataBase(db)
    print(session['access'])
    post = dbase.showClient()
    return render_template('showclient.html',post=post, title='Просмотр записей')

@app.route('/delclient', methods=["POST", "GET"])
def delClient():
    db = get_db()
    dbase = FDataBase(db)
    print(session['access'])
    if request.method == 'POST':
        cur = db.cursor()
        cur.execute(f"DELETE FROM telbook WHERE id={int(request.form['id'])}")
        db.commit()
        db.close()
        if not cur:
            flash('Ошибка удаления клиента', category='error')
        else:
            flash('Клиент удален', category='success')
    return render_template('delclient.html',title='Удаление записи')

@app.route('/update_client', methods=["POST", "GET"])
def updateclient():
    db = get_db()
    dbase = FDataBase(db)
    print(session['access'])
    if request.method == 'POST':
        cur = db.cursor()
        cur.execute(f"UPDATE telbook SET tel='{(request.form['number'])}', textnote='{(request.form['note'])}' WHERE id={int(request.form['id'])}")
        db.commit()
        db.close()
        if not cur:
            flash('Ошибка изменения записи', category='error')
        else:
            flash('Информация обновлена', category='success')
    return render_template('update_client.html',title='Изменение записи')

if __name__ == '__main__':
    app.run(debug=True)

