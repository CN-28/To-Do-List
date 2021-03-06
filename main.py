from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

#application setup
app = Flask(__name__)

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDoElement(db.Model):
    #we want a integer value to be unique
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    done = db.Column(db.Boolean)


#creating main page
@app.route('/')
def index():
    ArrayOfToDoList = ToDoElement.query.all()
    return render_template('index.html', ArrayOfToDoList=ArrayOfToDoList)


#function which adds functionality to our "ADD" button
@app.route('/add', methods=["POST"])
def add_new_element():
    elem_name = request.form.get("enter")
    element = ToDoElement(title=elem_name, done=False)
    db.session.add(element)
    #saving changes in database
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/modify/<int:element_id>')
def modify(element_id):
    #we query database to get this element
    element = ToDoElement.query.filter_by(id=element_id).first() 
    element.done = not element.done
    #saving changes in database
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/remove/<int:element_id>')
def remove(element_id):
    #we query database to get this element
    element = ToDoElement.query.filter_by(id=element_id).first() 
    #deleting element form database
    db.session.delete(element)
    #saving changes in database
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == '__main__':
    db.create_all()
    #runing the site
    app.run(debug=True)