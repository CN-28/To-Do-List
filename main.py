from flask import Flask, render_template
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
    return render_template('index.html')


if __name__ == '__main__':
    db.create_all()

    app.run(debug=True)