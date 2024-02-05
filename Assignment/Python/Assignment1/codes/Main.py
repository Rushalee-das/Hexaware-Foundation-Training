from datetime import datetime

class Customers:
    def __init__(self, customer_id, first_name, last_name, email, phone, address):
        self.CustomerID = customer_id
        self.FirstName = first_name
        self.LastName = last_name
        self.Email = email
        self.Phone = phone
        self.Address = address
        self.Orders = []  # Assuming orders will be stored as a list

    def calculate_total_orders(self):
        return len(self.Orders)

    def get_customer_details(self):
        print("Customer ID:", self.CustomerID)
        print("Name:", self.FirstName, self.LastName)
        print("Email:", self.Email)
        print("Phone:", self.Phone)
        print("Address:", self.Address)
        print("Total Orders:", self.calculate_total_orders())

    def update_customer_info(self, new_email=None, new_phone=None, new_address=None):
        if new_email:
            self.Email = new_email
        if new_phone:
            self.Phone = new_phone
        if new_address:
            self.Address = new_address
        print("Customer information updated successfully.")

class Products:
    def __init__(self, product_id, product_name, description, price):
        self.ProductID = product_id
        self.ProductName = product_name
        self.Description = description
        self.Price = price

    def get_product_details(self):
        print("Product ID:", self.ProductID)
        print("Product Name:", self.ProductName)
        print("Description:", self.Description)
        print("Price: $%.2f" % self.Price)

    def update_product_info(self, new_price=None, new_description=None):
        if new_price is not None:
            self.Price = new_price
        if new_description:
            self.Description = new_description
        print("Product information updated successfully.")

class Orders:
    def __init__(self, order_id, customer, order_date, total_amount):
        self.OrderID = order_id
        self.Customer = customer
        self.OrderDate = order_date
        self.TotalAmount = total_amount
        self.OrderStatus = "Pending"  # Default status
        self.OrderDetails = []  # Assuming order details will be stored as a list

    def calculate_total_amount(self):
        return sum(detail.calculate_subtotal() for detail in self.OrderDetails)

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
        self.update_order_status("Cancelled")
        print("Order cancelled.")

class OrderDetails:
    def __init__(self, order_detail_id, order, product, quantity):
        self.OrderDetailID = order_detail_id
        self.Order = order
        self.Product = product
        self.Quantity = quantity
        self.Discount = 0.0

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

class Inventory:
    def __init__(self, inventory_id, product, quantity_in_stock, last_stock_update):
        self.InventoryID = inventory_id
        self.Product = product
        self.QuantityInStock = quantity_in_stock
        self.LastStockUpdate = last_stock_update

    def get_product(self):
        return self.Product

    def get_quantity_in_stock(self):
        return self.QuantityInStock

    def add_to_inventory(self, quantity):
        self.QuantityInStock += quantity
        self.LastStockUpdate = datetime.now()
        print(quantity, self.Product.ProductName + "(s) added to the inventory.")

    def remove_from_inventory(self, quantity):
        if self.QuantityInStock >= quantity:
            self.QuantityInStock -= quantity
            self.LastStockUpdate = datetime.now()
            print(quantity, self.Product.ProductName + "(s) removed from the inventory.")
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
            print(self.Product.ProductName + " is low in stock with", self.QuantityInStock, "units.")

    def list_out_of_stock_products(self):
        if self.QuantityInStock == 0:
            print(self.Product.ProductName + " is out of stock.")

    def list_all_products(self):
        print("Product:", self.Product.ProductName + ",", "Quantity:", self.QuantityInStock)

# Example usage:
customer1 = Customers(1, "John", "Doe", "john.doe@example.com", "123-456-7890", "123 Main St")
product1 = Products(1, "Laptop", "High-performance laptop", 999.99)
order_date = datetime.now()
order1 = Orders(1, customer1, order_date, 0.0)
order_detail1 = OrderDetails(1, order1, product1, 2)
inventory_item1 = Inventory(1, product1, 10, datetime.now())


