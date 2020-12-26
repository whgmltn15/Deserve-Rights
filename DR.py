from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")
conn.execute('CREATE TABLE IF NOT EXISTS user_info (ID text PRIMARY KEY, PW text, EMAIL text, AGE text)')
print("Table created successfully")
conn.execute('CREATE TABLE IF NOT EXISTS google (URL text)')
print("Table created successfully")
conn.close()

# con = sqlite3.connect("database.db")
# cur = con.cursor()
# execute = 'INSERT INTO google(URL) VALUES (?)'
# cur.execute(execute, ["https://www.google.com/"])
# conn.close()
print("data input success")

app = Flask(__name__)

app.secret_key = b'123qwerty'

con = sqlite3.connect("database.db")

cur = con.cursor()

@app.route('/')
def start():
    return render_template('start.html')

@app.route("/sign_up", methods=['POST'])
def sign_up():
    global id_info
    if request.method == 'POST':
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        ID = request.form.get('ID', "not data")
        PW = request.form.get('PW', "not data")
        EMAIL = request.form.get('EMAIL', "not data")
        AGE = request.form.get('AGE', "not data")

        print("AGE", AGE)

        if AGE != "not data":
            if int(AGE) < 19:
                print("you only can sign up for user")

                if ID == "not data":
                    return render_template('sign_up.html')
                else:
                    try:
                        execute = "INSERT INTO user_info(ID, PW, EMAIL, AGE) VALUES (?, ?, ?, ?)"
                        cur.execute(execute, (ID, PW, EMAIL, AGE))
                        print("Success Join")
                        con.commit()
                        con.close()
                        id_info = ID
                        return redirect(url_for('main'))
                    except:
                        print("Fail Join")
                        return render_template('start.html')
    return render_template('sign_up.html')

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    error = None
    global id_info
    if not session.get('logged_in'):
        if request.method == 'POST':
            con = sqlite3.connect("database.db")
            cur = con.cursor()

            ID = request.form.get('ID', "not data")
            PW = request.form.get('PW', "not data")
            print(ID)
            if ID == "not data":
                return render_template('sign_in.html')

            execute = "SELECT * FROM user_info where ID = (?)"
            cur.execute(execute, [ID])
            rows = cur.fetchall()
            con.commit()
            con.close()

            try:
                if rows[0][1] == PW:
                    print("Success Login")
                    session['logged_in'] = True
                    id_info = ID
                    return redirect(url_for('main'))
            except:
                print("Fail Login")
                return render_template('sign_in.html')
        else:
            return redirect(url_for('main'))
    return render_template('sign_in.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('start'))

@app.route('/main', methods = ['POST', 'GET'])
def main():
    return render_template('main.html')

@app.route('/settings', methods = ['POST', 'GET'])
def account():
    global id_info
    if request.method == 'POST':
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        execute = "SELECT * FROM user_info"
        cur.execute(execute)
        rows = cur.fetchall()
        print("id_info", id_info)

        for ID, PW, EMAIL, AGE in rows:
            if ID == id_info:
                print("ID PW EMAIL AGE", ID, PW, EMAIL, AGE)

        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from user_info")
        rows = cur.fetchall()
        return render_template('settings.html', rows=rows)

@app.route('/pwEdit', methods = ['POST', 'GET'])
def pwEdit():
    msg = ""
    global id_info
    if request.method == 'POST':
        print("in post")
        PW = request.form.get('newPW', "not data")
        print("PW", PW)
        print("id info ", id_info)
        if PW == "not data":
            return render_template("pwEdit.html")
        else:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('UPDATE user_info set PW=? where ID =?', (PW, id_info))
                con.commit()

                return redirect(url_for('start'))
    else:
        return render_template("pwEdit.html")

@app.route('/searchResults', methods=['POST', 'GET'])
def searchResults():
    msg = ""
    if request.method == 'POST':
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        search = request.form.get('search', "not data")

        URL = request.form.get('URL', "not data")

        print("URL", URL, type(URL))

        if search == "not data" and URL == "not data":
            return render_template("searchResults.html")
        elif search != "not data":
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from google")
            rows = cur.fetchall()
            return render_template('searchResults.html', rows=rows)
        else:
            execute = 'INSERT INTO google(URL) VALUES (?)'
            cur.execute(execute, [URL])
            con.commit()
            return render_template('searchResults.html')

@app.route('/matching', methods=['POST', 'GET'])
def matching():
    msg =""
    error = None
    if request.method == 'POST':
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        user = [['Male', 25, 'science', 'hi'], ['Female', 30, 'math','af'], ['Female', 20, 'english','dfd']]
        score = [0, 0, 0]

        gender = request.form.get("gender", "not data")
        age = request.form.get("age", "not data")
        major = request.form.get("major", "not data")

        if gender != "not data" and age != "not data" and major != "not data":

            for i in range(len(user)):
                if gender == user[i][0]:
                    score[i] += 1
                else:
                    score[i] += 0

                score[i] = score[i] * 0.4

                age = int(age)
                age_score = age - user[i][1]

                # age
                if age_score > 50:
                    age_score = 0
                elif age_score < 50 and age_score > 0:
                    age_score = age_score * 0.5
                else:
                    score[i] += (age_score) * 0.3

                score[i] += (age_score * 0.4)

                # major
                if major == user[i][2]:
                    score[i] += 1
                else:
                    score[i] += 0

                score[i] = score[i] * 0.6

        max_value = 0
        for i in range(len(score)):
            if score[i] > score[max_value]:
                max_value = i
        print("select", user[max_value][3])

        return render_template('matching.html', row=user[max_value][3])
    else:
        return render_template('matching.html')

if __name__ == '__main__':
    app.run()