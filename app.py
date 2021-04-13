from flask import Flask, render_template,request
#from flask_consent import Consent
import dns
app = Flask(__name__)


import pymongo

client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.kopw9.mongodb.net/mydatabase?retryWrites=true&w=majority")
db = client.test
mydb = client["mydatabase"]
mycol = mydb["companies"]

@app.context_processor
def inject_template_scope():
    injections = dict()

    def cookies_check():
        value = request.cookies.get('cookie_consent')
        return value == 'true'
    injections.update(cookies_check=cookies_check)

    return injections
# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():
	data=''
	li = mycol.find()
	for i in li:
		for key,value in i.items():
			if(key=="name"):
				data+=value
				data+=','
	return render_template('index.html', the_title='Numero Gratuit',data= data)

@app.route('/symbol.html/<name>')
def symbol(name):
	data = ''
	li = mycol.find()
	for i in li:
		if(i["name"]==name):
			data= i["phone"]
	return render_template('symbol.html', the_title='Contact Info',data= data,comp=name)


@app.route('/myth.html', methods=['POST','GET'])
def myth():
	if request.method=='POST':
		a=request.form['name']
		b=request.form['phone']
		val={}
		val['name']=a
		val['phone']=b
		x = mycol.insert_one(val)
	return render_template('myth.html', the_title='Add companies')

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5001, debug = True)

