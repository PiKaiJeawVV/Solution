import mysql.connector

def _delete_rec_django():
    connect_db = mysql.connector.connect(host="172.18.0.2",user="root",password="benz4466",database="django_db")
    db_python = connect_db.cursor()
    db_python.execute(f"delete from automation_log where datetime < now() - interval 30 DAY;")
    db_python.execute(f"delete from still_problem where datetime < now() - interval 30 DAY;")
    db_python.execute(f"delete from finish_log where datetime < now() - interval 30 DAY;")
    connect_db.commit()
    connect_db.close()

def _delete_rec_cacti():
    db_cacti = mysql.connector.connect(host="127.0.0.1",user="admin",password="1qaz2wsx",database="automation")
    exec_command = db_cacti.cursor()
    exec_command.execute(f"delete from line_notify where update_time < now() - interval 30 DAY;")
    #exec_command.execute(f"delete from device_down where update_time < now() - interval 30 DAY;")
    #exec_command.execute(f"delete from automation_log where update_time < now() - interval 30 DAY;")
    db_cacti.commit()
    db_cacti.close()

def _delete_rec_snmptt():
    connect_db = mysql.connector.connect(host="10.1.0.27",user="admin",password="1qaz2wsx",database="snmptt")
    db_python = connect_db.cursor(f"delete from snmptt where update_time < now() - interval 30 DAY;")
    db_python = connect_db.cursor(f"delete from snmptt_unknown where update_time < now() - interval 30 DAY;")
    db_python.execute()
    db_python.close()


if __name__ == "__main__":
    _delete_rec_django()
    _delete_rec_cacti()
    _delete_rec_snmptt()