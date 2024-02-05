from datetime import datetime
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

from datetime import datetime
class InvalidDataException(Exception):
    def __init__(self, message="Invalid data provided."):
        self.message = message
        super().__init__(self.message)

class InsufficientStockException(Exception):
    def __init__(self, message="Insufficient stock."):
        self.message = message
        super().__init__(self.message)


class Orders:
    def __init__(self, order_id, customer_id, order_date, total_amount, status='Pending'):
        self.OrderID = order_id
        self.CustomerID = customer_id
        self.OrderDate = order_date
        self.TotalAmount = total_amount
        self.Status = status

    def calculate_total_amount(self):
        query = """
            SELECT SUM(TotalAmount) AS TotalAmount
            FROM Orders
            WHERE CustomerID = %s;
        """
        cursor.execute(query, (self.CustomerID,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_order_details(self):
        query = """
            SELECT *
            FROM OrderDetails
            WHERE OrderID = %s;
        """
        cursor.execute(query, (self.OrderID,))
        result = cursor.fetchall()
        return result

    def update_order_status(self, new_status):
        try:
            self._validate_order_status(new_status)
            query = """
                UPDATE Orders
                SET Status = %s
                WHERE OrderID = %s;
            """
            cursor.execute(query, (new_status, self.OrderID))
            conn.commit()
            print(f"Order {self.OrderID} status updated to {new_status}.")
        except InvalidDataException as e:
            print(f"Error: {e}")

    def cancel_order(self):
        query = """
            DELETE FROM Orders
            WHERE OrderID = %s;
        """
        cursor.execute(query, (self.OrderID,))
        conn.commit()
        print(f"Order {self.OrderID} canceled.")

    def add_new_order(self, product_id, quantity):
        try:
            # Check if the product is available in inventory
            if not self._is_product_available(product_id, quantity):
                raise InvalidDataException("Product not available in sufficient quantity.")

            # Insert new order
            oi=self.CustomerID
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query_insert_order = """
                INSERT INTO Orders (orderid,CustomerID, OrderDate, TotalAmount)
                VALUES (%s,%s, %s, %s);
            """
            cursor.execute(query_insert_order, (oi,self.CustomerID, order_date, 0))
            conn.commit()

            # Get the newly created order ID
            query_get_new_order_id = "SELECT LAST_INSERT_ID();"
            cursor.execute(query_get_new_order_id)
            new_order_id = cursor.fetchone()[0]

            # Insert order details
            query_insert_order_details = """
                INSERT INTO OrderDetails (OrderID, ProductID, Quantity)
                VALUES (%s, %s, %s);
            """
            cursor.execute(query_insert_order_details, (new_order_id, product_id, quantity))
            conn.commit()

            print(f"New order {new_order_id} added successfully.")
        except InvalidDataException as e:
            print(f"Error: {e}")

    def _validate_order_status(self, status):
        valid_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Canceled']
        if status not in valid_statuses:
            raise InvalidDataException("Invalid order status provided.")

    def _is_product_available(self, product_id, quantity):
        query = """
            SELECT CASE WHEN QuantityInStock >= %s THEN 1 ELSE 0 END AS IsAvailable
            FROM Inventory
            WHERE ProductID = %s;
        """
        cursor.execute(query, (quantity, product_id))
        result = cursor.fetchone()
        return result[0] if result else None
    
    #collections:handling inventory management
    def process_order(self):
        try:
            # Get order details
            order_details = self.get_order_details()

            # Update inventory quantities and calculate total amount
            total_amount = 0
            for order_detail in order_details:
                product_id = order_detail['ProductID']
                quantity = order_detail['Quantity']

                # Check if the product is available in inventory
                if not self._is_product_available(product_id, quantity):
                    raise InsufficientStockException(f"Insufficient stock for product {product_id}.")

                # Update inventory quantity
                self._update_inventory(product_id, quantity)

                # Calculate total amount for the order
                product_price = order_detail['Price']
                total_amount += quantity * product_price

            # Update total amount in the Orders table
            query_update_total_amount = """
                UPDATE Orders
                SET TotalAmount = %s
                WHERE OrderID = %s;
            """
            cursor.execute(query_update_total_amount, (total_amount, self.OrderID))
            conn.commit()

            print(f"Order {self.OrderID} processed successfully. Total Amount: {total_amount}")
        except InsufficientStockException as e:
            print(f"Error: {e}")
            # Optionally, you can cancel the order or take other actions based on business logic

    def _update_inventory(self, product_id, quantity):
        query_update_inventory = """
            UPDATE Inventory
            SET QuantityInStock = QuantityInStock - %s
            WHERE ProductID = %s;
        """
        cursor.execute(query_update_inventory, (quantity, product_id))
        conn.commit()

order_handler = Orders(101, 1, datetime.now(), 0)

# Add a new order
order_handler.add_new_order(product_id=11, quantity=3)

# Get order details
order_details = order_handler.get_order_details()

# Update order status
order_handler.update_order_status(new_status='Shipped')

# Cancel order
order_handler.cancel_order()
print('Order Cancelled')

order_handler.process_order()
print('Order Processed')
conn.commit()

cursor.close()
conn.close()

