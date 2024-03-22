CREATE DATABASE cargo_company;

CREATE TABLE dist_center(
dc_no int PRIMARY KEY auto_increment NOT NULL,
name varchar(100) NOT NULL 
);

CREATE TABLE branch(
branch_no int PRIMARY KEY auto_increment NOT NULL,
city varchar(50),
district nvarchar(50),
dist_no int NOT NULL, 
FOREIGN KEY(dist_no) REFERENCES dist_center (dc_no) 
);

CREATE TABLE employee(
id int PRIMARY KEY NOT NULL,
full_name varchar(200) NOT NULL,
d_no int, 
b_no int,
FOREIGN KEY(d_no) REFERENCES dist_center (dc_no),
FOREIGN KEY(b_no) REFERENCES branch (branch_no)  
);

CREATE TABLE courier(
c_id int NOT NULL REFERENCES employee(id),
PRIMARY KEY (c_id)
);

CREATE TABLE staff(
s_id int NOT NULL REFERENCES employee(id),
PRIMARY KEY (s_id)
);

CREATE TABLE customer(
cus_id int PRIMARY KEY NOT NULL,
c_full_name varchar(200) NOT NULL,
c_phone_number char(11) NOT NULL,
c_address varchar(300) NOT NULL
);

CREATE TABLE sender(
sender_id int NOT NULL REFERENCES customer(cus_id),
PRIMARY KEY (sender_id)
);

CREATE TABLE receiver(
receiver_id int NOT NULL REFERENCES customer(cus_id),
PRIMARY KEY (receiver_id)
);

CREATE TABLE cargo(
cargo_no int PRIMARY KEY NOT NULL auto_increment,
cargo_status varchar(100),
cargo_type varchar(50),
cargo_weight int,
cargo_sender_id int NOT NULL, 
cargo_receiver_id int NOT NULL,
cargo_courier_id int,
FOREIGN KEY(cargo_sender_id) REFERENCES sender (sender_id),
FOREIGN KEY(cargo_receiver_id) REFERENCES receiver (receiver_id),
FOREIGN KEY(cargo_courier_id) REFERENCES courier(c_id)
);

CREATE TABLE log (
    log_no int NOT NULL AUTO_INCREMENT,
    action varchar(100) NOT NULL,
    log_date datetime NOT NULL,
    cargo_id int NOT NULL REFERENCES cargo(cargo_no),
	PRIMARY KEY (log_no,cargo_id), 
    CONSTRAINT status_check CHECK (action IN ("Branch Received", "In Transport", "In Distribution", "Delivered"))
);

CREATE TABLE bill(
bill_id int PRIMARY KEY NOT NULL auto_increment,
bill_date datetime NOT NULL,
bill_price DECIMAL(10,2) NOT NULL,
bill_cargo_id int,
bill_sender_id int,
FOREIGN KEY (bill_cargo_id) REFERENCES cargo(cargo_no),
FOREIGN KEY (bill_sender_id) REFERENCES sender(sender_id)
);

INSERT INTO dist_center (dc_no, name)
Values (34, 'Istanbul'),(06,'Ankara'),(35,'İzmir'),(16,'Bursa'),(60,'Tokat');

Insert into branch (branch_no, city, district, dist_no)
values (34001,'Istanbul','Sarıyer',34),(06001,'Ankara','Mamak',06),(35001,'Izmir','Karsıyaka',35),(16001,'Bursa','Mustafakemalpasa',16),(60001,'Tokat','Niksar',60);

Insert into employee (id,full_name,b_no)
values (001,'Kadir Tuna Hasırcı',34001);

Insert into customer(cus_id,c_full_name,c_phone_number,c_address)
values (2,'Ali Özgün', 00055511133,'Başakşehir');

DELIMITER //

CREATE TRIGGER add_customer_to_sender_receiver
AFTER INSERT ON customer
FOR EACH ROW
BEGIN
    -- Insert the new customer into the sender table
    INSERT INTO sender (sender_id) VALUES (NEW.cus_id);

    -- Insert the new customer into the receiver table
    INSERT INTO receiver (receiver_id) VALUES (NEW.cus_id);
END //

DELIMITER ;

Insert into cargo(cargo_type, cargo_weight, cargo_sender_id, cargo_receiver_id)
values ('Fragile', 2, 1,2);

select * from cargo;

Insert into log (action,log_date,cargo_id)
values ("Delivered", NOW(),3);

DELIMITER //

CREATE TRIGGER reset_log_no_and_update_status
BEFORE INSERT ON log
FOR EACH ROW
BEGIN
    DECLARE next_log_no INT;
    
    -- Find the maximum log_no for the current cargo
    SELECT COALESCE(MAX(log_no), 0) + 1 INTO next_log_no
    FROM log
    WHERE cargo_id = NEW.cargo_id;
    
    -- Set the log_no for the new record
    SET NEW.log_no = next_log_no;

    -- Update cargo status based on the new log action
    UPDATE cargo
    SET cargo_status = NEW.action
	WHERE cargo_no = NEW.cargo_id;
	END //

	DELIMITER ;

ALTER TABLE log
add employee_id int;

Alter table log 
ADD FOREIGN key (employee_id) REFERENCES employee(id);