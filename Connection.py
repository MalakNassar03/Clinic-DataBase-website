#1200757 Malak Nassar
#1201107 Tala Flaifel
#1200277 Mona Dweikat
from flask import Flask, render_template, request, redirect, url_for,flash,jsonify,session,abort
import pymysql
import mysql.connector
from mysql.connector import IntegrityError
from datetime import timedelta,date
import json




app = Flask(__name__)
app.secret_key = 'secret'

# MySQL connection setup
conn = mysql.connector.connect(host='localhost', username='root', password='0267', database='clinic',
                               connect_timeout=120
                               )

def format_timedelta(td):
    # Format timedelta as HH:MM:SS
    seconds = td.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
# MySQL connection setup
conn = mysql.connector.connect(host='localhost', username='root', password='0267', database='clinic',
                               connect_timeout=120
                               )
my_cursor = conn.cursor()


# ********************************************************************

def get_patient_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM patient")
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []

    # ********************************************************************

def get_appointment_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM appointment")
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    # ********************************************************************
def get_equipment_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM equipment")
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_staff_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM staff")
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_expenses_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM clinicExpenses")
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
def get_treatment_plan_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM treatmentPlan")
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
# ********************************************************************
@app.route('/add_staff', methods=['POST'])
def add_staff():
    # Get data from the form
    # staffID = request.form['staffID']
    staffName = request.form['staffName']
    jobDescription = request.form['jobDescription']
    salary = request.form['salary']
    staffPhoneNumber = request.form['staffPhoneNumber']
    workDays = request.form['workDays']
    workingHours = request.form['workingHours']
    staffPassword = request.form['staffPassword']

    # Check if the staff phone number already exists
    check_query_phone = "SELECT * FROM staff WHERE staffPhoneNumber = %s"
    my_cursor.execute(check_query_phone, (staffPhoneNumber,))
    existing_staff_phone = my_cursor.fetchone()
    if existing_staff_phone:
        error_message = "Phone number already exists for another staff member."
        print("Error:", error_message)
        flash(error_message, "error")
        return redirect(url_for('staff'))

    # Check if the password already exists
    check_query = "SELECT * FROM staff WHERE staffPassword = %s"
    my_cursor.execute(check_query, (staffPassword,))
    existing_staff = my_cursor.fetchone()

    if existing_staff:
        flash("Error: The password already exists. Please choose a different password.", "error")
        return redirect(url_for('staff'))

    # Insert data into the "patient" table
    insert_query = "INSERT INTO staff (staffName, jobDescription, salary, staffPhoneNumber, workDays, workingHours, staffPassword) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    staff_data = (staffName, jobDescription, salary, staffPhoneNumber, workDays, workingHours, staffPassword)
    my_cursor.execute(insert_query, staff_data)

    # Commit changes and close the connection
    conn.commit()

    print("staff inserted successfully!")

    # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('staff'))
    # ********************************************************************


@app.route('/delete_staff', methods=['POST'])
def delete_staff():
    # Get data from the form
    staffID = request.form['staffID']

    # Delete staff record based on staff ID
    delete_query = "DELETE FROM staff WHERE staffID = %s"
    my_cursor.execute(delete_query, (staffID,))
    conn.commit()
    print(f"Staff with ID {staffID} deleted successfully!")
    # Commit changes and close the connection

    # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('staff'))


# ***************************
@app.route('/update_staff', methods=['POST'])
def update_staff():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Get data from the form
            staffID = request.form['staffID']
            staffName = request.form['staffName']
            jobDescription = request.form['jobDescription']

            # Convert salary to float
            salary = float(request.form['salary']) if request.form['salary'] else None

            staffPhoneNumber = request.form['staffPhoneNumber']
            workDays = request.form['workDays']

            # Convert workingHours to integer if it has a value, otherwise keep it as None
            workingHours = int(request.form['workingHours']) if request.form['workingHours'] else None

            staffPassword = request.form['staffPassword']

            # Check for changes in the form data
            update_query = "UPDATE staff SET"
            update_values = []

            # Build the SET clause dynamically based on form data
            if staffName:
                update_query += " staffName=%s,"
                update_values.append(staffName)
            if jobDescription:
                update_query += " jobDescription=%s,"
                update_values.append(jobDescription)
            if salary is not None:
                update_query += " salary=%s,"
                update_values.append(salary)
            if staffPhoneNumber:
                update_query += " staffPhoneNumber=%s,"
                update_values.append(staffPhoneNumber)
            if workDays:
                update_query += " workDays=%s,"
                update_values.append(workDays)
            if workingHours is not None:
                update_query += " workingHours=%s,"
                update_values.append(workingHours)
            if staffPassword:
                update_query += " staffPassword=%s,"
                update_values.append(staffPassword)

            # Remove the trailing comma and add WHERE clause
            update_query = update_query.rstrip(',') + " WHERE staffID=%s"

            # Add staffID to the values list
            update_values.append(staffID)

            # Update the staff record in the database
            cursor.execute(update_query, tuple(update_values))

            # Commit changes
            conn.commit()

            print(f"Staff with ID {staffID} updated successfully!")

    except Exception as e:
        print(f"Error updating staff with ID {staffID}: {e}")
        conn.rollback()  # Rollback changes in case of an error

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the staff page after updating the staff member
    return redirect(url_for('staff'))

# ********************************************************************
def get_staff_data_sorted_and_paginated(sort_by, sort_order, page, per_page):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the SQL query with sorting and pagination
            query = f"SELECT * FROM staff ORDER BY {sort_by} {sort_order} LIMIT {per_page} OFFSET {(page - 1) * per_page}"
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

# ********************************************************************
@app.route('/add_patient', methods=['POST'])
def add_patient():
    # Get data from the form
    # staffID = request.form['staffID']
    patientName = request.form['patientName']
    patientPhoneNumber = request.form['patientPhoneNumber']
    # Validate phone number
    if len(patientPhoneNumber) != 10 or not patientPhoneNumber.isdigit():
        error_message = 'Invalid phone number. Please enter exactly 10 digits.'
        print("Error:", error_message)
    else:
        # Insert data into the "patient" table
        insert_query = "INSERT INTO patient (patientName, patientPhoneNumber) VALUES (%s, %s)"
        patient_data = (patientName, patientPhoneNumber)
        try:
            my_cursor.execute(insert_query, patient_data)
            conn.commit()
            print("Patient inserted successfully!")
        except IntegrityError as e:
            print("Error:", e.msg)  # Print the error message
            print("Phone number already exists.")
            conn.rollback()  # Rollback the transaction

        # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('patient'))


# ********************************************************************

@app.route('/delete_patient', methods=['POST'])
def delete_patient():
    # Get data from the form
    patientID = request.form['patientID']

    # Delete staff record based on staff ID
    delete_query = "DELETE FROM patient WHERE patientID = %s"
    my_cursor.execute(delete_query, (patientID,))
    conn.commit()
    print(f"patient with ID {patientID} deleted successfully!")
    # Commit changes and close the connection

    # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('patient'))


# ********************************************************************
@app.route('/update_patient', methods=['POST'])
def update_patient():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Get data from the form
            patientID = request.form['patientID']
            patientName = request.form['patientName']
            patientPhoneNumber = request.form['patientPhoneNumber']
            # Check if the new phone number is already associated with another patient
            if patientPhoneNumber:
                cursor.execute("SELECT patientID FROM patient WHERE patientPhoneNumber = %s AND patientID != %s",
                               (patientPhoneNumber, patientID))
                existing_patient = cursor.fetchone()
                if existing_patient:
                    error_message = "Phone number already exists for another patient."
                    print("Error:", error_message)

            # Check for changes in the form data
            update_query = "UPDATE patient SET"
            update_values = []

            # Build the SET clause dynamically based on form data
            if patientName:
                update_query += " patientName=%s,"
                update_values.append(patientName)
            if patientPhoneNumber:
                update_query += " patientPhoneNumber=%s,"
                update_values.append(patientPhoneNumber)
            # Remove the trailing comma and add WHERE clause
            update_query = update_query.rstrip(',') + " WHERE patientID=%s"

            # Add staffID to the values list
            update_values.append(patientID)

            # Update the staff record in the database
            cursor.execute(update_query, tuple(update_values))

            # Commit changes
            conn.commit()

            print(f"patient with ID {patientID} updated successfully!")

    except Exception as e:
        print(f"Error updating patient with ID {patientID}: {e}")
        conn.rollback()  # Rollback changes in case of an error

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the staff page after updating the staff member
    return redirect(url_for('patient'))
# ********************************************************************
def get_total_salary_expense():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
        #     cursor.execute("SELECT SUM(salary) AS total_salary_expense FROM staff")
        #     result = cursor.fetchone()
        #     total_salary_expense = result['total_salary_expense']
        # return total_salary_expense
            cursor.execute("SELECT SUM(salary) AS total_salary_expense, AVG(salary) AS average_salary FROM staff")
            result = cursor.fetchone()
            total_salary_expense = result['total_salary_expense']
            average_salary = result['average_salary']
        return total_salary_expense, average_salary
    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        conn.close()
# ********************************************************************

def get_staff_data_patient(sort_by, sort_order, page, per_page):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the SQL query with sorting and pagination
            query = f"""
                SELECT s.staffID, s.staffName, COUNT(p.patientID) AS num_assigned_patients
                FROM staff s
                LEFT JOIN appointment a ON s.staffID = a.designateStaffID
                LEFT JOIN patient p ON a.assignPatientID = p.patientID
                GROUP BY s.staffID, s.staffName
                ORDER BY {sort_by} {sort_order}
                LIMIT {per_page} OFFSET {(page - 1) * per_page}
            """
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def get_staff_data_sorted_and_paginated(sort_by, sort_order, page, per_page):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the SQL query with sorting and pagination
            query = f"SELECT * FROM staff ORDER BY {sort_by} {sort_order} LIMIT {per_page} OFFSET {(page - 1) * per_page}"
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()
# ********************************************************************

@app.route('/clear_all_staff', methods=['POST'])
def clear_all_staff():
    try:
        # Connect to the database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Execute SQL query to delete all staff data
            cursor.execute("DELETE FROM staff")

            # Commit changes
            conn.commit()

            flash("All staff data cleared successfully!", "success")

    except Exception as e:
        print(f"Error clearing staff data: {e}")
        flash("An error occurred while clearing staff data", "error")
        conn.rollback()

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the staff page
    return redirect(url_for('staff'))
# ********************************************************************

# Separate routes for each search type
@app.route('/search_staff_staffID')
def search_staff_staffID():
    search_term = request.args.get('search')
    return search_staff_by_type('staffID', search_term)


@app.route('/search_staff_staffName')
def search_staff_staffName():
    search_term = request.args.get('search')
    return search_staff_by_type('staffName', search_term)


@app.route('/search_staff_jobDescription')
def search_staff_jobDescription():
    search_term = request.args.get('search')
    return search_staff_by_type('jobDescription', search_term)


@app.route('/search_staff_salary')
def search_staff_salary():
    search_term = request.args.get('search')
    return search_staff_by_type('salary', search_term)



@app.route('/search_staff_staffPhoneNumber')
def search_staff_staffPhoneNumber():
    search_term = request.args.get('search')
    return search_staff_by_type('staffPhoneNumber', search_term)


@app.route('/search_staff_workDays')
def search_staff_workDays():
    search_term = request.args.get('search')
    return search_staff_by_type('workDays', search_term)


@app.route('/search_staff_workingHours')
def search_staff_workingHours():
    search_term = request.args.get('search')
    return search_staff_by_type('workingHours', search_term)

@app.route('/search_staff_staffPassword')
def search_staff_staffPassword():
    search_term = request.args.get('search')
    return search_staff_by_type('staffPassword', search_term)


# Generic search function by type
def search_staff_by_type(search_type, search_term):
    try:
        # Open a new connection
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Query the database based on the search term and type
            search_query = f"SELECT * FROM staff WHERE {search_type} LIKE %s"
            term_with_percent = f"{search_term}"
            cursor.execute(search_query, (term_with_percent,))
            search_results = cursor.fetchall()

    except Exception as e:
        print(f"Error searching staff: {e}")
        search_results = []

    finally:
        # Close the connection
        if conn:
            conn.close()

    # Return the results as JSON
    return jsonify(search_results)

# ********************************************************************
#refresh
@app.route('/get_all_staff')
def get_all_staff():
    staff_data = get_staff_data()
    return jsonify(staff_data)

@app.route('/get_appointments_query', methods=['POST'])
def get_appointments_query():
    try:
        patient_id = request.form['patient_id']  # Assuming the patient_id is sent as a form parameter
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT appointmentNumber, appointmentDate, appointmentTime, appointmentType FROM appointment WHERE assignPatientID = %s;"
            cursor.execute(query, (patient_id,))
            result = cursor.fetchall()
        return render_template('Queries.html', appointment_data=result)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('Queries.html', appointment_data=[])

@app.route('/get_clinic_expenses_query', methods=['POST'])
def get_clinic_expenses_query():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT clinicPaymentNumber, expenses, balance FROM clinicExpenses;"
            cursor.execute(query)
            result = cursor.fetchall()
        return render_template('Queries.html', clinic_expenses_data=result)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('Queries.html', clinic_expenses_data=[])
@app.route('/highest_paid', methods=['POST'])
def highest_paid_query():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT staffID, staffName, jobDescription, salary FROM (SELECT staffID, staffName, jobDescription, salary, RANK() OVER (ORDER BY salary DESC) as ranking  FROM staff) AS ranked_staff WHERE ranking <= 3 ORDER BY ranking;"
            cursor.execute(query)
            result = cursor.fetchall()

        return render_template('Queries.html', highest_paid=result)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('Queries.html', highest_paid=[])

@app.route('/search_patient_patientName')
def search_patient_patientName():
    search_term = request.args.get('search')
    return search_patient_by_type('patientName', search_term)

# ********************************************************************
# Separate routes for each search type
@app.route('/search_patient_patientID')
def search_patient_patientID():
    search_term = request.args.get('search')
    return search_patient_by_type('patientID', search_term)
@app.route('/search_patient_patientPhoneNumber')
def search_patient_patientPhoneNumber():
    search_term = request.args.get('search')
    return search_patient_by_type('patientPhoneNumber', search_term)


# Generic search function by type
def search_patient_by_type(search_type, search_term):
    try:
        # Open a new connection
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Query the database based on the search term and type
            search_query = f"SELECT * FROM patient WHERE {search_type} LIKE %s"
            term_with_percent = f"{search_term}"
            cursor.execute(search_query, (term_with_percent,))
            search_results = cursor.fetchall()

    except Exception as e:
        print(f"Error searching patients: {e}")
        search_results = []

    finally:
        # Close the connection
        if conn:
            conn.close()

    # Return the results as JSON
    return jsonify(search_results)
# ********************************************************************
@app.route('/get_all_patients')
def get_all_patients():
    patient_data = get_patient_data()
    return jsonify(patient_data)

# ********************************************************************
def get_patient_data_sorted_and_paginated(sort_by, sort_order, page, per_page):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the SQL query with sorting and pagination
            query = f"SELECT * FROM patient ORDER BY {sort_by} {sort_order} LIMIT {per_page} OFFSET {(page - 1) * per_page}"
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()
# ********************************************************************

@app.route('/clear_all_patient', methods=['POST'])
def clear_all_patient():
    try:
        # Connect to the database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Execute SQL query to delete all staff data
            cursor.execute("DELETE FROM patient")

            # Commit changes
            conn.commit()

            flash("All staff data cleared successfully!", "success")

    except Exception as e:
        print(f"Error clearing staff data: {e}")
        flash("An error occurred while clearing staff data", "error")
        conn.rollback()

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the staff page
    return redirect(url_for('patient'))
# ********************************************************************
# ********************************************************************
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    # Get data from the form
    assignPatientID= request.form['assignPatientID']
    appointmentDate = request.form['appointmentDate']
    appointmentTime = request.form['appointmentTime']
    appointmentType = request.form['appointmentType']
    designateStaffID= request.form['designateStaffID']
    # Check if the appointment already exists for the specified date, time, and staff
    check_query = "SELECT * FROM appointment WHERE appointmentDate = %s AND appointmentTime = %s AND designateStaffID = %s"
    check_data = (appointmentDate, appointmentTime, designateStaffID)
    my_cursor.execute(check_query, check_data)
    existing_appointment = my_cursor.fetchone()


    if existing_appointment:
        # Appointment already exists, print an error message to the terminal
        print("Error: Appointment already exists for the specified date, time, and staff.")
        return redirect(url_for('Appointment'))  # Redirect back to the staff page or handle as needed

    # Insert data into the "patient" table

    insert_query = "INSERT INTO appointment (assignPatientID,appointmentDate,appointmentTime,appointmentType,designateStaffID) VALUES ( %s,%s, %s,%s,%s)"
    patient_data = ( assignPatientID,appointmentDate,appointmentTime,appointmentType,designateStaffID)
    my_cursor.execute(insert_query, patient_data)

    # Commit changes and close the connection
    conn.commit()

    print("Patient inserted successfully!")

    # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('Appointment'))


# ********************************************************************

@app.route('/delete_appointment', methods=['POST'])
def delete_appointment():
    # Get data from the form
    appointmentNumber = request.form['appointmentNumber']

    # Delete staff record based on staff ID
    delete_query = "DELETE FROM appointment WHERE appointmentNumber = %s"
    my_cursor.execute(delete_query, (appointmentNumber,))
    conn.commit()
    print(f"patient with ID {appointmentNumber} deleted successfully!")
    # Commit changes and close the connection

    # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('Appointment'))


# ********************************************************************
@app.route('/update_appointment', methods=['POST'])
def update_appointment():
    try:
        # Get data from the form
        appointmentNumber = request.form['appointmentNumber']
        assignPatientID = request.form['assignPatientID']
        appointmentDate = request.form['appointmentDate']
        appointmentTime = request.form['appointmentTime']
        appointmentType = request.form['appointmentType']
        designateStaffID = request.form['designateStaffID']
        print(f"Received data: {appointmentNumber},{assignPatientID}, {appointmentDate}, {appointmentTime}, {appointmentType},{designateStaffID}")

        # Check for changes in the form data
        update_query = "UPDATE appointment SET"
        update_values = []

        # Build the SET clause dynamically based on form data
        if assignPatientID:
            update_query += " assignPatientID=%s,"
            update_values.append(assignPatientID)
        if appointmentDate:
            update_query += " appointmentDate=%s,"
            update_values.append(appointmentDate)
        if appointmentTime:
            update_query += " appointmentTime=%s,"
            update_values.append(appointmentTime)
        if appointmentType:
            update_query += " appointmentType=%s,"
            update_values.append(appointmentType)
        if designateStaffID:
            update_query += " designateStaffID=%s,"
            update_values.append(designateStaffID)

        # Remove the trailing comma and add WHERE clause
        update_query = update_query.rstrip(',') + " WHERE appointmentNumber=%s"

        # Add appointmentNumber to the values list
        update_values.append(appointmentNumber)

        # Execute the update query
        my_cursor.execute(update_query, tuple(update_values))

        # Commit changes
        conn.commit()

        print(f"Appointment with the number {appointmentNumber} updated successfully!")

    except Exception as e:
        print(f"Error updating appointment with number {appointmentNumber}: {e}")
        conn.rollback()  # Rollback changes in case of an error

    # Redirect back to the appointment page after updating the appointment
    return redirect(url_for('Appointment'))


# ********************************************************************
# Separate routes for each search type
@app.route('/search_appointment_appointmentNumber')
def search_appointment_appointmentNumber():
    search_term = request.args.get('search')
    return search_appointment_by_type('appointmentNumber', search_term)


@app.route('/search_appointment_assignPatientID')
def search_appointment_assignPatientID():
    search_term = request.args.get('search')
    return search_appointment_by_type('assignPatientID', search_term)


@app.route('/search_appointment_appointmentDate')
def search_appointment_appointmentDate():
    search_term = request.args.get('search')
    return search_appointment_by_type('appointmentDate', search_term)
@app.route('/search_appointment_appointmentTime')
def search_appointment_appointmentTime():
    search_term = request.args.get('search')
    return search_appointment_by_type('appointmentTime', search_term)
@app.route('/search_appointment_appointmentType')
def search_appointment_appointmentType():
    search_term = request.args.get('search')
    return search_appointment_by_type('appointmentType', search_term)
@app.route('/search_appointment_designateStaffID')
def search_appointment_designateStaffID():
    search_term = request.args.get('search')
    return search_appointment_by_type('designateStaffID', search_term)

# Generic search function by type

def search_appointment_by_type(search_type, search_term):
    try:
        # Open a new connection
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Query the database based on the search term and type
            search_query = f"SELECT * FROM appointment WHERE {search_type} LIKE %s"
            term_with_percent = f"{search_term}"
            cursor.execute(search_query, (term_with_percent,))
            search_results = cursor.fetchall()
            # Convert timedelta values to total seconds
            for result in search_results:
                for key, value in result.items():
                    if isinstance(value, timedelta):
                        result[key] = format_timedelta(value)
                    elif isinstance(value, date):
                        result[key] = value.isoformat()


    except Exception as e:
        print(f"Error searching appointment: {e}")
        search_results = []

    finally:
        # Close the connection
        if conn:
            conn.close()

    # Return the results as JSON
    return json.dumps(search_results)
# ********************************************************************

@app.route('/get_all_appointment', methods=['GET'])

def get_all_appointment():
    try:
        # Open a new connection
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Query all appointments from the database
            cursor.execute("SELECT * FROM appointment")
            appointment_data = cursor.fetchall()

            # Convert timedelta values to formatted time
            for appointment in appointment_data:
                for key, value in appointment.items():
                    if isinstance(value, timedelta):
                        appointment[key] = format_timedelta(value)
                    elif isinstance(value, date):
                        appointment[key] = value.isoformat()

    except Exception as e:
        print(f"Error retrieving all appointments: {e}")
        appointment_data = []

    finally:
        # Close the connection
        if conn:
            conn.close()

    # Return the results as JSON
    return json.dumps(appointment_data)

# ********************************************************************
def get_appointment_data_sorted_and_paginated(sort_by, sort_order, page, per_page):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the SQL query with sorting and pagination
            query = f"SELECT * FROM appointment ORDER BY {sort_by} {sort_order} LIMIT {per_page} OFFSET {(page - 1) * per_page}"
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()
# ********************************************************************

@app.route('/clear_all_appointment', methods=['POST'])
def clear_all_appointment():
    try:
        # Connect to the database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Execute SQL query to delete all staff data
            cursor.execute("DELETE FROM appointment")

            # Commit changes
            conn.commit()

            flash("All staff data cleared successfully!", "success")

    except Exception as e:
        print(f"Error clearing staff data: {e}")
        flash("An error occurred while clearing staff data", "error")
        conn.rollback()

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the staff page
    return redirect(url_for('Appointment'))
# ********************************************************************
# ********************************************************************

@app.route('/add_patientPayment', methods=['POST'])
def add_patientPayment():
    # Get data from the form
    PatientID = request.form['PatientID']
    collectStaffID = request.form['collectStaffID']
    patientPaymentDate = request.form['patientPaymentDate']
    amount = request.form['amount']
    patientPaymentType = request.form['patientPaymentType']
    totalToPay= request.form['totalToPay']

    insert_query = "INSERT INTO patientPayment (PatientID,collectStaffID,patientPaymentDate,amount,patientPaymentType,totalToPay) VALUES ( %s,%s, %s,%s,%s,%s)"
    patientPayment_data = (PatientID,collectStaffID,patientPaymentDate,amount,patientPaymentType,totalToPay,)
    my_cursor.execute(insert_query, patientPayment_data)

    # Commit changes and close the connection
    conn.commit()

    print("Patient inserted successfully!")

    # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('patientPayment'))


# ********************************************************************

@app.route('/delete_patientPayment', methods=['POST'])
def delete_patientPayment():
    # Get data from the form
    patientPaymentNumber = request.form['patientPaymentNumber']

    # Delete staff record based on staff ID
    delete_query = "DELETE FROM patientPayment WHERE patientPaymentNumber = %s"
    my_cursor.execute(delete_query, (patientPaymentNumber,))
    conn.commit()
    print(f"patient with ID {patientPaymentNumber} deleted successfully!")
    # Commit changes and close the connection

    # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('patientPayment'))


# ********************************************************************
@app.route('/update_patientPayment', methods=['POST'])
def update_patientPayment():
    try:
        # Get data from the form
        patientPaymentNumber = request.form['patientPaymentNumber']
        PatientID = request.form['PatientID']
        collectStaffID = request.form['collectStaffID']

        patientPaymentDate = request.form['patientPaymentDate']
        # Convert salary to float
        amount = float(request.form['amount']) if request.form['amount'] else None
        patientPaymentType = request.form['patientPaymentType']
        # Convert salary to float
        totalToPay = float(request.form['totalToPay']) if request.form['totalToPay'] else None


        print(f"Received data: {patientPaymentNumber},{PatientID}, {collectStaffID}, {patientPaymentDate}, {amount}, {patientPaymentType},{totalToPay}")

        # Check for changes in the form data
        update_query = "UPDATE patientPayment SET"
        update_values = []

        if PatientID:
            update_query += " PatientID=%s,"
            update_values.append(PatientID)
        if collectStaffID:
            update_query += " collectStaffID=%s,"
            update_values.append(collectStaffID)
        # Build the SET clause dynamically based on form data
        if patientPaymentDate:
            update_query += " patientPaymentDate=%s,"
            update_values.append(patientPaymentDate)
        if amount:
            update_query += " amount=%s,"
            update_values.append(amount)
        if patientPaymentType:
            update_query += " patientPaymentType=%s,"
            update_values.append(patientPaymentType)
        if totalToPay:
            update_query += " totalToPay=%s,"
            update_values.append(totalToPay)

        # Remove the trailing comma and add WHERE clause
        update_query = update_query.rstrip(',') + " WHERE patientPaymentNumber=%s"

        # Add appointmentNumber to the values list
        update_values.append(patientPaymentNumber)

        # Execute the update query
        my_cursor.execute(update_query, tuple(update_values))

        # Commit changes
        conn.commit()

        print(f"payment with the number {patientPaymentNumber} updated successfully!")

    except Exception as e:
        print(f"Error updating appointment with number {patientPaymentNumber}: {e}")
        conn.rollback()  # Rollback changes in case of an error

    # Redirect back to the appointment page after updating the appointment
    return redirect(url_for('patientPayment'))


# ********************************************************************
# Separate routes for each search type
@app.route('/search_patientPayment_patientPaymentNumber')
def search_patientPayment_patientPaymentNumber():
    search_term = request.args.get('search')
    return search_patientPayment_by_type('patientPaymentNumber', search_term)
@app.route('/search_patientPayment_PatientID')
def search_patientPayment_PatientID():
    search_term = request.args.get('search')
    return search_patientPayment_by_type('PatientID', search_term)

@app.route('/search_patientPayment_collectStaffID')
def search_patientPayment_collectStaffID():
    search_term = request.args.get('search')
    return search_patientPayment_by_type('collectStaffID', search_term)
@app.route('/search_patientPayment_patientPaymentDate')
def search_patientPayment_patientPaymentDate():
    search_term = request.args.get('search')
    return search_patientPayment_by_type('patientPaymentDate', search_term)

@app.route('/search_patientPayment_amount')
def search_patientPayment_amount():
    search_term = request.args.get('search')
    return search_patientPayment_by_type('amount', search_term)

@app.route('/search_patientPayment_patientPaymentType')
def search_patientPayment_patientPaymentType():
    search_term = request.args.get('search')
    return search_patientPayment_by_type('patientPaymentType', search_term)

@app.route('/search_patientPayment_totalToPay')
def search_patientPayment_totalToPay():
    search_term = request.args.get('search')
    return search_patientPayment_by_type('totalToPay', search_term)

# # Generic search function by type
#
def search_patientPayment_by_type(search_type, search_term):
    try:
        # Open a new connection
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Query the database based on the search term and type
            search_query = f"SELECT * FROM patientPayment WHERE {search_type} LIKE %s"
            term_with_percent = f"{search_term}"
            cursor.execute(search_query, (term_with_percent,))
            search_results = cursor.fetchall()
            # Convert timedelta values to total seconds
            for result in search_results:
                for key, value in result.items():
                    if isinstance(value, date):
                        result[key] = value.isoformat()


    except Exception as e:
        print(f"Error searching appointment: {e}")
        search_results = []

    finally:
        # Close the connection
        if conn:
            conn.close()

    # Return the results as JSON
    return json.dumps(search_results)
# # ********************************************************************
@app.route('/get_all_patientPayment', methods=['GET'])

def get_all_patientPayment():
    try:
        # Open a new connection
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Query all appointments from the database
            cursor.execute("SELECT *, (totalToPay - amount) AS amountLeftToPay FROM patientPayment")
            patientPayment_data = cursor.fetchall()

            # Convert timedelta values to formatted time
            for patientPayment in patientPayment_data:
                for key, value in patientPayment.items():
                    if isinstance(value, timedelta):
                        patientPayment[key] = format_timedelta(value)
                    elif isinstance(value, date):
                        patientPayment[key] = value.isoformat()

    except Exception as e:
        print(f"Error retrieving all patientPayment: {e}")
        patientPayment_data = []

    finally:
        # Close the connection
        if conn:
            conn.close()

    # Return the results as JSON
    return json.dumps(patientPayment_data)

# # ********************************************************************
def get_patientPayment_data_sorted_and_paginated(sort_by, sort_order, page, per_page):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the SQL query with sorting and pagination
            query = f"SELECT * FROM patientPayment ORDER BY {sort_by} {sort_order} LIMIT {per_page} OFFSET {(page - 1) * per_page}"
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()
# ********************************************************************
@app.route('/clear_all_patientPayment', methods=['POST'])
def clear_all_patientPayment():
    try:
        # Connect to the database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Execute SQL query to delete all staff data
            cursor.execute("DELETE FROM patientPayment")

            # Commit changes
            conn.commit()

            flash("All staff data cleared successfully!", "success")

    except Exception as e:
        print(f"Error clearing staff data: {e}")
        flash("An error occurred while clearing patientPayment data", "error")
        conn.rollback()

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the staff page
    return redirect(url_for('patientPayment'))
# ********************************************************************
def get_debt_patient(sort_by, sort_order, page, per_page):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the new SQL query with sorting and pagination
            query = f"""
                SELECT
                    p.patientID,
                    p.patientName,
                    pp.patientPaymentDate,
                    pp.totalToPay,
                    pp.amountLeftToPay
                FROM
                    patient p
                JOIN
                    patientPayment pp ON p.patientID = pp.PatientID
                JOIN
                    appointment a ON p.patientID = a.assignPatientID
                WHERE
                    pp.patientPaymentDate = a.appointmentDate
                    AND pp.PatientID = a.assignPatientID
                    AND pp.amountLeftToPay > 0
                ORDER BY {sort_by} {sort_order}
            """
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

# ********************************************************************

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            equipmentName = request.form['equipmentName']
            maintenanceDate = request.form['maintenanceDate']
            supplierID = int(request.form['supplierID'])

            insert_query = "INSERT INTO equipment (equipmentName, maintenanceDate, supplierID) VALUES (%s, %s, %s)"
            equipment_data = (equipmentName, maintenanceDate, supplierID)
            cursor.execute(insert_query, equipment_data)
            conn.commit()
            print("Equipment inserted successfully!")

    except Exception as e:
        print(f"Error inserting equipment: {e}")
        conn.rollback()
        return render_template('error.html', error_message=f"Error inserting equipment: {e}")

    finally:
        conn.close()
    return redirect(url_for('equipment'))


@app.route('/delete_equipment', methods=['POST'])
def delete_equipment():
    equipment_id = request.form['equipmentID']
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            delete_query = "DELETE FROM equipment WHERE equipmentID = %s"
            cursor.execute(delete_query, (equipment_id,))
            conn.commit()
            print(f"Equipment with ID {equipment_id} deleted successfully!")
    except Exception as e:
        print(f"Error deleting equipment: {e}")
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for('equipment'))


# ***************************
@app.route('/update_equipment', methods=['POST'])
def update_equipment():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Get data from the form
            equipmentID = request.form['equipmentID']
            newEquipmentName = request.form['newEquipmentName']
            newMaintenanceDate = request.form['newMaintenanceDate']
            newSupplierID = request.form['newSupplierID']

            # Check for changes in the form data
            update_query = "UPDATE equipment SET"
            update_values = []

            # Build the SET clause dynamically based on form data
            if newEquipmentName:
                update_query += " equipmentName=%s,"
                update_values.append(newEquipmentName)
            if newMaintenanceDate:
                update_query += " maintenanceDate=%s,"
                update_values.append(newMaintenanceDate)
            if newSupplierID:
                update_query += " supplierID=%s,"
                update_values.append(newSupplierID)

            # Remove the trailing comma and add WHERE clause
            update_query = update_query.rstrip(',') + " WHERE equipmentID=%s"

            # Add equipmentID to the values list
            update_values.append(equipmentID)

            # Update the equipment record in the database
            cursor.execute(update_query, tuple(update_values))

            # Commit changes
            conn.commit()

            print(f"Equipment with ID {equipmentID} updated successfully!")

    except Exception as e:
        print(f"Error updating equipment with ID {equipmentID}: {e}")
        conn.rollback()  # Rollback changes in case of an error

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the equipment page after updating the equipment
    return redirect(url_for('equipment'))

# ********************************************************************

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            expenses = float(request.form['expenses']) if request.form['expenses'] else None
            balance = float(request.form['balance']) if request.form['balance'] else None
            expensesStaffID = int(request.form['expensesStaffID']) if request.form['expensesStaffID'] else None

            insert_query = "INSERT INTO clinicExpenses (expenses, balance, expensesStaffID) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (expenses, balance, expensesStaffID))
            conn.commit()
            print("Expense added successfully!")

    except Exception as e:
        print(f"Error adding expense: {e}")
        conn.rollback()

    finally:
        conn.close()

    return redirect(url_for('clinicExpenses'))


# ***************************
@app.route('/update_expense', methods=['POST'])
def update_expense():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Get data from the form
            clinicPaymentNumber = request.form['clinicPaymentNumber']
            newExpenses = float(request.form['newExpenses']) if request.form['newExpenses'] else None
            newBalance = float(request.form['newBalance']) if request.form['newBalance'] else None
            newExpensesStaffID = int(request.form['newExpensesStaffID']) if request.form['newExpensesStaffID'] else None

            # Check for changes in the form data
            update_query = "UPDATE clinicExpenses SET"
            update_values = []

            # Build the SET clause dynamically based on form data
            if newExpenses is not None:
                update_query += " expenses=%s,"
                update_values.append(newExpenses)
            if newBalance is not None:
                update_query += " balance=%s,"
                update_values.append(newBalance)
            if newExpensesStaffID is not None:
                update_query += " expensesStaffID=%s,"
                update_values.append(newExpensesStaffID)

            # Remove the trailing comma and add WHERE clause
            update_query = update_query.rstrip(',') + " WHERE clinicPaymentNumber=%s"

            # Add clinicPaymentNumber to the values list
            update_values.append(clinicPaymentNumber)

            # Update the clinicExpenses record in the database
            cursor.execute(update_query, tuple(update_values))

            # Commit changes
            conn.commit()

            print(f"Expense with Payment Number {clinicPaymentNumber} updated successfully!")

    except Exception as e:
        print(f"Error updating expense with Payment Number {clinicPaymentNumber}: {e}")
        conn.rollback()  # Rollback changes in case of an error

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the clinicExpenses page after updating the expense
    return redirect(url_for('clinicExpenses'))


@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            clinicPaymentNumber = int(request.form['clinicPaymentNumber']) if request.form[
                'clinicPaymentNumber'] else None

            delete_query = "DELETE FROM clinicExpenses WHERE clinicPaymentNumber = %s"
            cursor.execute(delete_query, (clinicPaymentNumber,))
            conn.commit()
            print(f"Expense with Payment Number {clinicPaymentNumber} deleted successfully!")

    except Exception as e:
        print(f"Error deleting expense with Payment Number {clinicPaymentNumber}: {e}")
        conn.rollback()

    finally:
        conn.close()

    return redirect(url_for('clinicExpenses'))

# ********************************************************************
# Add Treatment Plan
@app.route('/add_treatment_plan', methods=['POST'])
def add_treatment_plan():
    try:
        diagnosis = request.form['diagnosis']
        progress = request.form['progress']
        prescriptions = request.form['prescriptions']
        treatmentName = request.form['treatmentName']
        patientID = int(request.form['patientID'])
        staffID = int(request.form['staffID'])

        insert_query = "INSERT INTO treatmentPlan (diagnosis, progress, prescriptions, treatmentName, PatientID, StaffID) VALUES (%s, %s, %s, %s, %s, %s)"
        treatment_data = (diagnosis, progress, prescriptions, treatmentName, patientID, staffID)

        my_cursor.execute(insert_query, treatment_data)
        conn.commit()

        print("Treatment plan added successfully!")

    except Exception as e:
        print(f"Error adding treatment plan: {e}")
        conn.rollback()

    return redirect(url_for('treatmentPlan'))


# Delete Treatment Plan
@app.route('/delete_treatment_plan', methods=['POST'])
def delete_treatment_plan():
    try:
        treatmentID = int(request.form['treatmentID'])

        delete_query = "DELETE FROM treatmentPlan WHERE treatmentID = %s"
        my_cursor.execute(delete_query, (treatmentID,))
        conn.commit()

        print(f"Treatment plan with ID {treatmentID} deleted successfully!")

    except Exception as e:
        print(f"Error deleting treatment plan: {e}")
        conn.rollback()

    return redirect(url_for('treatmentPlan'))


# Update Treatment Plan
@app.route('/update_treatment_plan', methods=['POST'])
def update_treatment_plan():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Get data from the form
            treatmentID = request.form['treatmentID']
            newDiagnosis = request.form['newDiagnosis']
            newProgress = request.form['newProgress']
            newPrescriptions = request.form['newPrescriptions']
            newTreatmentName = request.form['newTreatmentName']
            newPatientID = request.form['newPatientID']
            newStaffID = request.form['newStaffID']

            # Check for changes in the form data
            update_query = "UPDATE treatmentPlan SET"
            update_values = []

            # Build the SET clause dynamically based on form data
            if newDiagnosis:
                update_query += " diagnosis=%s,"
                update_values.append(newDiagnosis)
            if newProgress:
                update_query += " progress=%s,"
                update_values.append(newProgress)
            if newPrescriptions:
                update_query += " prescriptions=%s,"
                update_values.append(newPrescriptions)
            if newTreatmentName:
                update_query += " treatmentName=%s,"
                update_values.append(newTreatmentName)
            if newPatientID:
                update_query += " PatientID=%s,"
                update_values.append(newPatientID)
            if newStaffID:
                update_query += " StaffID=%s,"
                update_values.append(newStaffID)

            # Remove the trailing comma and add WHERE clause
            update_query = update_query.rstrip(',') + " WHERE treatmentID=%s"

            # Add treatmentID to the values list
            update_values.append(treatmentID)

            # Update the treatment plan in the database
            cursor.execute(update_query, tuple(update_values))

            # Commit changes
            conn.commit()

            print(f"Treatment plan with ID {treatmentID} updated successfully!")

    except Exception as e:
        print(f"Error updating treatment plan with ID {treatmentID}: {e}")
        conn.rollback()  # Rollback changes in case of an error

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the treatment plan page after updating
    return redirect(url_for('treatmentPlan'))


# ********************************************************************
#counters:

@app.route('/get_patient_count', methods=['POST'])
def get_patient_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            count_query = "SELECT COUNT(patientID) AS patientCount FROM patient;"
            cursor.execute(count_query)
            result = cursor.fetchone()
            patient_count = result['patientCount'] if result else None

        session['patient_count'] = patient_count
        return patient_count
    except Exception as e:
        print(f"Error: {e}")
        return None


@app.route('/staff_count')
def get_staff_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT COUNT(staffID) AS staffCount FROM staff;"
            cursor.execute(query)
            result = cursor.fetchone()
            staff_count = result['staffCount']

        # Storing the staff count in the session variable
        session['staff_count'] = staff_count

        return staff_count
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()


@app.route('/appointment_count')
def get_appointment_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT COUNT(appointmentNumber) AS appointment_count FROM appointment;"
            cursor.execute(query)
            result = cursor.fetchone()
            appointment_count = result['appointment_count']

        session['appointment_count'] = appointment_count

        return appointment_count
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()


@app.route('/patient_payment_count')
def get_patient_payment_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT COUNT(patientPaymentNumber) AS patient_payment_count FROM patientPayment;"
            cursor.execute(query)
            result = cursor.fetchone()
            patient_payment_count = result['patient_payment_count']

        session['patient_payment_count'] = patient_payment_count

        return patient_payment_count
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()


@app.route('/treatment_plan_count')
def get_treatment_plan_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT COUNT(treatmentID) AS treatment_plan_count FROM treatmentPlan;"
            cursor.execute(query)
            result = cursor.fetchone()
            treatment_plan_count = result['treatment_plan_count']

        session['treatment_plan_count'] = treatment_plan_count

        return treatment_plan_count
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()


@app.route('/laboratory_count')
def get_laboratory_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT COUNT(laboratoryPhoneNumber) AS laboratory_count FROM laboratory;"
            cursor.execute(query)
            result = cursor.fetchone()
            laboratory_count = result['laboratory_count']

        session['laboratory_count'] = laboratory_count

        return laboratory_count
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()


@app.route('/supplier_count')
def get_supplier_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT COUNT(supplierID) AS supplier_count FROM supplier;"
            cursor.execute(query)
            result = cursor.fetchone()
            supplier_count = result['supplier_count']

        session['supplier_count'] = supplier_count

        return supplier_count
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()


@app.route('/equipment_count')
def get_equipment_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT COUNT(equipmentID) AS equipment_count FROM equipment;"
            cursor.execute(query)
            result = cursor.fetchone()
            equipment_count = result['equipment_count']

        session['equipment_count'] = equipment_count

        return equipment_count
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()


@app.route('/clinic_expenses_count')
def get_clinic_expenses_count():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = "SELECT COUNT(clinicPaymentNumber) AS clinic_expenses_count FROM clinicExpenses;"
            cursor.execute(query)
            result = cursor.fetchone()
            clinic_expenses_count = result['clinic_expenses_count']

        session['clinic_expenses_count'] = clinic_expenses_count

        return clinic_expenses_count
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

# ********************************************************************
# ********************************************************************
# laboratory
# ********************************************************************
def get_laboratory_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM laboratory")
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


# ********************************************************************

# refresh
@app.route('/get_all_laboratory')
def get_all_laboratory():
    laboratory_data = get_laboratory_data()
    return jsonify(laboratory_data)


# ********************************************************************
def get_laboratory_data_sorted_and_paginated(sort_by, sort_order, page, per_page):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the SQL query with sorting and pagination
            query = f"SELECT * FROM laboratory ORDER BY {sort_by} {sort_order} LIMIT {per_page} OFFSET {(page - 1) * per_page}"
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


# ********************************************************************
@app.route('/add_laboratory', methods=['POST'])
def add_laboratory():
    # Get data from the form
    # laboratoryID = request.form['laboratoryID']
    laboratoryPhoneNumber = request.form['laboratoryPhoneNumber']
    laboratoryName = request.form['laboratoryName']
    exportType = request.form['exportType']
    PatientID = request.form['PatientID']
    requestStaffID = request.form['requestStaffID']

    # Insert data into the "patient" table
    insert_query = "INSERT INTO laboratory (laboratoryPhoneNumber, laboratoryName, exportType, PatientID, requestStaffID) VALUES (%s, %s, %s, %s, %s)"
    laboratory_data = (laboratoryPhoneNumber, laboratoryName, exportType, PatientID, requestStaffID)
    my_cursor.execute(insert_query, laboratory_data)

    # Commit changes and close the connection
    conn.commit()

    print("Laboratory inserted successfully!")

    # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('laboratory'))


# ********************************************************************
@app.route('/delete_laboratory', methods=['POST'])
def delete_laboratory():
    # Get data from the form
    laboratoryID = request.form['laboratoryID']

    delete_query = "DELETE FROM laboratory WHERE laboratoryID = %s"
    my_cursor.execute(delete_query, (laboratoryID,))
    conn.commit()
    print(f"laboratory with ID {laboratoryID} deleted successfully!")
    # Commit changes and close the connection

    return redirect(url_for('laboratory'))


# ********************************************************************
@app.route('/update_laboratory', methods=['POST'])
def update_laboratory():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Get data from the form
            laboratoryID = request.form['laboratoryID']
            laboratoryPhoneNumber = request.form['laboratoryPhoneNumber']
            laboratoryName = request.form['laboratoryName']
            exportType = request.form['exportType']
            PatientID = int(request.form['PatientID']) if request.form['PatientID'] else None
            requestStaffID = int(request.form['requestStaffID']) if request.form['requestStaffID'] else None

            # Check for changes in the form data
            update_query = "UPDATE laboratory SET"
            update_values = []

            # Build the SET clause dynamically based on form data
            if laboratoryID:
                update_query += " laboratoryID=%s,"
                update_values.append(laboratoryID)
            if laboratoryPhoneNumber:
                update_query += " laboratoryPhoneNumber=%s,"
                update_values.append(laboratoryPhoneNumber)
            if laboratoryName:
                update_query += "laboratoryName=%s,"
                update_values.append(laboratoryName)
            if exportType:
                update_query += "exportType=%s,"
                update_values.append(exportType)
            if PatientID is not None:
                update_query += " PatientID=%s,"
                update_values.append(PatientID)
            if requestStaffID is not None:
                update_query += " requestStaffID=%s,"
                update_values.append(requestStaffID)

            # Remove the trailing comma and add WHERE clause
            update_query = update_query.rstrip(',') + " WHERE laboratoryID=%s"

            # Add laboratoryID to the values list
            update_values.append(laboratoryID)

            # Update the laboratory record in the database
            cursor.execute(update_query, tuple(update_values))

            # Commit changes
            conn.commit()

            print(f"laboratory with ID {laboratoryID} updated successfully!")

    except Exception as e:
        print(f"Error updating laboratory with ID {laboratoryID}: {e}")
        conn.rollback()  # Rollback changes in case of an error

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the laboratory page after updating the laboratory member
    return redirect(url_for('laboratory'))


# ********************************************************************
@app.route('/clear_all_laboratory', methods=['POST'])
def clear_all_laboratory():
    try:
        # Connect to the database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Execute SQL query to delete all laboratory data
            cursor.execute("DELETE FROM laboratory")

            # Commit changes
            conn.commit()

            flash("All laboratory data cleared successfully!", "success")

    except Exception as e:
        print(f"Error clearing laboratory data: {e}")
        flash("An error occurred while clearing laboratory data", "error")
        conn.rollback()

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the laboratory page
    return redirect(url_for('laboratory'))


# ********************************************************************
# Separate routes for each search type
@app.route('/search_laboratory_laboratoryID')
def search_laboratory_laboratoryID():
    search_term = request.args.get('search')
    return search_laboratory_by_type('laboratoryID', search_term)


# Separate routes for each search type
@app.route('/search_laboratory_laboratoryPhoneNumber')
def search_laboratory_laboratoryPhoneNumber():
    search_term = request.args.get('search')
    return search_laboratory_by_type('laboratoryPhoneNumber', search_term)


# Separate routes for each search type
@app.route('/search_laboratory_laboratoryName')
def search_laboratory_laboratoryName():
    search_term = request.args.get('search')
    return search_laboratory_by_type('laboratoryName', search_term)


@app.route('/search_laboratory_exportType')
def search_laboratory_exportType():
    search_term = request.args.get('search')
    return search_laboratory_by_type('exportType', search_term)


@app.route('/search_laboratory_PatientID')
def search_laboratory_PatientID():
    search_term = request.args.get('search')
    return search_laboratory_by_type('PatientID', search_term)


@app.route('/search_laboratory_requestStaffID')
def search_laboratory_requestStaffID():
    search_term = request.args.get('search')
    return search_laboratory_by_type('requestStaffID', search_term)


# Generic search function by type
def search_laboratory_by_type(search_type, search_term):
    try:
        # Open a new connection
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Query the database based on the search term and type
            search_query = f"SELECT * FROM laboratory WHERE {search_type} LIKE %s"
            term_with_percent = f"{search_term}"
            cursor.execute(search_query, (term_with_percent,))
            search_results = cursor.fetchall()

    except Exception as e:
        print(f"Error searching laboratory: {e}")
        search_results = []

    finally:
        # Close the connection
        if conn:
            conn.close()

    # Return the results as JSON
    return jsonify(search_results)


# ********************************************************************
def get_lab_and_staff_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # SQL query to get laboratories and their requesting staff
            query = """
                SELECT l.*, s.*
                FROM laboratory l
                JOIN staff s ON l.requestStaffID = s.staffID
            """
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

# ********************************************************************
def get_lab_and_patient_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            query = """
                SELECT l.*, p.*
                FROM laboratory l
                JOIN patient p ON l.PatientID = p.patientID
            """
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

# ********************************************************************
def get_supplier_and_equipment_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:

            query = """
                SELECT s.*, e.equipmentName, e.equipmentID
                FROM supplier s
                INNER JOIN equipment e ON s.supplierID = e.supplierID;
            """
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()
    # ********************************************************************
def get_staff_and_patient_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:

            query = """
                select p.patientID , p.patientName ,s.staffID,s.staffName,a.appointmentDate,a.appointmentTime from patient p, staff s, appointment a where p.patientID=a.assignPatientID AND s.staffID=a.designateStaffID

            """
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

@app.route('/')
def index():
    return render_template('web.html')


# ********************************************************************

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        try:
            staffID = request.form['staffID']
            password = request.form['password']

            # Check staff ID and password against the database
            query = "SELECT * FROM staff WHERE staffID = %s AND staffPassword = %s"
            my_cursor.execute(query, (staffID, password))
            staff = my_cursor.fetchone()

            if staff:
                # Login successful, set session variable or redirect
                session['staffID'] = staffID
                flash('Login successful!', 'success')
                print("'Login successful!', 'success'")
                return redirect(url_for('homepage'))
            else:
                flash('Invalid staff ID or password', 'error')
                print("'Invalid staff ID or password', 'error'")

        except KeyError as e:
            print(f"KeyError: {e}")
            flash('Invalid form submission', 'error')



    return render_template('login.html')  # You need to have a login.html template


# Helper function to retrieve staff data by ID
def get_staff_by_id(staffID):
    for staff in get_staff_data():
        if staff['staffID'] == staffID:
            return staff
    return None


# ********************************************************************

@app.route('/About')
def About():
    return render_template('About.html')


# ********************************************************************

@app.route('/Patient')
def patient():
    # Get sorting parameters from the query string
    sort_by = request.args.get('sort_by', 'patientID')
    sort_order = request.args.get('sort_order', 'asc')

    # Toggle sort_order
    new_sort_order = 'desc' if sort_order == 'asc' else 'asc'

    # Get pagination parameters from the query string
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Get staff data from the database (sorted and paginated)
    patient_data = get_patient_data_sorted_and_paginated(sort_by, sort_order, page, per_page)

    return render_template('Patient.html', patient_data=patient_data, new_sort_order=new_sort_order)


# ********************************************************************
def upcoming_appointments_query():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the new SQL query with sorting and pagination
            query = f"""
               SELECT p.patientID, s.staffID, a.appointmentTime, a.appointmentDate, a.appointmentType FROM appointment a JOIN patient p ON a.assignPatientID = p.patientID JOIN staff s ON a.designateStaffID = s.staffID ORDER BY a.appointmentDate, a.appointmentTime
            """
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()
# ********************************************************************
@app.route('/Home_page')
def homepage():
    upcoming_data = upcoming_appointments_query()
    return render_template('Home_page.html',upcoming_data=upcoming_data)


# ********************************************************************

@app.route('/Patient_Payment')
def patientPayment():
    # Get sorting parameters from the query string
    sort_by = request.args.get('sort_by', 'patientPaymentNumber')
    sort_order = request.args.get('sort_order', 'asc')

    # Toggle sort_order
    new_sort_order = 'desc' if sort_order == 'asc' else 'asc'

    # Get pagination parameters from the query string
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Get staff data from the database (sorted and paginated)
    patientPayment_data = get_patientPayment_data_sorted_and_paginated(sort_by, sort_order, page, per_page)
    debt_patients = get_debt_patient(sort_by, sort_order, page, per_page)

    return render_template('Patient_Payment.html', patientPayment_data=patientPayment_data, new_sort_order=new_sort_order, debt_patients=debt_patients)


# ********************************************************************


def get_supplier_data():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM supplier")
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


# ********************************************************************

# refresh
@app.route('/get_all_supplier')
def get_all_supplier():
    supplier_data = get_supplier_data()
    return jsonify(supplier_data)


# ********************************************************************
def get_supplier_data_sorted_and_paginated(sort_by, sort_order, page, per_page):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Construct the SQL query with sorting and pagination
            query = f"SELECT * FROM supplier ORDER BY {sort_by} {sort_order} LIMIT {per_page} OFFSET {(page - 1) * per_page}"
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


# ********************************************************************
@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    # Get data from the form
    # supplierID = request.form['supplierID']
    supplierPhoneNumber = request.form['supplierPhoneNumber']
    companyName = request.form['companyName']

    # Insert data into the "patient" table
    insert_query = "INSERT INTO supplier (supplierPhoneNumber, companyName) VALUES (%s, %s)"
    supplier_data = (supplierPhoneNumber, companyName)
    my_cursor.execute(insert_query, supplier_data)

    # Commit changes and close the connection
    conn.commit()

    print("Supplier inserted successfully!")

    # Redirect back to the staff page after adding a new staff member
    return redirect(url_for('supplier'))


# ********************************************************************
# ********************************************************************
@app.route('/delete_supplier', methods=['POST'])
def delete_supplier():
    # Get data from the form
    supplierID = request.form['supplierID']

    delete_query = "DELETE FROM supplier WHERE supplierID = %s"
    my_cursor.execute(delete_query, (supplierID,))
    conn.commit()
    print(f"supplier with ID {supplierID} deleted successfully!")
    # Commit changes and close the connection

    return redirect(url_for('supplier'))


# ********************************************************************
# ********************************************************************
@app.route('/update_supplier', methods=['POST'])
def update_supplier():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Get data from the form
            supplierID = request.form['supplierID']
            supplierPhoneNumber = request.form['supplierPhoneNumber']
            companyName = request.form['companyName']

            # Check for changes in the form data
            update_query = "UPDATE supplier SET"
            update_values = []

            # Build the SET clause dynamically based on form data
            if supplierID:
                update_query += " supplierID=%s,"
                update_values.append(supplierID)
            if supplierPhoneNumber:
                update_query += " supplierPhoneNumber=%s,"
                update_values.append(supplierPhoneNumber)
            if companyName:
                update_query += "companyName=%s,"
                update_values.append(companyName)

            # Remove the trailing comma and add WHERE clause
            update_query = update_query.rstrip(',') + " WHERE supplierID=%s"

            # Add supplier to the values list
            update_values.append(supplierID)

            # Update the supplier record in the database
            cursor.execute(update_query, tuple(update_values))

            # Commit changes
            conn.commit()

            print(f"supplier with ID {supplierID} updated successfully!")

    except Exception as e:
        print(f"Error updating supplier with ID {supplierID}: {e}")
        conn.rollback()  # Rollback changes in case of an error

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the supplier page after updating the supplier member
    return redirect(url_for('supplier'))


# ********************************************************************
@app.route('/clear_all_supplier', methods=['POST'])
def clear_all_supplier():
    try:
        # Connect to the database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Execute SQL query to delete all supplier data
            cursor.execute("DELETE FROM supplier")

            # Commit changes
            conn.commit()

            flash("All supplier data cleared successfully!", "success")

    except Exception as e:
        print(f"Error clearing supplier data: {e}")
        flash("An error occurred while clearing supplier data", "error")
        conn.rollback()

    finally:
        # Close the connection
        conn.close()

    # Redirect back to the supplier page
    return redirect(url_for('supplier'))


# ********************************************************************
# ********************************************************************
# Separate routes for each search type
@app.route('/search_supplier_supplierID')
def search_supplier_supplierID():
    search_term = request.args.get('search')
    return search_supplier_by_type('supplierID', search_term)


# Separate routes for each search type
@app.route('/search_supplier_supplierPhoneNumber')
def search_supplier_supplierPhoneNumber():
    search_term = request.args.get('search')
    return search_supplier_by_type('supplierPhoneNumber', search_term)


@app.route('/search_supplier_companyName')
def search_supplier_companyName():
    search_term = request.args.get('search')
    return search_supplier_by_type('companyName', search_term)


# Generic search function by type
def search_supplier_by_type(search_type, search_term):
    try:
        # Open a new connection
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0267',
            db='clinic',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Query the database based on the search term and type
            search_query = f"SELECT * FROM supplier WHERE {search_type} LIKE %s"
            term_with_percent = f"{search_term}"
            cursor.execute(search_query, (term_with_percent,))
            search_results = cursor.fetchall()

    except Exception as e:
        print(f"Error searching supplier: {e}")
        search_results = []

    finally:
        # Close the connection
        if conn:
            conn.close()

    # Return the results as JSON
    return jsonify(search_results)


# *******************************************************************

# ********************************************************************

@app.route('/Appointment')
def Appointment():
    # Get sorting parameters from the query string
    sort_by = request.args.get('sort_by', 'appointmentNumber')
    sort_order = request.args.get('sort_order', 'asc')

    # Toggle sort_order
    new_sort_order = 'desc' if sort_order == 'asc' else 'asc'

    # Get pagination parameters from the query string
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Get staff data from the database (sorted and paginated)
    appointment_data = get_appointment_data_sorted_and_paginated(sort_by, sort_order, page, per_page)
    patient_staff_data=get_staff_and_patient_data()
    # print(appointment_data)  # Add this line to check data in the console

    return render_template('Appointment.html', appointment_data=appointment_data, new_sort_order=new_sort_order,patient_staff_data=patient_staff_data)


# ********************************************************************
@app.route('/staff')
def staff():
    # Get sorting parameters from the query string
    sort_by = request.args.get('sort_by', 'staffID')
    sort_order = request.args.get('sort_order', 'asc')

    # Toggle sort_order
    new_sort_order = 'desc' if sort_order == 'asc' else 'asc'

    # Get pagination parameters from the query string
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Get staff data from the database (sorted and paginated)
    staff_data = get_staff_data_sorted_and_paginated(sort_by, sort_order, page, per_page)
 # Get the total salary expense (assuming it's a single value)
    # total_salary_expense = get_total_salary_expense()
    total_salary_expense, average_salary = get_total_salary_expense()

    num_assigned_patients = get_staff_data_patient(sort_by, sort_order, page, per_page)

    return render_template('staff.html', staff_data=staff_data, new_sort_order=new_sort_order, total_salary_expense=total_salary_expense,average_salary=average_salary,num_assigned_patients=num_assigned_patients)

# ********************************************************************


# ********************************************************************

@app.route('/treatmentPlan')
def treatmentPlan():
    treatment_plan_data = get_treatment_plan_data()  # Replace with your function to fetch treatment plan data
    return render_template('treatmentPlan.html', treatment_plan_data=treatment_plan_data)


# ********************************************************************
# ********************************************************************
@app.route('/laboratory')
def laboratory():
    # Get sorting parameters from the query string
    sort_by = request.args.get('sort_by', 'laboratoryPhoneNumber')
    sort_order = request.args.get('sort_order', 'asc')

    # Toggle sort_order
    new_sort_order = 'desc' if sort_order == 'asc' else 'asc'

    # Get pagination parameters from the query string
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Get staff data from the database (sorted and paginated)
    laboratory_data = get_laboratory_data_sorted_and_paginated(sort_by, sort_order, page, per_page)
    lab_and_staff_data = get_lab_and_staff_data()
    lab_and_patient_data=get_lab_and_patient_data()

    return render_template('laboratory.html', laboratory_data=laboratory_data, new_sort_order=new_sort_order,lab_and_staff_data=lab_and_staff_data,lab_and_patient_data=lab_and_patient_data)


# ********************************************************************


# ********************************************************************
@app.route('/supplier')
def supplier():
    # Get sorting parameters from the query string
    sort_by = request.args.get('sort_by', 'supplierID')
    sort_order = request.args.get('sort_order', 'asc')

    # Toggle sort_order
    new_sort_order = 'desc' if sort_order == 'asc' else 'asc'

    # Get pagination parameters from the query string
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Get staff data from the database (sorted and paginated)
    supplier_data = get_supplier_data_sorted_and_paginated(sort_by, sort_order, page, per_page)
    supplier_and_equipment_data = get_supplier_and_equipment_data()
    return render_template('supplier.html', supplier_data=supplier_data, new_sort_order=new_sort_order,supplier_and_equipment_data=supplier_and_equipment_data)



@app.route('/Queries')
def Queries():
    patient_count = get_patient_count()
    session['patient_count'] = patient_count
    staff_count = get_staff_count()
    session['staff_count'] = staff_count
    appointment_count = get_appointment_count()
    session['appointment_count'] = appointment_count
    patient_payment_count = get_patient_payment_count()
    session['patient_payment_count'] = patient_payment_count
    treatment_plan_count= get_treatment_plan_count()
    session['treatment_plan_count'] = treatment_plan_count
    laboratory_count = get_laboratory_count()
    session['laboratory_count'] = laboratory_count
    supplier_count = get_supplier_count()
    session['supplier_count'] = supplier_count
    equipment_count = get_equipment_count()
    session['equipment_count'] = equipment_count
    clinic_expenses_count = get_clinic_expenses_count()
    session['clinic_expenses_count'] = clinic_expenses_count

    return render_template('Queries.html', patient_count=patient_count, staff_count=staff_count, appointment_count=appointment_count, patient_payment_count=patient_payment_count, treatment_plan_count=treatment_plan_count, laboratory_count=laboratory_count, supplier_count=supplier_count, equipment_count=equipment_count, clinic_expenses_count=clinic_expenses_count)


# ********************************************************************
@app.route('/equipment')
def equipment():
    equipment_data = get_equipment_data()  # Retrieve equipment data from the database
    return render_template('equipment.html', equipment_data=equipment_data)


# ********************************************************************
@app.route('/clinicExpenses')
def clinicExpenses():
    clinic_expenses_data = get_expenses_data()
    return render_template('clinicExpenses.html', clinic_expenses_data=clinic_expenses_data)

if __name__ == '__main__':
    app.run(debug=True)
