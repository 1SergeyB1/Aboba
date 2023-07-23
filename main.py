from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from requests import post
import os

IMG_FOLDER = os.path.join('avatars')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data.db'
db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String())
    page_name = db.Column(db.String(20))
    footer = db.Column(db.String())
    content = db.Column(db.String())
    header = db.Column(db.String())

@app.route('/', methods=['POST', 'GET'])
def index():
    db.create_all()
    data = Data.query.order_by(Data.id).all()
    page = []
    for i in data:
        page.append([i.id, i.page_name])
    return render_template('index.html', pages_name = page)

@app.route('/Create', methods=['POST', 'GET'])
def CreatePage():

    if request.method == "POST":
        page = Data()
        page.page_name = request.form['name']
        page.image = request.form['image']
        page.header = request.form['header']
        page.content = request.form['content']
        page.footer = request.form['footer']
        try:
            db.session.add(page)
            db.session.commit()
            return 'done'
        except:
            return redirect('/Create')
    return render_template('CreateNewPage.html')

@app.route('/page/<int:index>', methods=['POST', 'GET'])
def page(index):
    content = db.session.get(Data, index)
    if content:
        return render_template('page.html', content = content)
    else:
        return 'Страница не найдена'

if __name__ == "__main__":
    app.run(debug=False)
