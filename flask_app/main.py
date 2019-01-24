from flask import Flask, render_template, redirect, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
import os
import json

app = Flask(__name__)
api = Api(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flask_react_app_v2.0.sqlite')
sqldb = SQLAlchemy(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_react_app_v2.0"
mongo = PyMongo(app)
# mongodb = mongo['task4_form']
# mongocoll = mongodb['all_data']

class SQLiteDatabase(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key = True)
    data = sqldb.Column(sqldb.Text)

    def __init__(self, input1, input2):
        self.data = str({
            'input1' : input1,
            'input2' : input2,
            'sum' : int(input1) + int(input2),
        })

class PublishSQLiteDB(Resource):
    def get(self, data_input):
        print(data_input)
        data_list = data_input.split('+')
        print(data_list)
        x = SQLiteDatabase(data_list[0], data_list[1])
        sqldb.session.add(x)
        sqldb.session.commit()
        return Response('Record inserted in database.')
    
class PublishMongoDB(Resource):
    def get(self, data_input):
        print(data_input)
        data_list = data_input.split('+')
        print(data_list)
        data = ({
            "input1" : data_list[0],
            "input2" : data_list[1],
            "sum" : int(data_list[0]) + int(data_list[1])
        })
        result = mongo.db.all_data.insert_one({'data':data})
        if result.inserted_id == None:
            return Response('Record could not be inserted in database.')
        else:
            return Response('Record inserted in database.')

api.add_resource(PublishSQLiteDB, '/PublishSQLiteDB/<string:data_input>')
api.add_resource(PublishMongoDB, '/PublishMongoDB/<string:data_input>')

if __name__ == '__main__':
    sqldb.create_all()
    app.run(debug=True)