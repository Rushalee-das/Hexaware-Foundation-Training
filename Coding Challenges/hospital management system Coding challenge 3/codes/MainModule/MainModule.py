from dao.service.IHospitalService import IHospitalService
from dao.service.HospitalServiceImpl import HospitalServiceImpl
from util.DBConnection import DBConnection
from util.PropertyUtil import PropertyUtil
import mysql.connector

def main():
    # Set up database connection details
    connection_details = {
        'host': 'localhost',
        'user': 'root',
        'passwd': 'root',
        'port': '3300',
        'dbname': 'HospitalManagementSystem'
    }

    # Initialize the database connection
    db_connection = mysql.connector.connect(**connection_details)

    # Create an instance of the Hospital Service
    hospital_service = HospitalServiceImpl(db_connection)

    # Example usage:
    # 1. Generate an appointment ID
    appointment_id = hospital_service.generate_appointment_id()
    print(f"Generated Appointment ID: {appointment_id}")

    # 2. Schedule an appointment
    appointment_data = {
        'patientId': 1,
        'doctorId': 1,
        'appointmentDate': '2024-03-10',
        'description': 'Regular checkup'
    }
    hospital_service.schedule_appointment(appointment_data)
    print("Appointment scheduled successfully!")

    # 3. Get appointment by ID
    appointment_id_to_retrieve = 1  # Replace with an actual appointment ID
    appointment_details = hospital_service.get_appointment_by_id(appointment_id_to_retrieve)
    print("Appointment Details:")
    print(appointment_details)

    # 4. Update appointment
    appointment_to_update = {
        'AppointmentID': appointment_id_to_retrieve,
        'patientId': 2,
        'doctorId': 1,
        'appointmentDate': '2024-02-15',
        'description': 'Follow-up'
    }
    hospital_service.update_appointment(appointment_to_update)
    print("Appointment updated successfully!")

    # 5. Cancel appointment
    appointment_id_to_cancel = 2  # Replace with an actual appointment ID
    hospital_service.cancel_appointment(appointment_id_to_cancel)
    print("Appointment canceled successfully!")

if __name__ == "__main__":
    main()