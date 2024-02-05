import datetime
import mysql.connector

db_config = {
'user':"root", 'password':"venkat", 'database':"Techshop",'port':"3305",'auth_plugin':'mysql_native_password'
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
# Inventory Class Queries
class Inventory:
    def get_product(self, product_id):
        query = """
            SELECT *
            FROM Products
            WHERE ProductID = %s;
        """
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        return result

    def get_quantity_in_stock(self, product_id):
        query = """
            SELECT QuantityInStock
            FROM Inventory
            WHERE ProductID = %s;
        """
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def add_to_inventory(self, product_id, quantity):
        query = """
            UPDATE Inventory
            SET QuantityInStock = QuantityInStock + %s
            WHERE ProductID = %s;
        """
        cursor.execute(query, (quantity, product_id))
        conn.commit()

    def remove_from_inventory(self, product_id, quantity):
        query = """
            UPDATE Inventory
            SET QuantityInStock = QuantityInStock - %s
            WHERE ProductID = %s;
        """
        cursor.execute(query, (quantity, product_id))
        conn.commit()

    def update_stock_quantity(self, product_id, new_quantity):
        query = """
            UPDATE Inventory
            SET QuantityInStock = %s
            WHERE ProductID = %s;
        """
        cursor.execute(query, (new_quantity, product_id))
        conn.commit()

    def is_product_available(self, product_id, quantity_to_check):
        query = """
            SELECT CASE WHEN QuantityInStock >= %s THEN 1 ELSE 0 END AS IsAvailable
            FROM Inventory
            WHERE ProductID = %s;
        """
        cursor.execute(query, (quantity_to_check, product_id))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_inventory_value(self):
        query = """
            SELECT SUM(QuantityInStock * Price) AS InventoryValue
            FROM Inventory
            JOIN Products ON Inventory.ProductID = Products.ProductID;
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None

    def list_low_stock_products(self, threshold):
        query = """
            SELECT *
            FROM Inventory
            JOIN Products ON Inventory.ProductID = Products.ProductID
            WHERE QuantityInStock < %s;
        """
        cursor.execute(query, (threshold,))
        result = cursor.fetchall()
        return result

    def list_out_of_stock_products(self):
        query = """
            SELECT *
            FROM Inventory
            JOIN Products ON Inventory.ProductID = Products.ProductID
            WHERE QuantityInStock = 0;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def list_all_products(self):
        query = """
            SELECT *
            FROM Inventory
            JOIN Products ON Inventory.ProductID = Products.ProductID;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

inventory_handler = Inventory()

product_info = inventory_handler.get_product(1)
print(product_info)
quantity_in_stock = inventory_handler.get_quantity_in_stock(1)
print(quantity_in_stock)
inventory_handler.add_to_inventory(1, 10)
print('added to inventory')
inventory_handler.remove_from_inventory(1, 5)
print('removed from inventory')
inventory_handler.update_stock_quantity(1, 20)
print('updated')
availability_status = inventory_handler.is_product_available(1, 15)
print(availability_status)
inventory_value = inventory_handler.get_inventory_value()
print(inventory_value)
low_stock_products = inventory_handler.list_low_stock_products(10)
print(low_stock_products)
out_of_stock_products = inventory_handler.list_out_of_stock_products()
print(out_of_stock_products)
all_products = inventory_handler.list_all_products()
print(all_products)

conn.commit()

# Close the database connection
cursor.close()
conn.close()



