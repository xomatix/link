from flask import Flask, flash,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    old_link = db.Column(db.String(200), nullable=False)
    new_link = db.Column(db.String(200), nullable=False)

    def getLink(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        old_link = request.form['old_link']
        new_link = request.form['new_link']
        if old_link.startswith('http://') or old_link.startswith('https://'):
            generate_link = Link(old_link=old_link, new_link=new_link)
            try:
                db.session.add(generate_link)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue while generating link'
          
        else:
            old_link = 'http://' + old_link
            generate_link = Link(old_link=old_link, new_link=new_link)
            try:
                db.session.add(generate_link)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue while generating link' 
    else:
        links = Link.query.order_by(Link.id).all()
        return render_template('index.html', links=links)

@app.route('/delete/<int:id>')
def delete(id):
    link_to_delete = Link.query.get_or_404(id)

    try:
        db.session.delete(link_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return'something went wroong when deleting'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    link = Link.query.get_or_404(id)
    
    if request.method == "POST":
        link.old_link = request.form['old_link']
        old_link = link.old_link
        link.new_link = request.form['new_link']
        if old_link.startswith('http://') or old_link.startswith('https://'):
            try:
                db.session.commit()
                return redirect('/')
            except:
                return'something went wrong when updating'
    else:
        return render_template('update.html', link=link)

@app.route('/<string:new_link>')
def final_link(new_link):
    link = Link.query.filter_by(new_link=new_link).first()
    direction = link.old_link
    return redirect(direction, code=302)
 

if __name__ == "__main__":
    app.run(debug=True)
