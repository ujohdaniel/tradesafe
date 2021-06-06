# Importing the Libraries
from flask import Flask, render_template, request, redirect,session
from datetime import datetime
import dateparser
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField

app= Flask(__name__)
app.config['SECRET_KEY']= 'tradesafeissafe'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///tradesafe.db'
db= SQLAlchemy(app)

# Creating the tables of the database
class Registration_form(db.Model):
    id= db.Column(db.Integer, primary_key=True, nullable=False)
    name= db.Column(db.Text, nullable=False)
    account_details= db.Column(db.Text, nullable=False)
    email= db.Column(db.Text, nullable=False)
    amount_paid= db.Column(db.Integer, nullable=False)
    phone_no= db.Column(db.Text, nullable=False)
    # first_month= db.Column(db.DateTime)
    date= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Creating WTForms 
class Reg_form(FlaskForm):
    name= TextField(
        'Full Name', 
    )
    account_details= TextField(
        'Address',
    )
    email= TextField(
        'Email', 
    )
    amount_paid= TextField(
        'Amount paid',
    )
    phone_no= TextField(
        'Phone Number', 
    )
    submit= SubmitField(
        'Submit'
    )

@app.route('/', methods=['GET', 'POST'])
def form():
    reg_data= Reg_form()

    if request.method == 'POST' and  reg_data.validate_on_submit():

        # adding new data from Reg_form to the database
        new_name= reg_data.data['name']
        new_account_details= reg_data.data['account_details']
        new_email= reg_data.data['email']
        new_amount_paid= reg_data.data['amount_paid']
        new_phone_no= reg_data.data['phone_no']

        data= Registration_form(
            name= new_name,
            account_details= new_account_details,
            email= new_email,
            amount_paid= new_amount_paid,
            phone_no= new_phone_no
        )

        try:
            db.session.add(data)
            db.session.commit()
            return redirect('/accounts')
        except:
            return 'An error occured'

    return render_template('form.html', reg_data=reg_data)

@app.route('/accounts')
def accounts():
    reg_data= Reg_form()
    reg_values= Registration_form.query.all()
    
    return render_template('accounts.html', reg_values= reg_values, reg_data=reg_data)

@app.route('/accounts/delete/<int:id>')
def delete(id):
    del_data = Registration_form.query.get_or_404(id)

    try:
        db.session.delete(del_data)
        db.session.commit()
        return redirect('/accounts')
    except:
        return 'An error occured'

@app.route('/accounts/edit/<int:id>', methods= ['GET', 'POST'])
def edit(id):
    reg_data= Reg_form()
    edit_data = Registration_form.query.get_or_404(id)

    if request.method == 'POST':
        edit_data.name = reg_data.data['name']
        edit_data.account_details = reg_data.data['account_details']
        edit_data.email = reg_data.data['email']
        edit_data.amount_paid = reg_data.data['amount_paid']
        edit_data.phone_no = reg_data.data['phone_no']

        try:
            db.session.commit()
            return redirect('/accounts')
        except:
            return 'An error occured'
    else:
        return render_template('edit.html', edit_data= edit_data, reg_data= reg_data)

# Debug mode on
if __name__ == '__main__':
    app.run(debug=True)