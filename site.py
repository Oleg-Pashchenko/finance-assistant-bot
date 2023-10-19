import json

import plotly
from flask import Flask, render_template
import plotly.express as px
from sqlalchemy import desc, func, and_

import db
from datetime import date, datetime

app = Flask(__name__)


def calculate_percentage(part, whole):
    if whole == 0:
        return 0
    return (part / whole) * 100


@app.route('/<chat_id>')
def index_page(chat_id):
    table1_columns = ["Дата", "Тип", 'Описание', 'Сколько (в ₽)']  # Заголовки колонок для таблицы 1

    last_5_records = db.session.query(db.Operation).filter(db.Operation.owner == chat_id).order_by(
        desc(db.Operation.date)).limit(5)
    last_5_rows = []
    for i in last_5_records:
        last_5_rows.append([i.date, 'Доход' if i.is_income else 'Расход', i.description, i.amount])

    current_datetime = datetime.now()

    # Get the current year, month, and day
    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day

    records = db.session.query(db.Operation).filter(db.Operation.owner == chat_id).all()
    current_income_sum, current_expenses_sum, previous_income_sum, previous_expenses_sum = 0, 0, 0, 0

    for record in records:
        year, month, day = map(int, str(record.date).split('-'))
        if year == current_year and month == current_month and day <= current_day:
            if record.is_income:
                current_income_sum += record.amount
            else:
                current_expenses_sum += record.amount

        prev_year, prev_month = current_year, current_month - 1
        if prev_month == 0:
            prev_year, prev_month = current_year - 1, 12

        if year == prev_year and month == prev_year and day <= current_day:
            if record.is_income:
                previous_income_sum += record.amount
            else:
                previous_expenses_sum += record.amount

    cur_acc_inc, prev_acc_inc = current_income_sum - current_expenses_sum, previous_income_sum - previous_expenses_sum

    labels = ["Доход", "Расход", "Накопления"]
    values = [current_income_sum, current_expenses_sum, cur_acc_inc]

    return render_template('index.html',
                           current_expenses_sum=current_expenses_sum,
                           current_income_sum=current_income_sum,
                           cur_acc_inc=cur_acc_inc,
                           diff_inc=calculate_percentage(min(current_income_sum, previous_income_sum),
                                                         max(current_income_sum, previous_income_sum)),
                           diff_acc=calculate_percentage(min(prev_acc_inc, cur_acc_inc),
                                                         max(prev_acc_inc, cur_acc_inc)),
                           diff_exp=calculate_percentage(min(current_expenses_sum, previous_expenses_sum),
                                                         max(current_expenses_sum, previous_expenses_sum)),
                           table_columns=table1_columns,
                           table_data=last_5_rows, labels=labels, values=values, label='Графическое представление анализа'
                           )


@app.route('/income-review/')
def income_review_page():
    return render_template('templates/income_review_page.html')


@app.route('/expenses-review/')
def expenses_review_page():
    return render_template('templates/expenses_review_page.html')


@app.route('/accumulations-review/')
def accumulations_review_page():
    return render_template('templates/accumulations_review_page.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
