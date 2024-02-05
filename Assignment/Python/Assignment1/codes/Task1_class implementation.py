'''
class Customers:
    def __init__(self, customer_id, first_name, last_name, email, phone, address):
        self.CustomerID = customer_id
        self.FirstName = first_name
        self.LastName = last_name
        self.Email = email
        self.Phone = phone
        self.Address = address
        self.orders = []  # Assuming orders will be stored as a list

    def calculate_total_orders(self):
        return len(self.orders)

    def get_customer_details(self):
        print(f"Customer ID: {self.CustomerID}")
        print(f"Name: {self.FirstName} {self.LastName}")
        print(f"Email: {self.Email}")
        print(f"Phone: {self.Phone}")
        print(f"Address: {self.Address}")
        print(f"Total Orders: {self.calculate_total_orders()}")

    def update_customer_info(self, new_email=None, new_phone=None, new_address=None):
        if new_email:
            self.Email = new_email
        if new_phone:
            self.Phone = new_phone
        if new_address:
            self.Address = new_address
        print("Customer information updated successfully.")

# Example usage:
customer1 = Customers(1, "John", "Doe", "john.doe@example.com", "123-456-7890", "123 Main St")
customer1.orders = [1, 2, 3]  # Assuming order IDs are stored as integers

customer1.get_customer_details()

customer1.update_customer_info(new_email="john.new@example.com", new_phone="987-654-3210")

customer1.get_customer_details()

class Product:
    def __init__(self, product_id, product_name, description, price, in_stock):
        self.ProductID = product_id
        self.ProductName = product_name
        self.Description = description
        self.Price = price
        self.InStock = in_stock

    def get_product_details(self):
        print("Product ID:", self.ProductID)
        print("Product Name:", self.ProductName)
        print("Description:", self.Description)
        print("Price: $%.2f" % self.Price)
        print("In Stock: Yes" if self.InStock else "In Stock: No")

    def update_product_info(self, new_price=None, new_description=None, new_stock_status=None):
        if new_price is not None:
            self.Price = new_price
        if new_description:
            self.Description = new_description
        if new_stock_status is not None:
            self.InStock = new_stock_status
        print("Product information updated successfully.")

    def is_product_in_stock(self):
        return self.InStock

# Example usage:
product1 = Product(1, "Laptop", "High-performance laptop", 999.99, True)

product1.get_product_details()

product1.update_product_info(new_price=1099.99, new_description="Ultra-slim laptop", new_stock_status=False)

product1.get_product_details()

print("Is Product in Stock?", product1.is_product_in_stock())


from datetime import datetime

class Orders:
    def __init__(self, order_id, customer, order_date, total_amount):
        self.OrderID = order_id
        self.Customer = customer  # Composition: referencing the Customer class
        self.OrderDate = order_date
        self.TotalAmount = total_amount
        self.OrderStatus = "Pending"  # Default status

    def calculate_total_amount(self):
        # You might want to implement this method based on the actual products and quantities in the order
        # For simplicity, we assume the total amount is already provided during order creation.
        return self.TotalAmount

    def get_order_details(self):
        print("Order ID:", self.OrderID)
        print("Customer:", self.Customer.FirstName, self.Customer.LastName)
        print("Order Date:", self.OrderDate.strftime("%Y-%m-%d %H:%M:%S"))
        print("Total Amount: $%.2f" % self.calculate_total_amount())
        print("Order Status:", self.OrderStatus)

    def update_order_status(self, new_status):
        self.OrderStatus = new_status
        print("Order status updated successfully.")

    def cancel_order(self):
        # You might want to implement this method to adjust stock levels and perform other cancellation tasks
        # For now, we'll just update the order status
        self.update_order_status("Cancelled")
        print("Order cancelled.")

# Example usage:
customer1 = Customers(1, "John", "Doe", "john.doe@example.com", "123-456-7890", "123 Main St")
order_date = datetime.now()
order1 = Orders(1, customer1, order_date, 1500.00)

order1.get_order_details()

order1.update_order_status("Processing")

order1.get_order_details()

order1.cancel_order()


class OrderDetails:
    def __init__(self, order_detail_id, order, product, quantity):
        self.OrderDetailID = order_detail_id
        self.Order = order  # Composition: referencing the Order class
        self.Product = product  # Composition: referencing the Product class
        self.Quantity = quantity
        self.Discount = 0.0  # Default discount

    def calculate_subtotal(self):
        return (self.Product.Price - self.Discount) * self.Quantity

    def get_order_detail_info(self):
        print("Order Detail ID:", self.OrderDetailID)
        print("Product:", self.Product.ProductName)
        print("Quantity:", self.Quantity)
        print("Subtotal: $%.2f" % self.calculate_subtotal())

    def update_quantity(self, new_quantity):
        self.Quantity = new_quantity
        print("Quantity updated successfully.")

    def add_discount(self, discount_amount):
        self.Discount += discount_amount
        print("Discount applied successfully.")

# Example usage:
product1 = Product(1, "Laptop", "High-performance laptop", 999.99, True)
order1 = Orders(1, customer1, order_date, 0.0)  # Assume total amount is initially 0.0
order_detail1 = OrderDetails(1, order1, product1, 2)

order_detail1.get_order_detail_info()

order_detail1.update_quantity(3)

order_detail1.get_order_detail_info()

order_detail1.add_discount(50.0)

order_detail1.get_order_detail_info()


from datetime import datetime

class Inventory:
    def __init__(self, inventory_id, product, quantity_in_stock, last_stock_update):
        self.InventoryID = inventory_id
        self.Product = product  # Composition: referencing the Product class
        self.QuantityInStock = quantity_in_stock
        self.LastStockUpdate = last_stock_update

    def get_product(self):
        return self.Product

    def get_quantity_in_stock(self):
        return self.QuantityInStock

    def add_to_inventory(self, quantity):
        self.QuantityInStock += quantity
        self.LastStockUpdate = datetime.now()
        print(f"{quantity} {self.Product.ProductName}(s) added to the inventory.")

    def remove_from_inventory(self, quantity):
        if self.QuantityInStock >= quantity:
            self.QuantityInStock -= quantity
            self.LastStockUpdate = datetime.now()
            print(f"{quantity} {self.Product.ProductName}(s) removed from the inventory.")
        else:
            print("Insufficient quantity in stock.")

    def update_stock_quantity(self, new_quantity):
        self.QuantityInStock = new_quantity
        self.LastStockUpdate = datetime.now()
        print("Stock quantity updated successfully.")

    def is_product_available(self, quantity_to_check):
        return self.QuantityInStock >= quantity_to_check

    def get_inventory_value(self):
        return self.Product.Price * self.QuantityInStock

    def list_low_stock_products(self, threshold):
        if self.QuantityInStock < threshold:
            print(f"{self.Product.ProductName} is low in stock with {self.QuantityInStock} units.")

    def list_out_of_stock_products(self):
        if self.QuantityInStock == 0:
            print(f"{self.Product.ProductName} is out of stock.")

    def list_all_products(self):
        print(f"Product: {self.Product.ProductName}, Quantity: {self.QuantityInStock}")

# Example usage:
product1 = Product(1, "Laptop", "High-performance laptop", 999.99, True)
inventory_item1 = Inventory(1, product1, 10, datetime.now())

print("Initial Inventory:")
inventory_item1.list_all_products()

inventory_item1.add_to_inventory(5)

inventory_item1.list_all_products()

inventory_item1.remove_from_inventory(3)

inventory_item1.list_all_products()

inventory_item1.update_stock_quantity(15)

inventory_item1.list_all_products()

print("Is Laptop Available? ", inventory_item1.is_product_available(7))

print("Inventory Value:", inventory_item1.get_inventory_value())

inventory_item1.list_low_stock_products(12)

inventory_item1.list_out_of_stock_products()
'''
from datetime import datetime

# Define custom exceptions
class InvalidDataException(Exception):
    pass

class InsufficientStockException(Exception):
    pass

class IncompleteOrderException(Exception):
    pass

class PaymentFailedException(Exception):
    pass

class FileIOException(Exception):
    pass

class DatabaseAccessException(Exception):
    pass

class ConcurrencyException(Exception):
    pass

class AuthenticationException(Exception):
    pass

class AuthorizationException(Exception):
    pass

class Customers:
    def __init__(self, customer_id, first_name, last_name, email, phone, address):
        self._customer_id = customer_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._phone = phone
        self._address = address
        self._orders = []  # Assuming orders will be stored as a list

    def calculate_total_orders(self):
        return len(self._orders)

    def get_customer_details(self):
        print("Customer ID:", self._customer_id)
        print("Name:", self._first_name, self._last_name)
        print("Email:", self._email)
        print("Phone:", self._phone)
        print("Address:", self._address)
        print("Total Orders:", self.calculate_total_orders())

    def update_customer_info(self, new_email=None, new_phone=None, new_address=None):
        if new_email:
            self._email = new_email
        if new_phone:
            self._phone = new_phone
        if new_address:
            self._address = new_address
        print("Customer information updated successfully.")

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    @property
    def address(self):
        return self._address

    @property
    def orders(self):
        return self._orders


class Products:
    def __init__(self, product_id, product_name, description, price):
        self._product_id = product_id
        self._product_name = product_name
        self._description = description
        self._price = 0.0  
        self.price = price  
    
    

    def get_product_details(self):
        print("Product ID:", self._product_id)
        print("Product Name:", self._product_name)
        print("Description:", self._description)
        print("Price: $%.2f" % self._price)

    def update_product_info(self, new_price=None, new_description=None):
        if new_price is not None:
            self._price = new_price
        if new_description:
            self._description = new_description
        print("Product information updated successfully.")

    @property
    def product_id(self):
        return self._product_id

    @property
    def product_name(self):
        return self._product_name

    @property
    def description(self):
        return self._description

    @property
    def price(self):
        return self._price


class Orders:
    def __init__(self, order_id, customer, order_date, total_amount):
        self._order_id = order_id
        self._customer = customer  # Composition relationship with Customers class
        self._order_date = order_date
        self._total_amount = total_amount
        self._order_status = "Pending"
        self._order_details = []  # Assuming order details will be stored as a list

    def calculate_total_amount(self):
        return sum(detail.calculate_subtotal() for detail in self._order_details)

    def get_order_details(self):
        print("Order ID:", self._order_id)
        print("Customer:", self._customer.first_name, self._customer.last_name)
        print("Order Date:", self._order_date.strftime("%Y-%m-%d %H:%M:%S"))
        print("Total Amount: $%.2f" % self.calculate_total_amount())
        print("Order Status:", self._order_status)

    def update_order_status(self, new_status):
        self._order_status = new_status
        print("Order status updated successfully.")

    def cancel_order(self):
        self.update_order_status("Cancelled")
        print("Order cancelled.")

    def process_order(self):
        try:
            self.validate_order()
            self.update_inventory()
            self.process_payment()
            print("Order processed successfully.")
        except (InvalidDataException, InsufficientStockException, IncompleteOrderException,
                PaymentFailedException, Exception) as e:
            print(f"Error processing order: {e}")

    def validate_order(self):
        # Validation logic for order details
        if not self._order_details:
            raise IncompleteOrderException("Order is incomplete. No order details found.")
        for detail in self._order_details:
            if not detail.product:
                raise IncompleteOrderException("Order is incomplete. Product reference missing.")
    
    def update_inventory(self):
        # Inventory management logic
        for detail in self._order_details:
            if detail.quantity > detail.product.quantity_in_stock:
                raise InsufficientStockException("Insufficient stock for product: "
                                                 f"{detail.product.product_name}")

    def process_payment(self):
        # Payment processing logic
        try:
            # Simulate payment processing
            payment_result = self.simulate_payment_processing()

            if payment_result == "success":
                print("Payment successful.")
            else:
                raise PaymentFailedException("Payment declined.")
        except PaymentFailedException as e:
            # Retry or cancel order
            raise e
    def simulate_payment_processing(self):
        
        import random
        if random.random() < 0.8:
            return "success"
        else:
            return "failure"

    @property
    def order_id(self):
        return self._order_id

    @property
    def customer(self):
        return self._customer

    @property
    def order_date(self):
        return self._order_date

    @property
    def total_amount(self):
        return self._total_amount

    @property
    def order_status(self):
        return self._order_status

    @property
    def order_details(self):
        return self._order_details


class OrderDetails:
    def __init__(self, order_detail_id, order, product, quantity):
        self._order_detail_id = order_detail_id
        self._order = order  # Composition relationship with Orders class
        self._product = product  # Composition relationship with Products class
        self._quantity = quantity
        self._discount = 0.0

    def calculate_subtotal(self):
        return (self._product.price - self._discount) * self._quantity

    def get_order_detail_info(self):
        print("Order Detail ID:", self._order_detail_id)
        print("Product:", self._product.product_name)
        print("Quantity:", self._quantity)
        print("Subtotal: $%.2f" % self.calculate_subtotal())

    def update_quantity(self, new_quantity):
        self._quantity = new_quantity
        print("Quantity updated successfully.")

    def add_discount(self, discount_amount):
        self._discount += discount_amount
        print("Discount applied successfully.")

    @property
    def order_detail_id(self):
        return self._order_detail_id

    @property
    def order(self):
        return self._order

    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity

    @property
    def discount(self):
        return self._discount


class Inventory:
    def __init__(self, inventory_id, product, quantity_in_stock, last_stock_update):
        self._inventory_id = inventory_id
        self._product = product
        self._quantity_in_stock = 0  # Default to 0 to ensure positivity
        self.quantity_in_stock = quantity_in_stock  # Use the setter to apply validation
        self._last_stock_update = last_stock_update

    @property
    def inventory_id(self):
        return self._inventory_id

    @property
    def product(self):
        return self._product

    @property
    def quantity_in_stock(self):
        return self._quantity_in_stock

    @quantity_in_stock.setter
    def quantity_in_stock(self, new_quantity):
        if not isinstance(new_quantity, int):
            raise ValueError("Quantity must be an integer.")
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity_in_stock = new_quantity

    @property
    def last_stock_update(self):
        return self._last_stock_update

