import mysql.connector
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "techshop"
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
# OrderDetails Class Queries
class OrderDetails:
    def calculate_subtotal(self, order_detail_id):
        query = """
            SELECT Quantity * Price AS Subtotal
            FROM OrderDetails
            JOIN Products ON OrderDetails.ProductID = Products.ProductID
            WHERE OrderDetailID = %s;
        """
        cursor.execute(query, (order_detail_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_order_detail_info(self, order_detail_id):
        query ="""
            SELECT *
            FROM OrderDetails od
            LEFT JOIN orders o ON o.orderid = od.orderid
            LEFT JOIN customers c ON c.customerid = o.customerid
            WHERE od.OrderdetailID = %s;
        """
        cursor.execute(query, (order_detail_id,))
        result = cursor.fetchone()
        return result

    def update_quantity(self, order_detail_id, quantity):
        query = """
            UPDATE OrderDetails
            SET Quantity = %s
            WHERE OrderDetailID = %s;
        """
        cursor.execute(query, (quantity, order_detail_id))
        conn.commit()

    def add_discount(self, order_detail_id, discount):
        query = """
            UPDATE Orders o
            LEFT JOIN orderdetails od ON od.orderid=o.orderid
            SET TotalAmount = %s
            WHERE OrderDetailID = %s;
        """
        cursor.execute(query, (discount, order_detail_id))
        conn.commit()

order_details_handler = OrderDetails()
subtotal_amount = order_details_handler.calculate_subtotal(3)
print(subtotal_amount)

order_detail_info = order_details_handler.get_order_detail_info(3)
print(order_detail_info)

order_details_handler.update_quantity(1, 5)
print('updated')

order_details_handler.add_discount(1, 10)
print('Information updated')

conn.commit()

