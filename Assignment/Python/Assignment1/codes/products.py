'''
class Products:
    def __init__(self, product_id, product_name, description, price):
        self.ProductID = product_id
        self.ProductName = product_name
        self.Description = description
        self.Price = price

    def get_product_details(self):
        pass
        #Retrieves and displays detailed information about the product
    def update_product_info(self, new_price=None, new_description=None):
        pass
        #Allows updates to product details (e.g., price, description).
    def is_product_in_stock(self):
        pass
        #Checks if the product is currently in stock
'''
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

class DuplicateProductException(Exception):
    def __init__(self, message="Duplicate product found."):
        self.message = message
        super().__init__(self.message)


class Products:
    def get_product_details(self, product_id):
        query = """
            SELECT *
            FROM Products
            WHERE ProductID = %s;
        """
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        return result

    def update_product_info(self, product_id, price, description):
        query = """
            UPDATE Products
            SET Price = %s, Description = %s
            WHERE ProductID = %s;
        """
        cursor.execute(query, (price, description, product_id))
        conn.commit()

    def is_product_in_stock(self, product_id):
        query = """
            SELECT QuantityInStock
            FROM Inventory
            WHERE ProductID = %s;
        """
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def search_products(self, search_criteria):
        try:
            query = """
                SELECT *
                FROM Products
                WHERE Category LIKE %s ;
            """
            cursor.execute(query, (f"%{search_criteria}%",))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error: {e}")

    def add_product(self, product):
        try:
            # Check for duplicate products based on name or SKU
            if any(p['ProductName'].lower() == product['ProductName'].lower() or
                   p['SKU'].lower() == product['SKU'].lower() for p in self.products):
                raise DuplicateProductException()

            self.products.append(product)
            print("Product added successfully.")
        except DuplicateProductException as e:
            print(f"Error: {e}")







product_handler = Products()
product_details = product_handler.get_product_details(1)
print(product_details)
product_handler.update_product_info(1, 1199.99, 'Updated new description')
print('updated')
stock_status = product_handler.is_product_in_stock(1)
print(stock_status)

# Search for products with a specific criteria
search_result = product_handler.search_products("Electronic Gadget")

# Display search results
for product in search_result:
    print(product)

conn.commit()

# Close the database connection
cursor.close()
conn.close()