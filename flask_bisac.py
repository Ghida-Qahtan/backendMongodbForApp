#flask_bisac.py

from flask import Flask,request, redirect,url_for,session
from flask import Response
from flask import json
from flask import jsonify
from bson.json_util import dumps
import pymongo,datetime,pprint

#from pymongo import collection
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MONGO_DBNAME']='ssdb'

#mongo= pymongo.MongoClient()
mongo = pymongo.MongoClient("mongodb+srv://ghida:ghida@cluster0-xskul.mongodb.net/ssdb?retryWrites=true&w=majority")

#mongo = pymongo.MongoClient(port=27017)

#db=client["ssdb"]
#mycoll=db["users"]
#print (db.list_collection_names({}))

@app.route('/', methods=['GET'])
def index():
    
    return jsonify({"co":['hi data']})

@app.route('/login', methods=['POST'])  # fanish
def login():
        user=mongo.get_database('ssdb').get_collection('users')
        request.data=json.loads(request.data)
        id= request.data["_id"]
        exis=user.find_one({"_id":id})
        #request.headers["Content-Type"]="application/json"
        if exis:
            if request.data['pass']== exis['pass']:
                return jsonify({'mas':["log in"]})
        return jsonify({'mas':["Invalid username and password combrnation!"]})
#    return jsonify({'mas':[""]}) 
    
@app.route('/SingUp', methods=['POST'])  # fanish
def SingUp():
        user=mongo.get_database('ssdb').get_collection('users')
        request.data=json.loads(request.data)
        id= request.data["_id"]
        exis=user.find_one({'_id':id})
        if exis is None:
            print(id)
            user.insert({'_id':request.data['_id'],'lname':request.data['lname'],'fname':request.data['fname'],'gender':request.data['gender'],'type':request.data['type'],'dd':request.data['dd'],'bd':request.data['bd'],'pass':request.data['pass']})
            return jsonify({'mas':["SING up"]})
        return jsonify({'mas':["this emil is already exists!"]})

@app.route('/Users', methods=['GET','PUT'])
def Users():
   if request.method=='PUT':
        user=mongo.get_database('ssdb').get_collection('users')
        print('hee;;;jjjjj')
        print(request.data)
        request.data=json.loads(request.data)
        id= request.data["_id"]
        exis=user.find_one({'_id':id})
        if exis:
            print(id)
            user.update_one({'_id':id},
            {
                "$set": {
                "lname": "nermeen"
                }
            }
            # upsert=True
            # {'_id':request.data['_id'],'lname':request.data['lname'],'fname':request.data['fname'],'gender':request.data['gender'],'type':request.data['type'],'dd':request.data['dd'],'bd':request.data['bd'],'pass':request.data['pass']
            # }
            )
            # ._insert_one({'_id':request.json('_id'),'lname':request.json('lname'),'fname':request.json('fname'),'gender':request.json('gender'),'type':request.json('type'),'dd':request.json('dd'),'bd':request.json('bd'),'pass':request.json('pass')})
            # session['_id'] = request.data['_id']       
            return jsonify({'mas':["updated"]})
        return jsonify({'mas':["this emil is already exists!"]})
   else:
    list=[]
    for x in mongo.get_database('ssdb').get_collection('users').find():
        list.append(x)
    return json.dumps(list)

@app.route('/Meals', methods=['GET','POST', 'PUT'])  
def Meals():
   meals=mongo.get_database('ssdb').get_collection('meals')
   request.data=json.loads(request.data)
   id= request.data["_id"]
   exis=meals.find_one({'_id':id})
   if request.method=='POST':
        if exis is None:       
            meals.insert({"_id": id, "TotalCalor": request.data['TotalCalor'],"TotalCarb":request.data['TotalCarb'],"type": request.data['type'],"date": request.data['date'],
            "varoeties": request.data['varoeties'],"time": request.data['time']})
            return jsonify({'mas':["created"]})
        return jsonify({'mas':["this meal is already exists!"]})
   
   elif request.method == 'PUT':
        meals.update_one({'_id':id},
            {
                "$set": {
                {"_id": id, "TotalCalor": request.data['TotalCalor'],"TotalCarb":request.data['TotalCarb'],"type": request.data['type'],"date": request.data['date'],
                "time": request.data['time']}                },
                "$push":{"varoeties":{request.data['varoeties']}
                }
            },upsert=True)
        return jsonify({'mas':["updated"]})
   else:
    list=[]
    for x in mongo.get_database('ssdb').get_collection('meals').find({"_id":id}):
        list.append(x)
    return json.dumps(list)

@app.route('/blood', methods=['POST','GET'])
def blood():

        user=mongo.get_database('ssdb').get_collection('users')
        request.data=json.loads(request.data)
        id= request.data["_id"]   
        currUser = user.find_one({'_id':id})
        if request.method=='POST':
            date=request.data["blood"]["date"]

            #dat=date{}
            # print(dat)
            time=request.data["blood"]["time"]

            exis= None
            for blood in currUser["blood"]: 
                if(blood["time"] == time and blood["date"] == date):
                    exis = True
                    break
            if exis is None:
                if not currUser["blood"]:
                    currUser["blood"] =  []
                currUser["blood"].append(request.data['blood'])
                user.update_one({"_id":id} , {"$set":{'blood': currUser["blood"]}})
                return jsonify({"data":'saved'})
            return jsonify("cann't save!")
        else:
            return jsonify(currUser["blood"])   
            

@app.route('/BMI', methods=['POST','GET'])
def BMI():
        user=mongo.get_database('ssdb').get_collection('users')
        request.data=json.loads(request.data)
        id= request.data["_id"]   
        currUser = user.find_one({'_id':id})
        if request.method=='POST':
            date=request.data["BMI"]["date"]
            time=request.data["BMI"]["time"]
            exis= None
            for blood in currUser["BMI"]: 
                if(blood["time"] == time and blood["date"] == date):
                    exis = True
                    break
            if exis is None:
                if not currUser["BMI"]:
                    currUser["BMI"] =  []
                currUser["BMI"].append(request.data['BMI'])
                user.update_one({"_id":id} , {"$set":{'BMI': currUser["BMI"]}})
                return jsonify({"data":'saved'})
            return jsonify("cann't save!")
        else:
            return jsonify(currUser["BMI"])  

@app.route('/Prursser', methods=['POST'])
def Prursser():
        user=mongo.get_database('ssdb').get_collection('users')
        request.data=json.loads(request.data)
        id= request.data["_id"]   
        currUser = user.find_one({'_id':id})
        if request.method=='POST':
            date=request.data["pressure"]["date"]

            #dat=date{}
            # print(dat)
            time=request.data["pressure"]["time"]

            exis= None
            for blood in currUser["pressure"]: 
                if(blood["time"] == time and blood["date"] == date):
                    exis = True
                    break
            if exis is None:
                if not currUser["pressure"]:
                    currUser["pressure"] =  []
                currUser["pressure"].append(request.data['pressure'])
                user.update_one({"_id":id} , {"$set":{'pressure': currUser["pressure"]}})
                return jsonify({"data":'saved'})
            return jsonify("cann't save!")
        else:
            return jsonify(currUser["pressure"])  

# @app.route('/meals', methods=['GET', 'POST'])
# def Meals_old():

#     if request.method =='POST':
#         request.data=json.loads(request.data)
#         user=mongo.get_database('ssdb').get_collection('meals')
#         id=request.data('_id')
#         exis=user.find_one({'_id':id,'type':request.json('type'),'date':request.data('date')})
#         if exis is None:
#             user._insert_one({'_id':request.json('_id'),'type':request.json('type'),'date':request.json('date'),'time':request.json('time'),'varoeties':request.json('varoeties'),'TotalCarb':request.json('TotalCarb'),'TotalCalor':request.json('TotalCalor')})
#             return jsonify("seved")
#         return jsonify("cann't save!")
#     else:         
#         return jsonify( 'hi')

@app.route('/variety', methods=['GET']) # fanish
def variety():
    list=[]
    for x in mongo.get_database('ssdb').get_collection('variety').find():
        list.append(x)
    return json.dumps(list)

@app.route('/Education', methods=['GET']) # fanish
def Education():
    list=[]
    for x in mongo.get_database('ssdb').get_collection('Education').find():
        print(x)
        list.append(x)
    return json.dumps(list,default=str)

@app.route('/med', methods=['GET'])# fanish
def med():
    list=[]
    for x in mongo.get_database('ssdb').get_collection('med').find():
        list.append(x)
    return json.dumps(list)

@app.route('/Actvitiy', methods=['POST'])
def Actvitiy():

    return
@app.route('/metions', methods=['POST'])
def metions():
    return
    
if __name__ == "__main__":
    app.run()
#    myobj={"message":"Hello Data"}
#    x = requests.post(" http://127.0.0.1:5000/messages", data = myobj)
