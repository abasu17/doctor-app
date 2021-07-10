from app import *
from datetime import timedelta
from flask import render_template, request, session, send_from_directory, redirect, url_for, jsonify
import os, time
from plugins import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from models import *
import json
from datetime import datetime, timedelta



@app.route('/', methods=['GET', 'POST'])
def user_login():
	error_check = 0
	session['auth'] = False
	u_id = None
	password = None
	
	if request.method == 'POST':
		u_id = request.form['inputUserID']
		passwd = encrypt_string(request.form['inputPassword'])
		userType = request.form['inputUserType']
		print(userType)
		if userType == "Patient":
			check_registered_user = db.session.query(Patient).filter(or_(Patient.u_name == u_id, Patient.mobile_no == u_id), Patient.password == passwd).first()
		else:
			check_registered_user = db.session.query(Doctor).filter(or_(Doctor.u_name == u_id, Doctor.mobile_no == u_id), Doctor.password == passwd).first()
		
		if check_registered_user is None:
			error_check = 1
		else:
			check_registered_user = eval(str(check_registered_user))
			if userType == "Patient":
				u_id, f_name, l_name, mobile_no, status  = check_registered_user.values()
			else:
				u_id, f_name, l_name, mobile_no, medication_type, status  = check_registered_user.values()
			
			session['auth'] = True
			session['u_id'] = u_id
			session['f_name'] = f_name
			session['l_name'] = l_name

			if userType == "Patient":
				session['u_type'] = "patient"
				return redirect("/patient_dashboard")
			else:
				session['u_type'] = "doctor"
				return redirect("/doctor_dashboard")

	return render_template('user_login/user_login.html', err_chk = error_check)


@app.route('/doctor_dashboard', methods=['GET', 'POST'])
def doctor_dashboard():
	combined_data = list()
	time_data = db.session.query(Timetable).filter(Timetable.doctor_id == session["u_id"], Timetable.status == False).all()

	for idx, each_data in enumerate(time_data):
		patient_data = db.session.query(Patient).filter(Patient.u_id == each_data.patient_id).first()
		new_data = {
			"u_id" : each_data.u_id,
			"f_name":patient_data.f_name, 
			"l_name":patient_data.l_name, 
			"mobile_no":patient_data.mobile_no, 
			"schedule_date":each_data.schedule_date,
			"start_time_slot":each_data.start_time_slot,
			"end_time_slot":each_data.end_time_slot,
			"prescription": each_data.prescription
		}
		combined_data.append(new_data)

	return render_template('doctor_dashboard/doctor_dashboard.html', combined_data=combined_data)

@app.route('/patient_dashboard', methods=['GET', 'POST'])
def patient_dashboard():
	combined_data = list()

	time_data = db.session.query(Timetable).filter(Timetable.patient_id == session["u_id"]).all()
	for idx, each_data in enumerate(time_data):
		doctor_data = db.session.query(Doctor).filter(Doctor.u_id == each_data.doctor_id).first()
		new_data = {
			"u_id" : each_data.u_id,
			"f_name":doctor_data.f_name, 
			"l_name":doctor_data.l_name, 
			"mobile_no":doctor_data.mobile_no, 
			"schedule_date":each_data.schedule_date,
			"start_time_slot":each_data.start_time_slot,
			"end_time_slot":each_data.end_time_slot
		}
		combined_data.append(new_data)
	doctor_data = db.session.query(Doctor).filter(Doctor.status == True).all()
	return render_template('patient_dashboard/patient_dashboard.html', doctor_data=doctor_data, combined_data=combined_data)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
	error_check = 0
	session['auth'] = False
	u_id = None
	password = None
	
	if request.method == 'POST':
		u_name = request.form['inputUserID']
		password = request.form['inputPassword']
		check_registered_user = db.session.query(Admin).filter(and_(Admin.u_name == u_name, Admin.password == password)).first()
		
		if check_registered_user is None:
			error_check = 1
		else:
			check_registered_user = eval(str(check_registered_user))
			u_id, u_name, u_type = check_registered_user.values()
			session['auth'] = True
			session['u_id'] = u_id
			session['u_name'] = u_name
			session['u_type'] = u_type
			return redirect("/admin_dashboard")

	return render_template('admin_login/admin_login.html', err_chk = error_check)


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
	patient_data = db.session.query(Patient).all()
	doctor_data = db.session.query(Doctor).all()
	return render_template('admin_dashboard/admin_dashboard.html', patient_data=patient_data, doctor_data=doctor_data)

@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
	error_check = 0
	u_id = None
	f_name = None
	l_name = None
	mobile_no = None
	u_name = None
	password = None
	signature = None
	
	if request.method == 'POST':
		
		if (request.form['inputPassword'] == request.form['inputConfPassword']):
			u_id = uuid()
			f_name = request.form['inputFname']
			l_name = request.form['inputLname']
			mobile_no = request.form['inputMobile']
			u_name = request.form['inputUserName']
			password = encrypt_string(request.form['inputPassword'])
			signature = encrypt_string(str(u_name) + str(mobile_no))

			if session['u_type'] == "admin":
				medication_type = request.form['inputMedicationType']
				if not db.session.query(Doctor).filter(Doctor.u_name == u_name).count() and not db.session.query(Doctor).filter(Doctor.mobile_no == mobile_no).count():
					reg = Doctor(u_id, f_name, l_name, mobile_no, medication_type, u_name, password, signature)
					db.session.add(reg)
					db.session.commit()
					return redirect("/admin_dashboard")
				else:
					error_check = 1
			else:
				if not db.session.query(Patient).filter(Patient.u_name == u_name).count() and not db.session.query(Patient).filter(Patient.mobile_no == mobile_no).count():
					reg = Patient(u_id, f_name, l_name, mobile_no, u_name, password, signature)
					db.session.add(reg)
					db.session.commit()
					return redirect('/')
				else:
					error_check = 1

	return render_template('user_registration/user_registration.html',  err_chk = error_check)

@app.route('/switch_status/<user_type>/<u_id>/<status>', methods=['GET', 'POST'])
def switch_status(user_type, u_id, status):
	print(user_type, u_id, status)
	if (session['u_type'] == "admin"):
		if user_type == "doctor":
			user = db.session.query(Doctor).filter(Doctor.u_id == u_id).first()
			user.status = True if status == "true" else False
			db.session.commit()
		elif user_type == "patient":
			user = db.session.query(Patient).filter(Patient.u_id == u_id).first()
			user.status = True if status == "true" else False
			db.session.commit()
	return redirect("/admin_dashboard")


@app.route('/schedule_duration/<u_id>', methods=['GET', 'POST'])
def schedule_duration(u_id):
	if (session['u_type'] == "doctor"):
		user = db.session.query(Doctor).filter(Doctor.u_id == u_id).first()
		if request.method == 'POST':
			u_id = user.u_id
			date, start_time, end_time = dict(request.form).values()
			FMT = '%H:%M'
			start_time = datetime.strptime(start_time, FMT)
			end_time = datetime.strptime(end_time, FMT)
			while True:
				if start_time >= end_time:
					break
				temp_end_time = start_time + timedelta(minutes = 15)
				s_id = uuid()
				reg = Timetable(s_id, u_id, datetime.strftime(start_time, FMT), datetime.strftime(temp_end_time, FMT), date)
				db.session.add(reg)
				db.session.commit()
				start_time = temp_end_time

			return redirect("/doctor_dashboard")
		
	return render_template('doctor_dashboard/doctor_schedule.html', doctor_id=u_id)


@app.route('/slot_booking/<method>/<u_id>', methods=['GET', 'POST'])
def slot_booking(method, u_id):
	if (session['u_type'] == "patient"):
		if method == "get_schedule":
			time_data = db.session.query(Timetable).filter(Timetable.doctor_id == u_id, Timetable.status == True).all()
		elif method == "book_schedule":
			time_data = db.session.query(Timetable).filter(Timetable.u_id == u_id).first()
			time_data.status = False
			time_data.patient_id = session["u_id"]
			db.session.commit()
			return redirect("/patient_dashboard")

	return render_template('patient_dashboard/slot_booking.html', time_data=time_data)


@app.route('/prescription/<method>/<u_id>', methods=['GET', 'POST'])
def prescription(method, u_id):
	
	time_data = db.session.query(Timetable).filter(Timetable.u_id == u_id).first()
	if method == "generate_prescription":
		if request.method == "POST":
			time_data.prescription = request.form["inputPrescription"]
			db.session.commit()
			return redirect("/doctor_dashboard")
	elif method == "get_prescription":
		return render_template('sys_prescription/sys_prescription.html', data=time_data.prescription, enable="1")

	return render_template('sys_prescription/sys_prescription.html', data=time_data.prescription)



@app.route('/logout')
def logout():
	session['auth'] = False
	session['u_type'] = ""
	return redirect('/')