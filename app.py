# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

@app.route('/')
def dashboard():
    expenses = Expense.query.all()
    incomes = Income.query.all()
    budgets = Budget.query.all()
    reminders = Reminder.query.all()
    total_expense = sum(expense.amount for expense in expenses)
    total_income = sum(income.amount for income in incomes)
    remaining_budget = sum(budget.amount for budget in budgets) - total_expense

    return render_template('dashboard.html', total_expense=total_expense, total_income=total_income, remaining_budget=remaining_budget, expenses=expenses, incomes=incomes, budgets=budgets, reminders=reminders)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    category = request.form['expense_category']
    amount = float(request.form['expense_amount'])
    expense = Expense(category=category, amount=amount)
    db.session.add(expense)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_income', methods=['POST'])
def add_income():
    source = request.form['income_source']
    amount = float(request.form['income_amount'])
    income = Income(source=source, amount=amount)
    db.session.add(income)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/set_budget', methods=['POST'])
def set_budget():
    category = request.form['budget_category']
    amount = float(request.form['budget_amount'])
    budget = Budget(category=category, amount=amount)
    db.session.add(budget)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    description = request.form['reminder_description']
    date = datetime.strptime(request.form['reminder_date'], '%Y-%m-%d')
    reminder = Reminder(description=description, date=date)
    db.session.add(reminder)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
