from dao.service.IHospitalService import IHospitalService
import mysql.connector


from dao.service.IHospitalService import IHospitalService
from util.DBConnection import DBConnection

class HospitalServiceImpl(IHospitalService):
    def __init__(self, database_con):
        self.database_con = database_con

    def generate_appointment_id(self):
        connection = self.database_con

        cur = connection.cursor()
        cur.execute("SELECT MAX(AppointmentID) FROM Appointment")
        AppointmentID = cur.fetchone()[0]
        if AppointmentID is None:
            AppointmentID = 1
        else:
            AppointmentID += 1
        return AppointmentID

    # Other methods remain unchanged

    def get_appointment_by_id(self, appointment_id):
        connection = self.database_con.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Appointments WHERE appointmentId = %s", (appointment_id,))
                appointment_data = cursor.fetchone()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return None
            return appointment_data

    def get_appointments_for_patient(self, patient_id):
        connection = self.database_con.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Appointments WHERE patientID = %s", (patient_id,))
                appointment_data = cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return None
            return appointment_data

    def get_appointments_for_doctor(self, doctor_id):
        connection = self.database_con.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Appointments WHERE doctorID = %s", (doctor_id,))
                appointment_data = cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return None
            return appointment_data

    def schedule_appointment(self, appointment):
        connection = self.database_con.get_connection()
        appointment_id = self.generate_appointment_id()
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Appointment VALUES (%s,%s,%s,%s,%s)",
                           (appointment_id, appointment['patientId'], appointment['doctorId'],
                            appointment['appointmentDate'], appointment['description'],))
            connection.commit()
        except Exception as e:
            print(e)

    def update_appointment(self, appointment):
        appointment_id = appointment.get('AppointmentID')
        patientId = appointment.get('patientId')
        doctorId = appointment.get('doctorId')
        appointmentDate = appointment.get('appointmentDate')
        description = appointment.get('description')

        connection = self.database_con.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute('''
                        UPDATE Appointment
                        SET patientId = %s,
                            doctorId = %s,
                            appointmentDate = %s,
                            description = %s  
                        WHERE appointmentID = %s
                        ''',
                           (patientId, doctorId, appointmentDate, description, appointment_id))
            connection.commit()
        except Exception as e:
            print(e)

    def cancel_appointment(self, appointment_id):
        connection = self.database_con.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Appointment WHERE appointmentID = %s", (appointment_id,))
            connection.commit()
        except Exception as e:
            print(e)
