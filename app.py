
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Karthik:01",
        database="zomato"
    )


# ----------------------------
# CUSTOMER REGISTRATION PAGE
# ----------------------------
@app.route("/")
def customer_page():
    return render_template("customer.html")


# ----------------------------
# REGISTER CUSTOMER
# ----------------------------
@app.route("/register_customer", methods=["POST"])
def register_customer():

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    phone = request.form.get("phone_number")
    email = request.form.get("email")

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO customers(first_name,last_name,phone_number,email)
    VALUES(%s,%s,%s,%s)
    """,(first_name,last_name,phone,email))

    conn.commit()

    user_id = cursor.lastrowid

    cursor.close()
    conn.close()

    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("home.html", items=items, user_id=user_id)


@app.route("/place_order", methods=["POST"])
def place_order():

    user_id = request.form.get("user_id")
    address = request.form.get("address")

    conn = create_connection()
    cursor = conn.cursor()

    # create order
    cursor.execute(
        "INSERT INTO orders(user_id,delivery_address) VALUES(%s,%s)",
        (user_id,address)
    )

    order_id = cursor.lastrowid

    cursor.execute("SELECT item_id,price FROM items")
    items = cursor.fetchall()

    total = 0
    item_added = False

    for item in items:
        item_id = item[0]
        price = float(item[1])

        quantity = int(request.form.get(f"item_{item_id}", 0))

        if quantity > 0:
            item_added = True

            cursor.execute("""
            INSERT INTO order_items(order_id,item_id,quantity,price)
            VALUES(%s,%s,%s,%s)
            """,(order_id,item_id,quantity,price))

            total += price * quantity

    # If no item selected
    if not item_added:
        cursor.close()
        conn.close()
        return "<h2>Please select at least one item.</h2><a href='/'>Go Back</a>"

    cursor.execute("""
    INSERT INTO payments(order_id,payment_method,payment_status,amount)
    VALUES(%s,%s,%s,%s)
    """,(order_id,"Cash","Pending",total))

    conn.commit()

    cursor.close()
    conn.close()

    return render_template(
        "order_success.html",
        order_id=order_id,
        total=total
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
