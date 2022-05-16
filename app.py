from flask import Flask , render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import flask_login
import flask
import bcrypt


app = Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'the secret key'
db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

salt = bcrypt.gensalt()
users = {'admin@admin.cz': {'password': b'$2b$12$M.JDqsstBqexzyToKipXsunrWO0gc/lTWpMi6qbCx1VuXfvQaf2fW'} , 'nik': {'password': bcrypt.hashpw('heslo'.encode('utf-8'), salt)}}
        

class User(flask_login.UserMixin):
    pass

#
@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user



@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = flask.request.form['email']
    if email in users and bcrypt.checkpw(flask.request.form['password'].encode('utf-8'), users[email]['password']):
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))
 
    ##return 'Špatné jméno nebo heslo' , {"Refresh": "2; url=http://127.0.0.1:5000/"}
    return 'Špatné jméno nebo heslo' , {"Refresh": "2; url=https://tranquil-thicket-20550.herokuapp.com/"}

@app.route('/logout')
def logout():
    flask_login.logout_user()
    ##return 'Úspěšně odhlášeno' , {"Refresh": "2; url=http://127.0.0.1:5000/"}
    return 'Úspěšně odhlášeno' , {"Refresh": "2; url=https://tranquil-thicket-20550.herokuapp.com/"}

@app.route('/protected')
@flask_login.login_required
def protected():
    ##return 'Přihlášen jako: ' + flask_login.current_user.id , {"Refresh": "2; url=http://127.0.0.1:5000/"}
    return 'Přihlášen jako: ' + flask_login.current_user.id , {"Refresh": "2; url=https://tranquil-thicket-20550.herokuapp.com/"}

class Todo(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete= db.Column(db.Boolean)

@app.route ('/')
def index():
    #Ukaž všechny úkoly 
    #print(bcrypt.hashpw('secret'.encode('utf-8'), salt))
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/done")
def done():
    #zobraz jen splnené úkoly 
    todo_list = Todo.query.filter_by(complete=True).all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/nope")
def nope():
    #zobraz jen nesplnené úkoly 
    todo_list = Todo.query.filter_by(complete=False).all()
    return render_template("base.html", todo_list=todo_list)    

@app.route ('/add', methods=["POST"])
@flask_login.login_required
def add():
    #přidej nový úkol
    title = request.form.get("title") 
    new_todo = Todo(title=title, complete=False ) 
    db.session.add(new_todo)   
    db.session.commit()
    return redirect(url_for("index"))

@app.route ('/update/<int:todo_id>')
@flask_login.login_required
def update(todo_id):
    #změn na hotovo/nehotovo 
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route ('/delete/<int:todo_id>')
@flask_login.login_required
def delete(todo_id):
    #smaž úkol
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.errorhandler(401)
def autorizace(e):
   ## return 'Aby jsi mohl přidávát úkoly, mazat je nebo aktualizovat, musíš být přihlášen !! ' , {"Refresh": "3; url=http://127.0.0.1:5000/"}
   return 'Aby jsi mohl přidávát úkoly, mazat je nebo aktualizovat, musíš být přihlášen !! ' , {"Refresh": "3; url=https://tranquil-thicket-20550.herokuapp.com/"}
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
