from flask import Flask, render_template ,request ,jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')  
db = client['library']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/new_book', methods=['GET', 'POST'])
def new_book():
     data_inserted = False
     
     if request.method == 'POST':
        book_title = request.form.get('title')
        book_author = request.form.get('author')
        book_lan = request.form.get('language')
        book_pgno = request.form.get('pageNumber')
        book_pd = request.form.get('publicationDate')
        book_publisher = request.form.get('publisher')
        book_quant = request.form.get('quantity')
        book_genre = request.form.get('genre')

        collection = db['books']
        collection.insert_one({'title': book_title, 'author': book_author, 'language':book_lan, 'pageNumber':book_pgno, 'publicationDate':book_pd, 'publisher':book_publisher, 'quantity':book_quant, 'genre':book_genre})

        data_inserted = True
        
     collection = db['books']
     data = collection.find()

     return render_template('new_book.html', data=data, data_inserted=data_inserted)

@app.route('/get_book')
def get_book():
    collection = db['books']
    books_cursor = collection.find({}, {'_id': 0, 'title': 1, 'author': 1, 'language': 1})
    books = list(books_cursor)
    return jsonify(books)

@app.route('/new_member')
def new_member():
    return render_template('new_member.html')

@app.route('/new_member', methods=['GET', 'POST'])
def new_member1():
    data_inserted = False

    if request.method == 'POST':
        member_name = request.form.get('name')
        member_address = request.form.get('address')
        member_phone = request.form.get('phone')
        member_dob = request.form.get('dob')
        member_email = request.form.get('email')
        member_gender = request.form.get('gender')

        collection = db['members']
        collection.insert_one({
            'name': member_name,
            'address': member_address,
            'phone': member_phone,
            'dob': member_dob,
            'email': member_email,
            'gender': member_gender
        })

        data_inserted = True

    return render_template('new_member.html', data_inserted=data_inserted)

@app.route('/get_member')
def get_member():
    collection = db['members']
    members_data = collection.find({}, {'name': 1, 'phone': 1, '_id': 0})

    return render_template('get_member.html', members_data=members_data)

@app.route('/total_books')
def total_books():
    collection = db['books']
    total_count = collection.count_documents({})
    return jsonify({'total_Books': total_count})

@app.route('/total_members')
def total_members():
    collection = db['members']
    total_count = collection.count_documents({})
    return jsonify({'total_members': total_count})

@app.route('/new_transaction', methods=['GET', 'POST'])
def new_transaction():
    if request.method == 'POST':
        member_name = request.form.get('member_name')
        book_title = request.form.get('book_title')
        transaction_type = request.form.get('transaction_type')
        date_of_rent = request.form.get('dob1')
        date_of_return = request.form.get('dob2')

        if date_of_rent:
            date_of_rent = datetime.strptime(date_of_rent, '%Y-%m-%d')
        else:
            date_of_rent = None

        if date_of_return:
            date_of_return = datetime.strptime(date_of_return, '%Y-%m-%d')
        else:
            date_of_return = None

        collection = db['transaction']
        collection.insert_one({
            'member_name': member_name,
            'book_title': book_title,
            'transaction_type': transaction_type,
            'date_of_rent': date_of_rent,
            'date_of_return': date_of_return
        })

    return render_template('new_transaction.html')

@app.route('/get_transaction')
def get_transaction():
    collection = db['transaction']
    transactions_data = collection.find({}, {'_id': 0})
    transactions_list = list(transactions_data)
    return jsonify(transactions_list)


if __name__ == '__main__':
    app.run()
