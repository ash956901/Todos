from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)

#database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

# Create db in python cli
#from app import db,app
# >>> app.app_context().push()
# >>> db.create_all()

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route('/',methods=['GET','POST'])
def hello_world():
    # return 'Hello, World!'
    if(request.method=='POST'):
        title=request.form.get('title')
        desc=request.form.get('desc')
        if title and desc:
            todo=Todo(title=title,desc=desc)
            db.session.add(todo)
            db.session.commit()
    # todo=Todo(title='First Todo',desc='Read Interview Questions')
    # db.session.add(todo)
    # db.session.commit()
    allTodo=Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo)

@app.route('/products')
def products():
    return 'Products'

@app.route('/show')
def show():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form.get('title')
        desc=request.form.get('desc')
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

if __name__ == '__main__':
    app.run(debug=True,port=8000)