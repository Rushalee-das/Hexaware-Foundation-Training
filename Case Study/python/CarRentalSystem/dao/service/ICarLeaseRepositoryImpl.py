import mysql.connector
from mysql.connector import Error

from dao.service.ICarLeaseRepository import ICarLeaseRepository
from entity.model.Lease import Lease


class ICarLeaseRepositoryImpl(ICarLeaseRepository):
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(**self.connection_params)
            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Connection closed")


    def addCar(self, car):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO vehicle (vehicleID, make, model, year, dailyRate, status, passengerCapacity, engineCapacity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (car.vehicleID, car.make, car.model, car.year, car.dailyRate, car.status, car.passengerCapacity, car.engineCapacity)
            cursor.execute(query, values)
            self.connection.commit()
            print("Car added successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def removeCar(self, carID) :
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM vehicle WHERE vehicleID = %s"
            values = (carID,)
            cursor.execute(query, values)
            self.connection.commit()
            print("Car removed successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def listAvailableCars(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM vehicle WHERE status = 'available'"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def listRentedCars(self) :
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM vehicle WHERE status = 'notAvailable'"
            cursor.execute(query)
            result = cursor.fetchall()

            return result
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def findCarById(self, carID):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM vehicle WHERE vehicleID = %s"
            values = (carID,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise Exception(f"Car with ID {carID} not found")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def addCustomer(self, customer):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO customer (customerID, firstName, lastName, email, phoneNumber) VALUES (%s, %s, %s, %s, %s)"
            values = (customer.customerID, customer.firstName, customer.lastName, customer.email, customer.phoneNumber)
            cursor.execute(query, values)
            self.connection.commit()
            print("Customer added successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def removeCustomer(self, customerID: int) :
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM customer WHERE customerID = %s"
            values = (customerID,)
            cursor.execute(query, values)
            self.connection.commit()
            print("Customer removed successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def listCustomers(self) :
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM customer"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def findCustomerById(self, customerID: int):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM customer WHERE customerID = %s"
            values = (customerID,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise Exception(f"Customer with ID {customerID} not found")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def createLease(self, customerID: int, carID: int, startDate, endDate):
        try:
            cursor = self.connection.cursor()

            # Fetch the current maximum leaseID from the database
            cursor.execute("SELECT MAX(leaseID) FROM lease")
            max_lease_id = cursor.fetchone()[0]

            # Increment the max_lease_id by 1 to get the new leaseID
            new_lease_id = max_lease_id + 1 if max_lease_id is not None else 1

            # Insert the new lease record with the calculated leaseID
            query = "INSERT INTO lease (leaseID, vehicleID, customerID, startDate, endDate) VALUES (%s, %s, %s, %s, %s)"
            values = (new_lease_id, carID, customerID, startDate, endDate)
            cursor.execute(query, values)
            self.connection.commit()

            # Return the Lease object with the calculated leaseID
            return Lease(new_lease_id, carID, customerID, startDate, endDate)

        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def returnCar(self, leaseID: int):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE lease SET endDate = CURRENT_DATE WHERE leaseID = %s"
            values = (leaseID,)
            cursor.execute(query, values)
            self.connection.commit()

            # Fetch the updated lease information
            query_select = "SELECT * FROM lease WHERE leaseID = %s"
            cursor.execute(query_select, values)
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise Exception(f"Lease with ID {leaseID} not found")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def listActiveLeases(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM lease WHERE endDate >= CURRENT_DATE"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def listLeaseHistory(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM lease WHERE endDate < CURRENT_DATE"
            cursor.execute(query)
            result = cursor.fetchall()

            return result
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def recordPayment(self, leaseID: int, amount: float):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO payment (leaseID, paymentDate, amount) VALUES (%s, CURRENT_DATE, %s)"
            values = (leaseID, amount)
            cursor.execute(query, values)
            self.connection.commit()
            print("Payment recorded successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()