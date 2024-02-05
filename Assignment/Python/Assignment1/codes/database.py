import mysql.connector
from datetime import datetime

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="techshop"
)
cursor = conn.cursor()

# Task 1: Customer Registration
def register_customer(customerid,first_name, last_name, email, phone):
    try:
        # Check for duplicate email
        cursor.execute("SELECT * FROM Customers WHERE Email = %s", (email,))
        existing_customer = cursor.fetchone()

        if existing_customer:
            print("Error: Duplicate email address.")
            return

        # Insert new customer
        query = "INSERT INTO Customers (customerid,FirstName, LastName, Email, Phone) VALUES (%s,%s, %s, %s, %s)"
        cursor.execute(query, (customerid,first_name, last_name, email, phone))
        conn.commit()
        print("Customer registered successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Task 2: Product Catalog Management
def update_product(product_id, new_price, new_description):
    try:
        # Update product information
        query = "UPDATE Products SET Price = %s, Description = %s WHERE ProductID = %s"
        cursor.execute(query, (new_price, new_description, product_id))
        conn.commit()
        print("Product information updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Task 3: Placing Customer Orders
def place_order(orderid,customer_id, product_id, quantity):
    try:
        # Check product availability in inventory
        cursor.execute("SELECT QuantityInStock FROM Inventory WHERE ProductID = %s", (product_id,))
        available_quantity = cursor.fetchone()[0]

        if available_quantity < quantity:
            print("Error: Insufficient stock.")
            return

        # Insert new order
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query_insert_order = "INSERT INTO Orders (orderid,CustomerID, OrderDate, TotalAmount) VALUES (%s,%s, %s, %s)"
        cursor.execute(query_insert_order, (orderid,customer_id, order_date, 0))
        conn.commit()

        # Get the newly created order ID
        query_get_new_order_id = "SELECT LAST_INSERT_ID();"
        cursor.execute(query_get_new_order_id)
        new_order_id = cursor.fetchone()[0]
        
        '''        
        orderdetailid=orderid
        # Insert order details
        query_insert_order_details = "INSERT INTO OrderDetails (orderdetailid,OrderID, ProductID, Quantity) VALUES (%s,%s, %s, %s)"
        cursor.execute(query_insert_order_details, (orderdetailid,new_order_id, product_id, quantity))
        conn.commit()
        
        # Update inventory quantity
        query_update_inventory = "UPDATE Inventory SET QuantityInStock = QuantityInStock - %s WHERE ProductID = %s"
        cursor.execute(query_update_inventory, (quantity, product_id))
        conn.commit()
        '''

        print("Order placed successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Task 4: Tracking Order Status
def track_order_status(order_id):
    try:
        # Retrieve order status
        query = "SELECT Status FROM Orders WHERE OrderID = %s"
        cursor.execute(query, (order_id,))
        status = cursor.fetchone()

        if status:
            print(f"Order {order_id} status: {status[0]}")
        else:
            print("Error: Order not found.")
    except Exception as e:
        print(f"Error: {e}")

# Task 5: Inventory Management
def add_new_product(productid,product_name, description, price, quantity_in_stock):
    try:
        # Insert new product
        query_insert_product = "INSERT INTO Products (productid,ProductName, Description, Price) VALUES (%s,%s, %s, %s)"
        cursor.execute(query_insert_product, (productid,product_name, description, price))
        conn.commit()

        # Get the newly created product ID
        query_get_new_product_id = "SELECT LAST_INSERT_ID();"
        cursor.execute(query_get_new_product_id)
        new_product_id = cursor.fetchone()[0]
        '''
        # Add product to inventory
        inventoryid=productid
        query_add_to_inventory = "INSERT INTO Inventory (inventoryid,ProductID, QuantityInStock) VALUES (%s,%s, %s)"
        cursor.execute(query_add_to_inventory, (inventoryid,new_product_id, quantity_in_stock))
        conn.commit()
        '''
        print("New product added to inventory successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Task 6: Sales Reporting
def generate_sales_report(start_date, end_date):
    try:
        # Retrieve sales data based on specified criteria
        query = """
            SELECT Orders.OrderID, Customers.FirstName, Customers.LastName, Orders.OrderDate, Orders.TotalAmount
            FROM Orders
            JOIN Customers ON Orders.CustomerID = Customers.CustomerID
            WHERE Orders.OrderDate BETWEEN %s AND %s
        """
        cursor.execute(query, (start_date, end_date))
        sales_data = cursor.fetchall()

        if sales_data:
            print("Sales Report:")
            for row in sales_data:
                print(f"OrderID: {row[0]}, Customer: {row[1]} {row[2]}, OrderDate: {row[3]}, TotalAmount: {row[4]}")
        else:
            print("No sales data found for the specified period.")
    except Exception as e:
        print(f"Error: {e}")

# Task 7: Customer Account Updates
def update_customer_account(customer_id, new_email, new_phone):
    try:
        # Update customer account details
        query = "UPDATE Customers SET Email = %s, Phone = %s WHERE CustomerID = %s"
        cursor.execute(query, (new_email, new_phone, customer_id))
        conn.commit()
        print("Customer account updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Task 8: Payment Processing
#No table for payments
        
# Task 9: Product Search and Recommendations
def search_products(search_criteria):
    try:
        # Search for products based on criteria
        query = "SELECT * FROM Products WHERE ProductName LIKE %s OR Description LIKE %s"
        cursor.execute(query, (f"%{search_criteria}%", f"%{search_criteria}%"))
        search_result = cursor.fetchall()

        if search_result:
            print("Search Results:")
            for product in search_result:
                print(product)
        else:
            print("No products found for the specified criteria.")
    except Exception as e:
        print(f"Error: {e}")

#Task 1: Customer Registration
register_customer(15,"Rohan1", "Chaudhari1", "Rohan1@example.com", "1234756890")

# Task 2: Product Catalog Management
update_product(2, 150.0, "Upgraded speed upto 150mbps")

# Task 3: Placing Customer Orders
place_order(20,1, 2, 3)

# Task 4: Tracking Order Status
track_order_status(1)

# Task 5: Inventory Management
add_new_product(20,"AC", "High-resolution display", 1000.0, 50)

# Task 6: Sales Reporting
generate_sales_report("2023-01-01", "2023-12-31")

# Task 7: Customer Account Updates
update_customer_account(1, "new@example.com", "9876543210")

# Task 9: Product Search and Recommendations
search_products("laptop")
