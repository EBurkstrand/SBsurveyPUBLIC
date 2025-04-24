from flask import Flask, render_template, request, redirect, url_for
import os, psycopg2

app = Flask(__name__)



def recordSurvey(one, two, three, four, five):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])

    cur = conn.cursor()

    cur.execute("INSERT INTO SurveyResponses (responder, selection, dropdown, checkbox, sometimes) VALUES (%s, %s, %s, %s, %s)", (one, two, three, four, five))

    conn.commit()
    cur.close()
    conn.close()

def getResults():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])

    cur = conn.cursor()

    # cur.execute("SELECT * FROM SurveyResponses")
    cur.execute("select array_to_json(array_agg(row_to_json(t))) from (select * from SurveyResponses) t")

    data = cur.fetchall()

    cur.close()

    conn.close()

    return data

def getResultsBackwards():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])

    cur = conn.cursor()

    # cur.execute("SELECT * FROM SurveyResponses ORDER BY id DESC")

    cur.execute("select array_to_json(array_agg(row_to_json(t))) from (select * from SurveyResponses ORDER BY id DESC) t")

    data = cur.fetchall()

    cur.close()

    conn.close()

    return data

@app.route("/")
def hello_world():
    user_name = request.args.get("userName", "unknown")
    return render_template("main.html", user = user_name)

@app.route("/survey")
def take_survey():
    return render_template("survey.html")

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")

@app.route("/record", methods=["POST"])
def record():
    name = request.form.get("ThisIsName")
    second = request.form.get("fav")
    third = request.form.get("length")
    fourth = request.form.get("solo", False)
    if(fourth != False):
        fourth = True
    sometimes = request.form.get("sometimes", None)
    print(name)
    print(second)
    print(third)
    recordSurvey(name, second, third, fourth, sometimes)

    return redirect(url_for("thanks"))

@app.route("/decline")
def decline_user():
    return render_template("decline.html")

@app.route("/api/results")
def returnJson():
    order = request.args.get("reverse", False)
    print(order)
    if(order == "true" or order == True):
        data = getResultsBackwards()
    else:
        data = getResults()
    
    return data[0][0]

@app.route("/admin/summary")
def adminPage():

    data = getResults()

    names = []
    defense = []
    length = []
    check = []
    text = []

    for i in data[0][0]:
        print(i)
        names.append(i["responder"])
        defense.append(i["selection"])
        length.append(i["dropdown"])
        check.append(i["checkbox"])
        text.append(i["sometimes"])

    return render_template("admin.html", names = names, defense = defense, length = length, check = check, text = text)