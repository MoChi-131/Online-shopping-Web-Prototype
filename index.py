from datetime import datetime
from flask import Flask, render_template, session, request, g
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_session import Session
from wtforms import StringField, SubmitField,MonthField, RadioField,IntegerField, HiddenField
from wtforms.validators import ValidationError,NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"]="filesystem"
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Session(app)

app.app_context().push()

def validate_card_number(form, field):
    card_number = field.data
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValidationError('Card number must be 16 digits')

def validate_cvv_number(form, field):
    cvv_number = field.data
    if len(cvv_number) != 3 or not cvv_number.isdigit():
        raise ValidationError('CVV must be 3 digits ')

def validate_addresss(form, field):
    addresss = field.data
    if len(addresss) <= 5 :
        raise ValidationError('The length of address must be more then 5')
    
def validate_postcode(form, field):
    postcode = field.data
    if len(postcode) != 8 :
        raise ValidationError('The length of post code must be more then 7')

def validate_phone(form, field):
    phone = field.data
    if len(phone) != 11 :
        raise ValidationError('Phone Number must be 11 digits')

def dataRequired(form, field):
    value = field.data
    if value is None or value.strip() == '':
        raise ValidationError('The field is required')
    
def dateRequired(form, field):
    g.when = datetime.now().strftime('%m:%y')
    value = field.data
    if value is None :
        raise ValidationError('The field is required')
    if datetime.strptime(g.when, '%m:%y').date() > value:
        raise ValidationError('Invaild date')


class SortForm(FlaskForm):
    order = RadioField('Order', choices=[('price_asc', 'Price from low to high'), ('price_desc', 'Price from high to low'),
                                               ('name_asc', 'Name from A to z'), ('name_desc', 'Name from z to A'),
                                               ('type_asc', 'Type from A to z'), ('type_desc', 'Type from z to A')], default='price_asc')
    submit = SubmitField('Confirm')

class Quantity(FlaskForm):
    quantity = IntegerField('Quantity', default = 1)
    submit = SubmitField("Add to Basket")

class Basket_AddDrop(FlaskForm):
    quantity = IntegerField('', default =0,validators=[NumberRange(min=0)])

class PayForm(FlaskForm):
    name = StringField('Card holder name', validators=[dataRequired])
    card_no = StringField('Card number', validators= [dataRequired,validate_card_number])
    expire_date = MonthField('Expire Date (MM/YYYY)',format='%m/%Y', validators=[dateRequired])
    cvv = StringField('CVV', validators=[dataRequired,validate_cvv_number])
    address = StringField('Bill Address', validators=[dataRequired, validate_addresss])
    postcode = StringField('Post code', validators=[dataRequired, validate_postcode])
    phone = StringField('Phone Number (e.g 07891234567)', validators=[dataRequired, validate_phone])
    submit = SubmitField('Submit')

class Item(db.Model):
    __tablename__ = 'Items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)
    type = db.Column(db.String(40))
    price = db.Column(db.Integer)
    picture = db.Column(db.String(200))
    detail = db.Column(db.String(1000))

    def __repr__(self):
        return f'<ID:{self.id}<name: {self.name}><price: {self.price}><url: {self.picture}\n'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)

    def __repr__(self):
        return '<User {0}>'.format(self.name)
        
    
def quantity_check_append(form, item):
    submit = False
    if form.validate_on_submit():
        submit = True
        quantity = int(form.quantity.data)
        if quantity == 0:
            submit = False
        if submit:
            list_item = [item, quantity]
            append_order(list_item)
        return (submit)

def append_order(order):
    cart = session["basket"]
    item_id = order[0].id
    quantity = order[1]
    add=False

    for x in cart:
        if x[0].id == item_id:
            x[1] +=quantity
            add = True
    if add == False:
        session["basket"].append(order)

def total():
    cart = session["basket"]
    sum=0
    for x in cart:
        sum+=x[0].price * int(x[1])
    return sum



@app.before_request
def before_request():
    if session.get("basket") is None:
        session["basket"]=[]

@app.route('/', methods=['GET', 'POST'])
def index():
    sort = SortForm()
    items = db.session.query(Item).all()
    if sort.validate_on_submit():
        if sort.order.data == 'price_asc':
            items = db.session.query(Item).order_by(Item.price.asc()).all()
        elif sort.order.data == 'price_desc':
            items = db.session.query(Item).order_by(Item.price.desc()).all()
        elif sort.order.data == 'name_asc':
            items = db.session.query(Item).order_by(Item.name.asc()).all()
        elif sort.order.data == 'name_desc':
            items = db.session.query(Item).order_by(Item.name.desc()).all()
        elif sort.order.data == 'type_asc':
            items = db.session.query(Item).order_by(Item.type.asc()).all()
        elif sort.order.data == 'type_desc':
            items = db.session.query(Item).order_by(Item.type.desc()).all()

    return render_template('index.html', items=items, sort=sort)

@app.route('/detail/<int:id>', methods=['GET', 'POST'])
def detail(id):
    item = Item.query.get(id)
    quantity_form = Quantity()
    submit = quantity_check_append(quantity_form,item)
    return render_template('detail.html', item=item, form=quantity_form, submit=submit)    

@app.route('/basket/<int:item_id>/<int:update>', methods=['GET', 'POST'])
def basket(item_id, update):
    carts = session["basket"]
    quantity = 1
    form= Basket_AddDrop()
    if update == 1:
            quantity = int(request.form.get('quantity', 1))
    if item_id >0:
        item = Item.query.get(item_id)
        for x in carts:
            if x[0].id == item.id:
                x[1] = quantity
    sum = total()
    if len(carts)==0 or sum == 0:
        condition = False
    else:
        condition= True
    return render_template('basket.html', items=carts, condition=condition,sum=sum,item_change=quantity, form=form)

@app.route('/payment/<int:sum>', methods=['GET', 'POST'])
def payment(sum):
    name = None
    form = PayForm()
    submit = False
    if form.validate_on_submit():
        submit = True
        name = form.name.data
        if User.query.filter_by(name=name).first() is None:
            db.session.add(User(name=name))
            db.session.commit()
    return render_template('payment.html', form=form, submit=submit, sum=sum)

        

if __name__ == '__main__':
    # Create the database tables
    db.create_all()

    # Run the application
    app.run(debug=True)
