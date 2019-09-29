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
#app.config['MONGO_URL']='mongodb+srv://ghida:<ghida>@cluster0-xskul.mongodb.net/test?retryWrites=true&w=majority&authSource=authDB'

#mongo= pymongo.MongoClient()
mongo = pymongo.MongoClient("mongodb+srv://ghida:ghida@cluster0-xskul.mongodb.net/ssdb?retryWrites=true&w=majority")

#mongo = pymongo.MongoClient(port=27017)

#db=client["ssdb"]
#mycoll=db["users"]
#print (db.list_collection_names({}))

@app.route('/', methods=['GET'])
def index():
    
    return jsonify({"co":['hi data']})

@app.route('/login', methods=['POST'])
def login():
        user=mongo.db.users
        id=request.json('_id')

        exis=user.find_one({'_id':id})
        request.headers["Content-Type"]="application/json"
        if exis:
            if request.json('pass')== exis['pass']:
                session['_id'] = request.json('_id')      

            return jsonify(CONNCTION="login")
        return jsonify("Invalid username and password combrnation!")
    
@app.route('/SingUp', methods=['POST'])
def SingUp():
#    if request.method=='POST':
        user=mongo.get_database('ssdb').get_collection('users')
        print('hee;;;jjjjj')
        print(request.data)
        request.data=json.loads(request.data)
        id= request.data["_id"]
        exis=user.find_one({'_id':id})
        if exis is None:
            print(id)
            user.insert({'_id':request.data['_id'],'lname':request.data['lname'],'fname':request.data['fname'],'gender':request.data['gender'],'type':request.data['type'],'dd':request.data['dd'],'bd':request.data['bd'],'pass':request.data['pass']})
            # ._insert_one({'_id':request.json('_id'),'lname':request.json('lname'),'fname':request.json('fname'),'gender':request.json('gender'),'type':request.json('type'),'dd':request.json('dd'),'bd':request.json('bd'),'pass':request.json('pass')})
            # session['_id'] = request.data['_id']       
            return jsonify({'mas':["SING up"]})
        return jsonify({'mas':["this emil is already exists!"]})
#    return jsonify({"data":[ {"name": 'GHaida'}]})

    
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
   return jsonify({"data":[ {"name": 'GHaida'}]})


@app.route('/Meals', methods=['GET','POST', 'PUT'])
def Meals():
   meals=mongo.get_database('ssdb').get_collection('meals')
   request.data=json.loads(request.data)
   id= request.data["_id"]
   exis=meals.find_one({'_id':id})
   if request.method=='POST':
        id= request.data["_id"]
        exis=meals.find_one({'_id':id})
        if exis is None:       
            meals.insert({"_id": id, "TotalCalor": request.data['TotalCalor']})

            return jsonify({'mas':["created"]})
        return jsonify({'mas':["this emil is already exists!"]})
   elif request.method == 'PUT':
        meals.update_one({'_id':id},
            {
                "$set": {
                "TotalCalor": request.data['TotalCalor']
                }
            })
        return jsonify({'mas':["updated"]})
   else:
    list=[]
    for x in mongo.get_database('ssdb').get_collection('meals').find():
        list.append(x)
    return json.dumps(list)
   return jsonify({"data":[ {"name": 'GHaida'}]})



@app.route('/blood', methods=['POST'])
def blood():
        user=mongo.db.users
        id=request.json('_id')
        time=request.json('time')
        date=request.json('date')
        exis=user.find_one({'_id':id,'blood':{'time':time,'date':date}})
        if exis is None:
            user.update_one({exis['_id']},{'$blood':request.json('blood')})
            return jsonify(CONNCTION="seved")
        return jsonify("cann't save!")    

@app.route('/BMI', methods=['POST'])
def BMI():
        user=mongo.db.users
        id=request.json('_id')
        time=request.json('time')
        date=request.json('date')
        exis=user.find_one({'_id':id,'BMI':{'time':time,'date':date}})
        if exis is None:
            user.update_one({exis['_id']},{'$BMI':request.json('BMI')})
            return jsonify(CONNCTION="seved")
        return jsonify("cann't save!")

@app.route('/Prursser', methods=['POST'])
def Prursser():
        user=mongo.db.users
        id=request.json('_id')
        time=request.json('time')
        date=request.json('date')
        exis=user.find_one({'_id':id,'pressure':{'time':time,'date':date}})
        if exis is None:
            user.update_one({exis['_id']},{'$pressure':request.json('pressure')})
            return jsonify("seved")
        return jsonify("cann't save!")

@app.route('/meals', methods=['GET', 'POST'])
def Meals_old():
    # print('request--hduewdhue')
    # print(request.headers)
    # return 'hi'
    if request.method =='POST':
        user=mongo.db.meals
        id=request.json('_id')
        exis=user.find_one({'_id':id,'type':request.json('type'),'date':request.json('date')})
        if exis is None:
            user._insert_one({'_id':request.json('_id'),'type':request.json('type'),'date':request.json('date'),'time':request.json('time'),'varoeties':request.json('varoeties'),'TotalCarb':request.json('TotalCarb'),'TotalCalor':request.json('TotalCalor')})
            return jsonify("seved")
        return jsonify("cann't save!")
    else:
              
        return jsonify( 'hi')

@app.route('/variety', methods=['GET'])
def variety():
    print('we;;ppp;')
    #print(mongo.db.get_collection('variety').count_documents)
    #print(mongo.get_database('ssdb').name)
    print('-----;kkkkkk')
    list=[]
#    if mongo.db.variety.count_documents({})>0:
    for x in mongo.get_database('ssdb').get_collection('variety').find():
        list.append(x)
    return json.dumps(list)
#    return jsonify({'is none':[mongo.get_database('ssdb').get_collection('variety').find()]})

@app.route('/Education', methods=['GET'])
def Education():
    list=[]
    if mongo.db.Education.count_documents({})>0:
        for x in mongo.db.Education.find():
            list.append(x)
        return json.dumps(list)
    return jsonify({'is none':[mongo.db.Education.count_documents({})]})

@app.route('/med', methods=['GET'])
def med():
    user=mongo.db.med       
    return jsonify( user.find({}))

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
