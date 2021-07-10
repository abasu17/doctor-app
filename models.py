from app import *

# Create database model
class Admin(db.Model):
	__tablename__ = 'sys_admin'
	
	u_id = db.Column(db.String(32), primary_key=True)
	u_name = db.Column(db.String(25))
	password = db.Column(db.String(64))
	u_type = db.Column(db.String(25))
	status = db.Column(db.Boolean())
	del_flag = db.Column(db.Boolean())
	
	def __init__(self, u_id, u_name, password, u_type):
		self.u_id = u_id
		self.u_name = u_name
		self.password = password
		self.u_type = u_type
		self.status = True
		self.del_flag = False

	def __repr__(self):
		return str({
			"u_id" : self.u_id,
			"u_name" : self.u_name,
			"u_type" : self.u_type
			})


# Create database model
class Patient(db.Model):
	__tablename__ = 'usr_patient'
	u_id = db.Column(db.String(32), primary_key=True)
	f_name = db.Column(db.String(25))
	l_name = db.Column(db.String(25))
	mobile_no = db.Column(db.String(10))
	u_name = db.Column(db.String(25))
	password = db.Column(db.String(64))
	signature = db.Column(db.String(64))
	status = db.Column(db.Boolean())
	del_flag = db.Column(db.Boolean())
		
	def __init__(self, u_id, f_name, l_name, mobile_no, u_name, password, signature):
		self.u_id = u_id
		self.f_name = f_name
		self.l_name = l_name
		self.mobile_no = mobile_no
		self.u_name = u_name
		self.password = password
		self.signature = signature
		self.status = True
		self.del_flag = False

	def __repr__(self):
		return str({
			"u_id" : self.u_id,
			"f_name" : self.f_name,
			"l_name" : self.l_name,
			"mobile_no" : self.mobile_no,
			"status" : self.status
			})


class Doctor(db.Model):
	__tablename__ = 'usr_doctor'
	u_id = db.Column(db.String(32), primary_key=True)
	f_name = db.Column(db.String(25))
	l_name = db.Column(db.String(25))
	mobile_no = db.Column(db.String(10))
	medication_type = db.Column(db.String(25))
	u_name = db.Column(db.String(25))
	password = db.Column(db.String(64))
	signature = db.Column(db.String(64))
	status = db.Column(db.Boolean())
	del_flag = db.Column(db.Boolean())

	def __init__(self, u_id, f_name, l_name, mobile_no, medication_type, u_name, password, signature):
		self.u_id = u_id
		self.f_name = f_name
		self.l_name = l_name
		self.mobile_no = mobile_no
		self.medication_type = medication_type
		self.u_name = u_name
		self.password = password
		self.signature = signature
		self.status = True
		self.del_flag = False

	def __repr__(self):
		return str({
			"u_id" : self.u_id,
			"f_name" : self.f_name,
			"l_name" : self.l_name,
			"mobile_no" : self.mobile_no,
			"medication_type" : self.medication_type,
			"status" : self.status
			})


class Timetable(db.Model):
	__tablename__ = 'sys_timetable'
	u_id = db.Column(db.String(32), primary_key=True)
	doctor_id = db.Column(db.String(32))
	patient_id = db.Column(db.String(32))
	start_time_slot = db.Column(db.String(32))
	end_time_slot = db.Column(db.String(32))
	schedule_date = db.Column(db.String(32))
	prescription = db.Column(db.String(500))
	status = db.Column(db.Boolean())
	del_flag = db.Column(db.Boolean())

	def __init__(self, u_id, doctor_id, start_time_slot, end_time_slot, schedule_date):
		self.u_id = u_id
		self.doctor_id = doctor_id
		self.patient_id = None
		self.start_time_slot = start_time_slot
		self.end_time_slot = end_time_slot
		self.schedule_date = schedule_date
		self.prescription = None
		self.status = True
		self.del_flag = False

	def __repr__(self):
		return str({
			"u_id" : self.u_id,
			"doctor_id" : self.doctor_id,
			"patient_id" : self.patient_id,
			"start_time_slot" : self.start_time_slot,
			"end_time_slot" : self.end_time_slot,
			"schedule_date" : self.schedule_date,
			"status" : self.status,
			"prescription" : self.prescription
			})