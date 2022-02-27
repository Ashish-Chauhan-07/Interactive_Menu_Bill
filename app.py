from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, UserMixin
import json
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/3b_db'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_chef = db.Column(db.Integer, nullable=False)  # 0-user, 1-chef


class Menu(db.Model):
    Item_no = db.Column(db.Integer, primary_key=True)
    Half_Plate = db.Column(db.Integer, nullable=False)
    Full_Plate = db.Column(db.Integer, nullable=False)


class Transaction(db.Model):
    txn_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    items = db.Column(db.String(2000), nullable=False)
    total = db.Column(db.Float, nullable=False)
    tip_percent = db.Column(db.Float, nullable=False)
    dis_or_inc = db.Column(db.Float, nullable=False)
    final_total = db.Column(db.Float, nullable=False)
    updated_share_per_head = db.Column(db.Float, nullable=False)


@app.route('/get/menu', methods=['GET'])
def menu_get():
    with open("Menu.csv", 'r') as menu:
        csvreader = csv.reader(menu)
        col_names = next(csvreader)

        for row in csvreader:
            item_num = (int(row[0]))
            half_price = (int(row[1]))
            full_price = (int(row[2]))
            menu_obj = Menu(Item_no=item_num, Half_Plate=half_price,
                            Full_Plate=full_price)
            db.session.add(menu_obj)
            db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/customer/login', methods=['POST'])
def customer_login():
    data = json.loads(request.get_json())
    username = data.get('user_name')
    password = data.get('password')
    user = User.query.filter_by(user_name=username).first()
    if(user is not None):
        if(user.password == password):
            login_user(user)
            msg = str(username) + " has LOGGED IN successfully."
            return "<<-- " + msg + " -->\n"
        else:
            return "Try again with correct Password.\n"
    else:
        msg = str(username) + " doesn't exist in records as Customer. \n"
        return msg


@app.route('/chef/login', methods=['POST'])
def chef_login():
    data = json.loads(request.get_json())
    username = data.get('user_name')
    password = data.get('password')
    check_chef = data.get('is_chef')
    user = User.query.filter_by(user_name=username).first()
    if(user is not None):
        if(user.password == password and check_chef == 1):
            login_user(user)
            msg = "<<-- Welcome Chef " + str(username) + " -->>\n"
            msg += "<<-- You've LOGGED IN successfully. -->>\n"
            return msg
        else:
            return "Try again with correct Password.\n"
    else:
        msg = str(username) + " doesn't exist in records as Chef. \n"
        return msg


@app.route('/customer/signup', methods=['POST'])
def customer_signup():
    data = json.loads(request.get_json())
    username = data.get('user_name')
    password = data.get('password')
    user = User.query.filter_by(user_name=username, is_chef=0).first()
    if(user is not None):
        msg = str(username) + " already exist in our records as a Customer.\n"
        msg += "Try logging in yourself. \n"
        return msg
    else:
        user_obj = User(user_name=username, password=password, is_chef=0)
        db.session.add(user_obj)
        db.session.commit()
        msg = "<<-- " + str(username) + \
            " has signed up as a Customer Successfully -->>"
        return msg


@app.route('/chef/signup', methods=['POST'])
def chef_signup():
    data = json.loads(request.get_json())
    username = data.get('user_name')
    password = data.get('password')
    user = User.query.filter_by(user_name=username, is_chef=1).first()
    if(user is not None):
        msg = str(username) + " already exist in our records as a Chef.\n"
        msg += "Try logging in yourself. \n"
        return msg
    else:
        user_obj = User(user_name=username, password=password, is_chef=1)
        db.session.add(user_obj)
        db.session.commit()
        msg = "<<-- " + str(username) + \
            " has signed up as a Chef Successfully -->>"
        return msg


@app.route('/users', methods=['GET'])
def get_users():
    response = []
    result = User.query.all()
    for obj in result:
        row = dict()
        row['username'] = obj.user_name
        row['password'] = obj.password
        row['type'] = "chef" if obj.is_chef == 1 else "customer"
        response.append(row)
    return json.dumps(response)


@app.route('/customer/signout', methods=['GET'])
def customer_signout():
    logout_user()
    msg = "<<-- LOGGED OUT -->>"
    return msg


@app.route('/chef/signout', methods=['GET'])
def chef_signout():
    logout_user()
    msg = "<<-- LOGGED OUT -->>"
    return msg


@app.route('/menu', methods=['GET'])
def retrieve_menu():
    response = []
    results = Menu.query.all()
    for item in results:
        row = dict()
        row['id'] = item.Item_no
        row['half'] = item.Half_Plate
        row['full'] = item.Full_Plate
        response.append(row)
    return json.dumps(response)


@app.route('/add/menu', methods=['POST'])
def add_menu():
    data = json.loads(request.get_json())
    item = data.get('item_id')
    half_price = data.get('half')
    full_price = data.get('full')
    new_item = Menu(Item_no=item, Half_Plate=half_price, Full_Plate=full_price)
    db.session.add(new_item)
    db.session.commit()
    msg = "New ITEM Added Successfully.\n"
    msg += "<<-- Review Menu to Check -->>"
    return msg


@app.route('/add/transaction', methods=['POST'])
def add_transaction():
    data = json.loads(request.get_json())
    username = data.get('username')
    item = data.get('item_id')
    total = data.get('total')
    tip = data.get('tip_percent')
    dis_inc = data.get('dis_inc')
    final_total = data.get('final_total')
    share = data.get('updated_share_per_head')
    transaction = Transaction(user_name=username, items=item, total=total, tip_percent=tip,
                              dis_or_inc=dis_inc, final_total=final_total, updated_share_per_head=share)
    db.session.add(transaction)
    db.session.commit()
    msg = "<<-- Order has been recorded successfully -->>\n"
    msg += "<<-- You can view transactions made/ order again -->>\n"
    return msg


@app.route('/list/transactions', methods=['GET'])
def list_transactions():
    data = json.loads(request.get_json())
    username = data.get('user_name')
    bill_statements = Transaction.query.filter_by(user_name=username).all()
    response = []
    if bill_statements is None:
        msg = "There has been no Transaction recorded yet.\n"
        msg += "<<-- Kindly Order some Items -->>\n"
        return msg
    else:
        for bill in bill_statements:
            row = dict()
            row['txn_num'] = bill.txn_id
            row['username'] = bill.user_name
            row['final_total'] = bill.final_total
            response.append(row)
        return json.dumps(response)


@app.route('/bill', methods=['GET'])
def get_bill():
    data = json.loads(request.get_json())
    transaction_number = data.get('transactionNumber')
    bill_details = Transaction.query.filter_by(txn_id=transaction_number)
    response = []
    for bill in bill_details:
        row = dict()
        row['txn_num'] = bill.txn_id
        row['username'] = bill.user_name
        row['items'] = bill.items
        row['total'] = bill.total
        row['tip'] = bill.tip_percent
        row['final_total'] = bill.final_total
        row['dis_inc'] = bill.dis_or_inc
        row['share'] = bill.updated_share_per_head
        response.append(row)
    return json.dumps(response)


if(__name__ == '__main__'):
    db.create_all()
    app.run(port=8000, debug=True)
