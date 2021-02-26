from flask import Flask, render_template, redirect, request, session, flash
import mysql.connector
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)
app.permanent_session_lifetime = timedelta(days=2)
db = mysql.connector.connect(database="rms", host="localhost",user="root",password="")
cursor = db.cursor()

@app.route("/")
def index():
    if 'user_id' in session:
        return redirect("/download")
    else:
        return render_template("index.html")

@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method=="POST":
        hall_ticket_number = request.form["ticket"]
        date_of_birth = request.form["dob"]
        if hall_ticket_number != "" and date_of_birth != "":
            x=""
            x=x+date_of_birth[8]
            x=x+date_of_birth[9]
            x=x+"-"
            x=x+date_of_birth[5]
            x=x+date_of_birth[6]
            x=x+"-"
            x=x+date_of_birth[0]
            x=x+date_of_birth[1]
            x=x+date_of_birth[2]
            x=x+date_of_birth[3]
            cursor.execute("""SELECT * FROM employees WHERE ROLLNO='{}' AND DOB='{}' """.format(hall_ticket_number,x))
            user = cursor.fetchall()
            if len(user) > 0:
                session.permanent=True
                session['user_id']=user[0][3]
                return redirect("/download")
            else:
                flash("The given Roll Number and Date Of Birth doesn't match.")
                return redirect("/")
        else:
            flash("The form shouldn't be empty")
            return redirect("/")
    else:
        return redirect("/")


@app.route("/download")
def download():
    if 'user_id' in session:
        rollno = session['user_id']
        cursor.execute("""SELECT * FROM employees WHERE ROLLNO='{}' """.format(rollno))
        user = cursor.fetchall()
        return render_template("download.html", data={'sno':user[0][0], 'dateofexam':user[0][1], 'appearingpost':user[0][2], 'rollno': user[0][3], 'name':user[0][4], 'fathername':user[0][5], 'dob':user[0][6], 'venue':user[0][7], 'address':user[0][8]})
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return redirect("/")
    else:
        return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
