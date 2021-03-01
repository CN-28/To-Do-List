from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

#application setup
app = Flask(__name__)

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDoList(db.Model):
    #we want integer value to be unique
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    full = db.Column(db.Boolean)

#creating main page
@app.route('/')
def index():
    ArrayOfToDoList = ToDoList.query.all()
    print(ArrayOfToDoList)
    return render_template('index.html', ArrayOfToDoList=ArrayOfToDoList)

#function which adds functionality to our "ADD" button
@app.route('/add', methods=["POST"])
def add_new_element():
    elem_name = request.form.get("enter")
    element = ToDoList(title=elem_name, full=False)
    db.session.add(element)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/mark_as_done/<int:elem_id>', methods=["POST"])
def mark_as_done():
    #we query database to get this element
    element = ToDoList.query.filter(id=elem_id).first() 
    element.full = True
    #saving changes in database
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int: elem_id>', methods=["POST"])
def delete():
    #we query database to get this element
    element = ToDoList.query.filter(id=elem_id).first() 
    #deleting element form database
    db.session.delete(element)
    #saving changes in database
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)