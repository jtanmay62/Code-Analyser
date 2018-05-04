import os
import sqlite3
from flask import g
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import javalang
import ast
fp = open("key.txt","r")
text = fp.read()
text = text.split('\n')
fp.close()
UPLOAD_FOLDER = '\uploads'
ALLOWED_EXTENSIONS = set(['.java'])
app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



#Siddharth
@app.route('/')
def index():
	return render_template('home.html')

@app.route('/our_team')
def our_team():
	return render_template('our_team.html')

@app.route('/login')
def home():
	return render_template('login.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/new_user')
def new_user():
	return render_template('new_user.html')
#/Siddharth





#Tanmay
@app.route('/insert', methods=['GET','POST'])
def insert():
	msg=""
	if request.method=='POST':
		try:
			fname=request.form['fname']
			lname=request.form['lname']
			uname=request.form['uname']
			password=request.form['password']
			email=request.form['email']
			phone=request.form['phone']
			address=request.form['address']
			with sqlite3.connect("user_details.db") as con:
				cur = con.cursor()
	        	
	        	cur.execute("INSERT INTO User7 (fname, lname, uname, phone, password, address, email) VALUES (?, ?, ?, ?, ?, ?, ?)",(fname, lname, uname, phone, password, address, email) )
	        	con.commit()
	        	
	        	msg = "Record successfully added"
		except:
			con.rollback()
			msg = "Error in insert operation"
      
		finally:
			return render_template("inserted.html",msg = msg)
			con.close()
	
@app.route('/index', methods=['GET', 'POST'])
def login():
	flag=0
	if request.method == 'POST':
		con=sqlite3.connect("user_details.db")
		cursor=con.execute("select * from User7")
		for row in cursor:
			if request.form['uname'] == row[2]:
				if request.form['pass'] == row[4]:
					return render_template('index.html')
				else:
					error="Invalid Username or Password"
					flag=0
			else:
				error="Invalid Username or Password"
				flag=0
		return render_template('login.html')
	else:
		return render_template('login.html')
#/Tanmay



#Moulie
@app.route('/file', methods = ['GET', 'POST'])
def action():
	if request.method == 'POST':
		f = request.files['file']
		fn = secure_filename(f.filename)
		#fn = fn.rsplit('.', 1)[1].lower()
		f.save(fn)
		fp = open(fn,"r")
		CodeStr = fp.read()
		return render_template('result.html', fn=fn)
		
	else:
		return render_template('index.html')
#/Moulie





@app.route('/show', methods=['GET', 'POST'])
def show():
	result=request.form
	file=result.get("fname", "")
	fp = open(file,'r')
	CodeStr = fp.read()
	tree = javalang.parse.parse(CodeStr)
	tokens = list(javalang.tokenizer.tokenize(CodeStr))
	Keys = {}
	Vars = {}
	Class = []
	Meth = []
	Loops = {}
	Cond = {}
	Search = {}
	Depth=[[]]
	ClassMeth={}
	ClassVar={}
	CodeList = CodeStr.split('\n')
	x = 0
	count = 0

	if request.method == 'POST':
		
		#Tulika
		if request.form['submit'] == 'Keywords':
			for x in tokens:
				if x.value in text:
					Keys[str(x.value)] = Keys.get(str(x.value),0) + 1
			return render_template('result.html', Keys=Keys, fn=file)
		

		elif request.form['submit'] == 'Variables':
			while (x < len(tokens)):
			    if type(tokens[x]) is javalang.tokenizer.BasicType:
			        count+=1
			        typename = str(tokens[x].value) +" '"+ str(tokens[x+1].value)+"'"
			        Vars[typename] = Vars.get(typename , 0) + 1
			    x = x + 1
			return render_template('result.html', Vars=Vars, fn=file, count=count)
		#/Tulika


		#Siddharth
		elif request.form['submit'] == 'Classes':
			for path,node in tree.filter(javalang.tree.ClassDeclaration):
				Class.append(str(node.name))
			return render_template('result.html', Class=Class, fn=file)


		elif request.form['submit'] == 'Methods':
			for path,node in tree.filter(javalang.tree.MethodDeclaration):
				Meth.append(str(node.name))
			return render_template('result.html', Meth=Meth, fn=file)
		#/Siddharth		


		#Moulie
		elif request.form['submit'] == 'Loops':
			for path,node in tree.filter(javalang.tree.ForStatement):
				Loops["For"] = Loops.get("For",0) + 1


			for path,node in tree.filter(javalang.tree.DoStatement):
				Loops["DoWhile"] = Loops.get("DoWhile",0) + 1


			for path,node in tree.filter(javalang.tree.WhileStatement):
				Loops["While"] = Loops.get("While",0) + 1
			
			return render_template('result.html', Loops=Loops, fn=file)
		

		elif request.form['submit'] == 'Conditions':
			for path,node in tree.filter(javalang.tree.IfStatement):
				Cond["if"] = Cond.get("if",0) + 1


			for path,node in tree.filter(javalang.tree.SwitchStatementCase):
				Cond["Switch"] = Cond.get("Switch",0) + 1
			
			return render_template('result.html', Cond=Cond, fn=file)
		#/Moulie



		#Tanmay
		elif request.form['submit'] == 'Description of classes':
			for path,node in tree.filter(javalang.tree.ClassDeclaration):
			    tmpVar = []
			    tmpMeth = []
			    for path,n in node:
			        if type(n) is javalang.tree.VariableDeclarator:
			            tmpVar.append(str(n.name))
			        if type(n) is javalang.tree.MethodDeclaration:
			            tmpMeth.append(str(n.name))
			    ClassVar[str(node.name)] = tmpVar
			    ClassMeth[str(node.name)] = tmpMeth
			return render_template('result.html',ClassVar=ClassVar, ClassMeth=ClassMeth, fn=file)    
		#/Tanmay



		#Moksh
		elif request.form['submit']	== 'Depth of Inheritance':
			for pos,x in enumerate(tokens):
			    if type(x) is javalang.tokenizer.Keyword:
			        if str(x.value) == "extends":
			        	Found = 0
			        	Parent = str(tokens[pos+1].value)
			        	Child = str(tokens[pos-1].value)
			        	for I,items in enumerate(Depth):
			        		if Parent in items:
			        			Found = 1
			        			if Parent == items[len(items)-1]:
			        				Depth[I].append(Child)
			        			else:
			        				tmp = []
			        				for x in items:
			        					print x
			        					tmp.append(x)
			        					if x == Parent:
			        						break
			        				Depth.append(tmp)

					if Found == 0:
						tmp = [Parent,Child]
						Depth.append(tmp)
			del Depth[0]
			return render_template('result.html', Depth=Depth, fn=file)
		#/Moksh
		



		
		elif request.form['submit'] == 'Back':
			return render_template('index.html')
	else:
		return render_template('result.html')	        


if __name__ == '__main__':
	app.run(debug = True)