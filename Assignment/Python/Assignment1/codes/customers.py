
import mysql.connector

db_config = {
'user':"root", 'password':"venkat", 'database':"Techshop",'port':"3305",'auth_plugin':'mysql_native_password'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

class InvalidDataException(Exception):
    def __init__(self, message="Invalid data provided."):
        self.message = message
        super().__init__(self.message)

# Customers Class Queries
class Customers:
    def __init__(self,email):
        self._validate_email(email)  

    def _validate_email(self, email):
        # Custom email validation logic
        if "@" not in email or "." not in email:
            raise InvalidDataException("Invalid email address provided.")

    def calculate_total_orders(self, customer_id):
        query = """
            SELECT COUNT(OrderID) AS TotalOrders
            FROM Orders
            WHERE CustomerID = %s;
        """
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_customer_details(self, customer_id):
        query = """
            SELECT *
            FROM Customers
            WHERE CustomerID = %s;
        """
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        return result

    def update_customer_info(self, customer_id, email, phone, address):
        
        query = """
            UPDATE Customers
            SET Email = %s, Phone = %s, Address = %s
            WHERE CustomerID = %s;
        """
        cursor.execute(query, (email, phone, address, customer_id))
        conn.commit()

try:
    #to create a customer with an invalid email
    invalid_customer = Customers( "invalid-email")
except InvalidDataException as e:
    print(f"Error: {e}")


customer_handler = Customers('john@example.com')
total_orders = customer_handler.calculate_total_orders(1)
print("Total order:",total_orders)

customer_details = customer_handler.get_customer_details(1)
print("Customer detail",customer_details)

customer_handler.update_customer_info(1, 'newemail1@gmail.com', 'newphone101', 'newaddress101')
print('information updated')

# Commit the changes
conn.commit()
