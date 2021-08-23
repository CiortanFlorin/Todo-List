from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from forms import CreateList
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = ['awdawdawcwa']
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Create list item class
class ListItem(db.Model):
    __tablename__ = "ListItems"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
db.create_all()

#First page where first item in list can be added
@app.route('/',methods=["POST", "GET"])
def home():
    form = CreateList()
    if form.validate_on_submit():
        new_item = ListItem(item=form.list_item.data, done=False)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template("index.html", form=form)

#List page with option to add more items
@app.route('/list',methods=["POST", "GET"])
def list():
    form = CreateList()
    items = ListItem.query.all()
    if form.validate_on_submit():
        new_item = ListItem(item=form.list_item.data, done=False)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template("list.html", form=form, items=items)

#Page that marks items as done
@app.route("/make-done/<int:item_id>", methods=["GET", "POST"])
def make_done(item_id):
    item = ListItem.query.get(item_id)
    item.done = True
    db.session.commit()
    return redirect(url_for('list'))

if __name__ == "__main__":
    app.run(debug=True)