from flask import Flask
from flask_mysqldb import MySQL
from flask import Blueprint, render_template,request, redirect, url_for, session, flash
import MySQLdb.cursors
import re
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'atharva'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'dmsd_final'
mysql = MySQL(app)


@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['Email'])
    return redirect(url_for('login'))


@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        if email == 'admin' and password == 'admin':
            return redirect('/admin')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM CUSTOMER WHERE Email = % s AND Password = % s', (email, password, ))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['CID'] = account['CID']
                session['Email'] = account['Email']
                mesage = 'Logged in successfully !'
                return render_template('home.html', mesage = mesage)
            else:
                mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/query6' , methods =['GET', 'POST'])
def query6():
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select c.CardNumber, sum(a.Quantity*a.PriceSold) as Total_Amount from CART c inner join APPEARS_IN a on c.CartID = a.CartID group by CardNumber')
        data = cursor.fetchall()
        columns = ['CardNumber', 'Total_Amount']
    return render_template('admin_result.html', columns=columns, data=data)

@app.route('/query3', methods =['GET', 'POST'])
def query3():
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select c.CID as Customer_ID, SUM(TotalAmount) as Total_expenditure from cart c group by c.CID order by Total_expenditure DESC LIMIT 10')
        data = cursor.fetchall()
        columns = ['Customer_ID','Total_expenditure']
    return render_template('admin_result.html', data=data, columns=columns)

@app.route('/query1' , methods =['GET', 'POST'])
def query1():
    if request.method == 'POST':
        begindate = request.form['begindate1']
        enddate = request.form['enddate1']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT ProductID, SUM(Quantity) FROM APPEARS_IN a, CART c WHERE a.CartID = c.CartID AND TStatus = % s AND TDate BETWEEN % s AND % s GROUP BY ProductID ORDER BY SUM(Quantity) DESC;',('Done', begindate, enddate))
        data = cursor.fetchall()
        columns = ['ProductID', 'SUM(Quantity)']
    return render_template('admin_result.html', columns=columns, data=data)

@app.route('/query2', methods =['GET', 'POST'])
def query2():
    if request.method == 'POST':
        begindate = request.form['begindate2']
        enddate = request.form['enddate2']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select ProductID, COUNT(DISTINCT CID) from appears_in a, cart c where a.CartID = c.CartID and TStatus = %s and TDate BETWEEN %s and %s group by ProductID order by COUNT(DISTINCT CID) desc;',('Done', str(begindate), str(enddate)))
        data = cursor.fetchall()
        columns = ['ProductID', 'COUNT(DISTINCT CID)']
    return render_template('admin_result.html', data=data, columns=columns)

@app.route('/query4', methods =['GET', 'POST'])
def query4():
    if request.method == 'POST':
        begindate = request.form['begindate4']
        enddate = request.form['enddate4']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT c.CardNumber, MAX(c.TotalAmount) AS MaxBasketTotalAmount FROM CART c WHERE c.TDate BETWEEN %s AND %s GROUP BY c.CardNumber;',(str(begindate), str(enddate)))
        data = cursor.fetchall()
        columns = ['CardNumber', 'MaxBasketTotalAmount']
    return render_template('admin_result.html', data=data, columns=columns)

@app.route('/query5', methods =['GET', 'POST'])
def query5():
    if request.method == 'POST':
        begindate = request.form['begindate5']
        enddate = request.form['enddate5']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select PType, AVG(PPrice) from PRODUCT group by PType;')
        data = cursor.fetchall()
        columns = ['PType', 'AVG(PPrice)']
    return render_template('admin_result.html', data=data, columns=columns)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('CID', None)
    session.pop('Email', None)
    session.pop('total_price',None)
    session.pop('SAName',None)
    session.pop('CardNumber',None)
    session.pop('dict_of_melons',None)
    session.pop('cart',None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        firstname = request.form['Fname']
        lastname = request.form['Lname']
        emailid = request.form['Email']
        address = request.form['Address']
        phonenum = request.form['Phone']
        password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM CUSTOMER WHERE Email = % s', (emailid, ))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
        elif not firstname or not lastname or not emailid or not address or not phonenum or not password:
            message = 'Please fill out the complete form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
            message = 'Invalid email address !'
        
        else:
            cursor.execute("INSERT INTO CUSTOMER(Fname, Lname, Email, Address, Phone, Password) VALUES (% s, % s, % s,% s, % s, % s);", (firstname, lastname, emailid, address, phonenum, password, ))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message = message)

@app.route('/laptop')
def laptop():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM PRODUCT INNER JOIN LAPTOP on PRODUCT.ProductID = LAPTOP.ProductID")
    data = cursor.fetchall()
    return render_template('laptop.html', data = data)

@app.route('/desktop')
def desktop():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM PRODUCT INNER JOIN DESKTOP on PRODUCT.ProductID = DESKTOP.ProductID")
    data = cursor.fetchall()
    return render_template('desktop.html', data = data)

@app.route('/printer')
def printer():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM PRODUCT INNER JOIN PRINTER on PRODUCT.ProductID = PRINTER.ProductID")
    data = cursor.fetchall()
    return render_template('printer.html', data = data)

@app.route('/history')
def history():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM CART WHERE CID = % s",(session['CID'],))
    history = cursor.fetchall()
    return render_template('history.html', history = history)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)
    flash("Successfully added to cart!")
    return redirect("/cart")

@app.route('/cart')
def cart():
    if "cart" not in session:
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        dict_of_melons = {}
        total_price = 0
        for item in items:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM PRODUCT WHERE ProductID = % s', (item, ))
            melon = cursor.fetchone()
            total_price += melon['PPrice']
            if melon['ProductID'] in dict_of_melons:
                dict_of_melons[melon['ProductID']]["qty"] += 1
            else:
                dict_of_melons[melon['ProductID']] = {"qty":1, "name": melon['Pname'], "price":melon['PPrice']}
        session['dict_of_melons'] = dict_of_melons
        session['total_price'] = total_price
        return render_template("cart.html", display_cart = dict_of_melons, total = total_price)  

@app.route("/address")
def address():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM SHIP_ADDRESS WHERE CID = % s",(session['CID'],))
    address = cursor.fetchall()
    return render_template('address.html', address = address)

@app.route('/addaddress', methods =['GET', 'POST'])
def addaddress():
    if request.method == 'POST':
        SAName = request.form['SAName']
        RecipientName = request.form['RecipientName']
        SNumber = request.form['SNumber']
        Street = request.form['Street']
        SAName = request.form['SAName']
        Zip = request.form['Zip']
        City = request.form['City']
        State = request.form['State']
        Country = request.form['Country']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO SHIP_ADDRESS (SAName,CID,RecipientName,SNumber,Street,Zip,City,State,Country) VALUES (% s, % s, % s,% s, % s, % s,% s, % s, % s)",(SAName,session['CID'],RecipientName,SNumber,Street,Zip,City,State,Country,))
        mysql.connection.commit()
        session['SAName'] = SAName
        return redirect('/new_credit')
    return render_template('addaddress.html')

@app.route("/credit/<SAName>")
def credit(SAName):
    session['SAName'] = SAName
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM CREDIT_CARD WHERE CID = % s",(session['CID'],))
    credit = cursor.fetchall()
    return render_template('credit.html', credit = credit)


@app.route('/new_credit', methods =['GET', 'POST'])
def new_credit():
    if request.method == 'POST':
        CardNumber = request.form['CardNumber']
        SecNumber = request.form['SecNumber']
        CardOwnerName = request.form['CardOwnerName']
        CardType = request.form['CardType']
        BillingAddress = request.form['BillingAddress']
        ExpDate = request.form['ExpDate']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO CREDIT_CARD (CardNumber,SecNumber,CardOwnerName,CardType,BillingAddress,ExpDate,CID) VALUES (% s, % s, % s,% s, % s, % s,% s);",(CardNumber,SecNumber,CardOwnerName,CardType,BillingAddress,ExpDate,session['CID'],))
        mysql.connection.commit()
        session['CardNumber'] = str(CardNumber)
        return redirect("/ordercomplete")
    return render_template("new_credit.html")

@app.route("/ordercomplete/<CardNumber>")
def ordercomplete(CardNumber):
    session['CardNumber'] = str(CardNumber)
    now = datetime.now()
    cartid = int(now.strftime('%H%M%S'))
    date = now.strftime('%Y-%m-%d')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO CART (CartID,TStatus,TDate,TotalAmount,CardNumber,SAName,CID) VALUES (% s, 'Done', % s,% s, % s, % s,% s)",(cartid,date,session['total_price'],session['CardNumber'],session['SAName'],session['CID'],))
    mysql.connection.commit()
    item_dict = session['dict_of_melons']
    keys = list(item_dict.keys())
    for i in keys:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO APPEARS_IN (CartID,ProductID,Quantity,PriceSold) VALUES (% s,% s, % s, % s)",(cartid,int(i),item_dict[i]['qty'],item_dict[i]['price'],))
        mysql.connection.commit()

    session.pop('total_price',None)
    session.pop('SAName',None)
    session.pop('CardNumber',None)
    session.pop('dict_of_melons',None)
    session.pop('cart',None)
    return redirect('/history')

@app.route("/ordercomplete")
def ordercomplete_new():
    now = datetime.now()
    cartid = int(now.strftime('%H%M%S'))
    date = now.strftime('%Y-%m-%d')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO CART (CartID,TStatus,TDate,TotalAmount,CardNumber,SAName,CID) VALUES (% s, 'Done', % s,% s, % s, % s,% s)",(cartid,date,session['total_price'],session['CardNumber'],session['SAName'],session['CID'],))
    mysql.connection.commit()
    item_dict = session['dict_of_melons']
    keys = list(item_dict.keys())
    for i in keys:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO APPEARS_IN (CartID,ProductID,Quantity,PriceSold) VALUES (% s,% s, % s, % s)",(cartid,int(i),item_dict[i]['qty'],item_dict[i]['price'],))
        mysql.connection.commit()

    session.pop('total_price',None)
    session.pop('SAName',None)
    session.pop('CardNumber',None)
    session.pop('dict_of_melons',None)
    session.pop('cart',None)
    return redirect('/history')

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        current_user = session['Email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM CUSTOMER WHERE Email = % s', (current_user, ))
        account = cursor.fetchone()
        return render_template('profile.html', account = account)
    return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)