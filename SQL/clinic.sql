
create database clinic;
use clinic;
drop database clinic;


CREATE TABLE patient (
    patientID INT AUTO_INCREMENT PRIMARY KEY,
    patientName VARCHAR(32),
    patientPhoneNumber VARCHAR(16) UNIQUE
) AUTO_INCREMENT = 1;
create table staff (
    staffID int AUTO_INCREMENT primary key,
    staffName varchar(32),
    jobDescription varchar(32),
    salary double,
    staffPhoneNumber varchar(16) UNIQUE,
    workDays varchar(32),
    workingHours int,
    staffPassword varchar(32) unique
)AUTO_INCREMENT=1200000;

create table appointment(
	appointmentNumber int AUTO_INCREMENT primary key, 
    assignPatientID int,
    appointmentDate date,
    appointmentTime time,
    appointmentType varchar(32),
    designateStaffID int,
    foreign key (assignPatientID) references patient(patientID) ON DELETE CASCADE,
    foreign key (designateStaffID) references staff(staffID) ON DELETE CASCADE

)AUTO_INCREMENT = 1;

create table patientPayment(
	patientPaymentNumber int AUTO_INCREMENT primary key,
    patientPaymentDate date,
    amount double,
    patientPaymentType varchar(32),
    totalToPay double,
    collectStaffID int,
    PatientID int,
    foreign key (PatientID) references patient(patientID) on delete cascade,
    foreign key (collectStaffID) references staff(staffID) on delete cascade
)AUTO_INCREMENT = 1;
ALTER TABLE patientPayment
ADD COLUMN amountLeftToPay DOUBLE GENERATED ALWAYS AS (amount-totalToPay) STORED;


create table treatmentPlan(
	treatmentID int AUTO_INCREMENT primary key,
	diagnosis varchar(128),
    progress varchar(128),
    prescriptions varchar(32),
    treatmentName varchar(64),
    PatientID int,
    StaffID int,
    foreign key (PatientID) references patient(patientID) on delete cascade,
    foreign key (StaffID) references staff(staffID) on delete cascade
)AUTO_INCREMENT = 1;

create table laboratory (
	laboratoryID int AUTO_INCREMENT primary key,
	laboratoryPhoneNumber varchar(16) UNIQUE,
    laboratoryName varchar(64),
    exportType varchar(64),
    PatientID int,
    requestStaffID int,
	foreign key (PatientID) references patient(patientID) on delete cascade,
    foreign key (requestStaffID) references staff (staffID) on delete cascade
)AUTO_INCREMENT=1;

create table supplier(
	supplierID int AUTO_INCREMENT primary key,
	supplierPhoneNumber varchar(16) UNIQUE,
    companyName varchar(32)
)AUTO_INCREMENT=1;

create table equipment (
	equipmentID int AUTO_INCREMENT primary key,
    equipmentName varchar(64),
    maintenaceDate date,
    supplierID int,
    foreign key (supplierID) references supplier (supplierID) on delete cascade

)AUTO_INCREMENT=1;


create table clinicExpenses(
	clinicPaymentNumber int AUTO_INCREMENT primary key,
    expenses double,
    balance double,
    expensesStaffID int,
    foreign key (expensesStaffID) references staff (staffID) on delete cascade
)AUTO_INCREMENT = 1;



select * from laboratory ;
-- **************************************************************** 
create table appointmentPayment(
	appointmentNumber int,
	paymentPatientID int,
	patientPaymentNumber int,
	treatmentID int,
	primary key(appointmentNumber, paymentPatientID, patientPaymentNumber, treatmentID),
	foreign key (patientPaymentNumber) references patientPayment (patientPaymentNumber),
	foreign key (paymentPatientID) references patient (patientID),
	foreign key (appointmentNumber) references appointment (appointmentNumber),
	foreign key (treatmentID) references treatmentPlan (treatmentID)
);


create table treatPatient(
	patientID int,
	treatmentID int,
    treatStaffID int,
	primary key (patientID,treatmentID, treatStaffID),
	foreign key (patientID) references patient (patientID),
	foreign key (treatmentID) references treatmentPlan (treatmentID),
    foreign key (treatStaffID) references staff (staffID)
);

create table laboratoryExport(
	patientID int,
	laboratoryID int,
	primary key (patientID, laboratoryID),
	foreign key (patientID) references patient (patientID),
	foreign key (laboratoryID) references laboratory (laboratoryID)
);

create table constructTreatmentPlan(
	treatmentID int,
	staffID int,
	primary key (treatmentID, staffID),
	foreign key (treatmentID) references treatmentPlan (treatmentID),
	foreign key (staffID) references staff (staffID)
);

create table paymentContributeExpenses(
	patientPaymentNumber int,
	staffID int,
	primary key (patientPaymentNumber, staffID),
	foreign key (patientPaymentNumber) references patientPayment (patientPaymentNumber),
	foreign key (staffID) references staff (staffID)
);

create table payForEquipment(
	payClinicPaymentNumber int,
	equipmentID int,
    supplierID int,
	primary key (payClinicPaymentNumber, equipmentID, supplierID),
	foreign key (supplierID) references clinicExpenses (clinicPaymentNumber),
	foreign key (equipmentID) references equipment (equipmentID),
    foreign key (supplierID) references supplier (supplierID)
);

create table Maintain(
	equipmentID int,
	supplierID int ,
	primary key (equipmentID, supplierID),
	foreign key (equipmentID) references equipment (equipmentID),
	foreign key (supplierID) references supplier (supplierID)
);
INSERT INTO patient (patientName, patientPhoneNumber) VALUES
('John Doe', '0594567890'),
('Alice Johnson', '0596543210'),
('Bob Smith', '0591234567');

-- Insert dummy data into the staff table
INSERT INTO staff (staffName, jobDescription, salary, staffPhoneNumber, workDays, workingHours, staffPassword) VALUES
('Dr. Johnson', 'Dentist', 80000.00, '0597891234', 'Mon-Fri', 8, 'password123'),
('Nurse Smith', 'Nurse', 50000.00, '0599876543', 'Mon-Sat', 7, 'nursepass'),
('Receptionist Alice', 'Receptionist', 40000.00, '0591112222', 'Mon-Fri', 8, 'receptpass');

-- Insert dummy data into the appointment table
INSERT INTO appointment (assignPatientID, appointmentDate, appointmentTime, appointmentType, designateStaffID) VALUES
(1, '2024-01-25', '10:00:00', 'Checkup', 1200000),
(2, '2024-01-26', '11:30:00', 'Cleaning', 1200000),
(3, '2024-01-27', '14:00:00', 'X-ray', 1200002);

-- Insert dummy data into the patientPayment table
INSERT INTO patientPayment (patientPaymentDate, amount, patientPaymentType, totalToPay, collectStaffID, PatientID) VALUES
('2024-01-25', 100.00, 'Cash', 100.00, 1200000, 1),
('2024-01-26', 150.00, 'Credit Card', 150.00, 1200001, 2),
('2024-01-27', 200.00, 'Debit Card', 200.00, 1200002, 3);

-- Insert dummy data into the treatmentPlan table
INSERT INTO treatmentPlan (diagnosis, progress, prescriptions, treatmentName, PatientID, StaffID) VALUES
('Toothache', 'Improving', 'Painkillers', 'Checkup', 1, 1200002),
('Cavity', 'Stable', 'Fluoride Treatment', 'Cleaning', 2, 1200001),
('X-ray Analysis', 'Pending', 'None', 'X-ray', 3, 1200000);

-- Insert dummy data into the laboratory table
INSERT INTO laboratory (laboratoryPhoneNumber, laboratoryName, exportType, PatientID, requestStaffID) VALUES
('0594443333', 'Dental Lab', 'Digital', 1, 1200001),
('0592221111', 'X-ray Lab', 'Printed', 2, 1200002),
('0596669999', 'Analysis Lab', 'Digital', 3, 1200000);

-- Insert dummy data into the supplier table
INSERT INTO supplier (supplierPhoneNumber, companyName) VALUES
('059-555-0000', 'Dental Supplier'),
('059-999-8888', 'Lab Supplier');

-- Insert dummy data into the equipment table
INSERT INTO equipment (equipmentName, maintenaceDate, supplierID) VALUES
('Dental Chair', '2024-02-01', 1),
('X-ray Machine', '2024-03-15', 2);

-- Insert dummy data into the clinicExpenses table
INSERT INTO clinicExpenses (expenses, balance, expensesStaffID) VALUES
(500.00, 200.00, 1200002),
(300.00, 150.00, 1200001),
(200.00, 100.00, 1200000);
