from datetime import date
from dao.service.ICarLeaseRepositoryImpl import ICarLeaseRepositoryImpl
from entity.model.Customer import Customer
from entity.model.Vehicle import Vehicle

def print_menu():
    print("1. Add a Car")
    print("2. List Available Cars")
    print("3. Add a Customer")
    print("4. List Customers")
    print("5. Create a Lease")
    print("6. List Active Leases")
    print("7. Record Payment for a Lease")
    print("8. Return a Car")
    print("9. Exit")

def main():
    # Replace with your actual MySQL connection details
    connection_params = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "CarRentalSystem",
        "port" : "3300"
    }

    car_repository = ICarLeaseRepositoryImpl(connection_params)

    while True:
        print("\n--- Car Rental System Menu ---")
        print_menu()
        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            # Example: Adding a Car
            new_car = Vehicle(vehicleID=int(input("Enter Vehicle ID: ")),
                              make=input("Enter Make: "),
                              model=input("Enter Model: "),
                              year=int(input("Enter Year: ")),
                              dailyRate=float(input("Enter Daily Rate: ")),
                              status=input("Enter Status (available/notAvailable): "),
                              passengerCapacity=int(input("Enter Passenger Capacity: ")),
                              engineCapacity=int(input("Enter Engine Capacity: ")))

            car_repository.addCar(new_car)
            print("Car added successfully")

        elif choice == "2":
            # Example: Listing Available Cars
            available_cars = car_repository.listAvailableCars()
            print("Available Cars:")
            for car in available_cars:
                print(car)

        elif choice == "3":
            # Example: Adding a Customer
            new_customer = Customer(customerID=int(input("Enter Customer ID: ")),
                                    firstName=input("Enter First Name: "),
                                    lastName=input("Enter Last Name: "),
                                    email=input("Enter Email: "),
                                    phoneNumber=input("Enter Phone Number: "))

            car_repository.addCustomer(new_customer)
            print("Customer added successfully")

        elif choice == "4":
            # Example: Listing Customers
            customers = car_repository.listCustomers()
            print("Customers:")
            for customer in customers:
                print(customer)

        elif choice == "5":
            # Example: Creating a Lease
            start_date = date(2024, 2, 10)
            end_date = date(2024, 2, 20)
            new_lease = car_repository.createLease(customerID=int(input("Enter Customer ID: ")),
                                                   carID=int(input("Enter Car ID: ")),
                                                   startDate=start_date,
                                                   endDate=end_date)
            print("Lease created:", new_lease)

        elif choice == "6":
            # Example: Listing Active Leases
            active_leases = car_repository.listActiveLeases()
            print("Active Leases:")
            for lease in active_leases:
                print(lease)

        elif choice == "7":
            # Example: Recording Payment for a Lease
            lease_id = int(input("Enter Lease ID: "))
            payment_amount = float(input("Enter Payment Amount: "))
            car_repository.recordPayment(leaseID=lease_id, amount=payment_amount)
            print("Payment recorded successfully")

        elif choice == "8":
            # Example: Returning a Car
            lease_id = int(input("Enter Lease ID: "))
            returned_lease = car_repository.returnCar(leaseID=lease_id)
            print("Car returned. Updated Lease information:", returned_lease)

        elif choice == "9":
            # Exit the program
            print("Exiting Car Rental System. Goodbye!")
            car_repository.close_connection()
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()