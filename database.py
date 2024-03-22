import mysql.connector as sql

def convert_table(table2):

    for i in range(0,len(table2)):
        table2[i] = list(table2[i])

    for i in range(len(table2)):
        for j in range(len(table2[i])):
            if table2[i][j] is None:
                table2[i][j] = "-"
    

def connect_db():
    #DATABASE BAGLANMAK ICIN
    #GIRIS BILGILERINI KONTROL ET
    my_db = sql.connect(
        host="localhost",
        user="root",
        password="8ods3eg9"
    )

    
    if my_db:
        print('connected')

    cursor = my_db.cursor()
    cursor.execute('use cargo_company')
    cursor.fetchall()

    return my_db

def cargo_info(cargo_id:int, db):
    cursor = db.cursor()
    query = f"SELECT cargo_no, cargo_status, cargo_type, cargo_weight, s.c_full_name as sender,s.c_address as sender_adress ,r.c_full_name as receiver, r.c_address as receover_address\
    from cargo as c\
    join customer r on c.cargo_receiver_id = r.cus_id\
    join customer s on c.cargo_sender_id = s.cus_id \
    where cargo_no = {cargo_id};"
    cursor.execute(query)

    result = cursor.fetchall()
    
    return result


def cargo_tracking(cargo_id : int, db):
#Kargo takıp (DUZELTİLECEK!!!)
    table1 = cargo_info(cargo_id= cargo_id, db=db)

    cursor = db.cursor()
    query = f"SELECT l.log_no, l.log_date, l.action, b.district, d.dc_name FROM log AS l\
    JOIN employee AS e ON e.id = l.employee_id\
    LEFT JOIN dist_center AS d ON e.d_no = d.dc_no\
    LEFT JOIN branch AS b ON e.b_no = b.branch_no\
    WHERE {cargo_id} = l.cargo_id ORDER BY l.log_no asc;"
    cursor.execute(query)

    table2 = cursor.fetchall()
    
    return table1,table2

def get_customer_info(cust_id : int, db):
    #Seçili müşteri bilgilerini getiriyor  
    cursor = db.cursor()
    query = f"SELECT * FROM customer \
        WHERE {cust_id} = cus_id;"
    cursor.execute(query)
    result = cursor.fetchall()

    return result

def get_admin_customer_info(db):
    #Tüm müşteri bilgilerini getiriyor  
    cursor = db.cursor()
    query = f"SELECT * FROM customer;"

    cursor.execute(query)
    result = cursor.fetchall()

    return result

def get_employee_info(id : int,db):
#employee bilgilerini getiriyor(Employee girişinde kullanılacak)
    cursor = db.cursor()
    query = f"SELECT * FROM employee \
        WHERE {id} = id;"
    cursor.execute(query)

    result = cursor.fetchall()

    return result

def get_admin_employee_info(db):
#Tüm employee bilgilerini getiriyor(Admin girişinde kullanılacak)
    cursor = db.cursor()
    query = f"SELECT * FROM employee;"
    cursor.execute(query)

    result = cursor.fetchall()

    return result

def get_cargo_bill(cargo_id: int, db):
#Cargo id ile faturasini ceker

    cursor = db.cursor()
    query = f"SELECT * FROM bill\
        WHERE {cargo_id} = bill_cargo_id;"
    cursor.execute(query)

    result = cursor.fetchall()

    return result

def test(db):
    cursor = db.cursor()
    query = f"SELECT a.full_name, b.c_full_name from (select* from employee) as a, (select * from customer) as b ;"
    cursor.execute(query)

    result = cursor.fetchall()

    return result

def get_dist_center_info(db):
    #admin dist centerları listelemesi için
    cursor = db.cursor()
    query = f"Select * from dist_center;"
    cursor.execute(query)   

    result = cursor.fetchall()

    return result

def get_branch_info(db):
    #admin branchleri listelemesi için
    cursor = db.cursor()
    query = f"Select * from branch;"
    cursor.execute(query)   

    result = cursor.fetchall()

    return result

def add_dist_center(id,name,db):
    #Adding dist_center 
    cursor = db.cursor()
    query = f"INSERT INTO dist_center (dc_no, dc_name)\
    Values ({id},\"{name}\");"
   
    cursor.execute(query)       
    db.commit()
    
def add_branch(b_no,city,district,d_no,db):
    cursor = db.cursor()
    query = f"INSERT INTO branch (branch_no, city, district, dist_no)\
    Values ({b_no},\"{city}\",\"{district}\",\"{d_no}\");"
   
    cursor.execute(query)       
    db.commit()

def add_cargo(cargo_no,cargo_type,cargo_weight,cargo_receiver_id,cargo_sender_id,e_id,db):
    cursor = db.cursor()
    query = f"INSERT INTO cargo (cargo_no,cargo_type,cargo_weight,cargo_receiver_id,cargo_sender_id)\
    VALUES ({cargo_no},\"{cargo_type}\",{cargo_weight},{cargo_receiver_id},{cargo_sender_id});"
   
    cursor.execute(query)       
    db.commit()

    add_log("Branch Received",cargo_no,e_id,db)

def add_customer(id, full_name, phone, c_address, db):
    cursor = db.cursor()
    query = f"INSERT INTO customer (cus_id, c_full_name, c_phone_number, c_address)\
        VALUES({id},\"{full_name}\",\"{phone}\", \"{c_address}\");"
    
    cursor.execute(query)
    db.commit()

def add_bill(price, cargo_id, sender_id,db):
    cursor = db.cursor()
    query = f"INSERT INTO bill(bill_date, bill_price, bill_cargo_id, bill_sender_id)\
        VALUES(NOW(),{price},{cargo_id},{sender_id});"
    
    cursor.execute(query)       
    db.commit()

def add_log(action,cargo_id,employee_id,db):
    cursor = db.cursor()
    query = f"INSERT INTO log(action, log_date, cargo_id, employee_id)\
        VALUES(\"{action}\",NOW(),{cargo_id},{employee_id})"

    cursor.execute(query)       
    db.commit()

def add_dc_employee (id,full_name,d_no,db):
    cursor = db.cursor()
    query = f"Insert INTO employee(id,full_name,d_no)\
        VALUES({id},\"{full_name}\",{d_no});"

    cursor.execute(query)       
    db.commit()
    add_staff(id,db)
    
def add_branch_staff(id,full_name,b_no,db):
    cursor = db.cursor()
    query = f"Insert INTO employee(id,full_name,b_no)\
        VALUES({id},\"{full_name}\",{b_no});"

    cursor.execute(query)       
    db.commit()

    add_staff(id,db)

def add_branch_courier(id,full_name,b_no,db):
    cursor = db.cursor()
    query = f"Insert INTO employee(id,full_name,b_no)\
        VALUES({id},\"{full_name}\",{b_no});"

    cursor.execute(query)       
    db.commit()
    add_courier(id,db)
    
def add_staff(id,db):
    cursor = db.cursor()
    query = f"INSERT INTO staff(s_id)\
        VALUES({id});"
    cursor.execute(query)
    db.commit()
    
def add_courier(id,db):
    cursor = db.cursor()
    query = f"INSERT INTO courier(c_id)\
        VALUES({id});"
    
    cursor.execute(query)       
    db.commit()

def make_delivered(cargo_no,courier,db):
    add_log("Delivered",cargo_id=cargo_no,employee_id=courier,db=db)
    cursor = db.cursor()
    query = f"UPDATE cargo\
        SET cargo_courier_id = {courier}\
        WHERE cargo_no = {cargo_no};"
    cursor.execute(query)
    db.commit()

def get_cargo_history(cust_id,db):
    table1 = get_customer_info(cust_id,db)
    
    cursor = db.cursor()
    query = f"Select * from cargo\
        where cargo_sender_id = {cust_id} or cargo_receiver_id = {cust_id}"
    cursor.execute(query)
    table2=cursor.fetchall()

    return table1,table2

    
def main():
    my_db = connect_db()

    table1, table2 = cargo_tracking(3,my_db)
    
    for i in range(0,len(table2)):
        table2[i] = list(table2[i])

    

    for i in range(len(table2)):
        for j in range(len(table2[i])):
            if table2[i][j] is None:
                table2[i][j] = "-"

    # Print the types of elements in the first row
    #print(table2[len(table2)-1][1])
    convert_table(table1)
    print(table1[1])
    
    
    
   
if __name__ == '__main__':
    main()




    