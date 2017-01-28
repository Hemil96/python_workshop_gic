import sqlite3
from datetime import datetime

from flask import Flask,request,jsonify
from flask_reqparse import RequestParser

from constants import DB_PATH

app = Flask(__name__)

parser = RequestParser()


def init_db():
    conn.execute("create table if not exists todo(id number auto_increment,name varchar(50),status varchar(10),created_at datetime)")
    conn.commit()

@app.route("/api/todos",methods=["POST"])
@parser.validate_arguments([
    {
        "name":"name",
        "source":"json",
        "required":True
    }
])
def create_todo(args):
    conn = sqlite3.connect(DB_PATH)
    name = args["name"]
    now = datetime.now()
    status = "pending"
    query = "insert into todo (name,status,created_at) values(\"{}\", \"{}\", \"{}\")".format(name,status,str(now))

    conn.execute(query)
    try:
        conn.commit()
    except:
        return jsonify({"error":"kuch to galat hain"})
    return jsonify({"response":"item has been added to todo"})

@app.route('/api/todos')
def todos_get():
    conn = sqlite3.connect(DB_PATH)
    data = conn.execute("select * from todo")
    jsondata = []
    for d in data:
        jsondata.append({
            "id" : d[0],
            "title" : d[1],
            "status" : d[2],
            "created_at" : d[3]
        })
    return jsonify({"response" : jsondata})



if __name__== "__main__":
    app.run(port=8080, host="0.0.0.0",debug=True)
