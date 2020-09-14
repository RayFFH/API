import flask
from flask import request, jsonify, render_template
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
     return '''<h1>Grade outcomes page</h1>
 <p>Records different students grades</p>'''


@app.route('/add_record', methods=["POST"])
def add_record():
    if request.method == "POST":
        firstname = request.form["fm"]
        lastname = request.form["lm"]
        grade = request.form["gr"]
        conn = sqlite3.connect('grades.db')
        c = conn.cursor()
        c.execute("INSERT INTO grades VALUES (?,?,?)", (firstname, lastname, grade))
        conn.commit()
        conn.close()
    return render_template("gradeinput2.html")


@app.route('/api/v1/grades/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('grades.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM grades;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/grades', methods=['GET'])
def api_filter():
    query_parameters = request.args

    first_name = query_parameters.get('first_name')
    last_name = query_parameters.get('last_name')
    grade = query_parameters.get('grade')

    query = "SELECT * FROM grades WHERE"
    to_filter = []

    if first_name:
         query += ' first_name=? AND'
         to_filter.append(first_name)
    if last_name:
         query += ' last_name=? AND'
         to_filter.append(last_name)
    if grade:
         query += ' grade=? AND'
         to_filter.append(grade)
    if not (first_name or last_name or grade):
         return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('grades.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()