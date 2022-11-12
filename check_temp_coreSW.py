import mysql.connector
import time
import datetime
import subprocess

db_cacti = mysql.connector.connect(host="127.0.0.1",user="admin",password="1qaz2wsx",database="automation")
exec_command = db_cacti.cursor()

timestr = datetime.datetime.now()
date = timestr.strftime("%d-%m-%Y")
time_now = timestr.strftime("%X")
time_stamp = date + " " + time_now
create_file = "output_" + time_stamp + ".txt"

def temperature():
    value_raw = subprocess.run(f"snmpwalk -c htvnms -v2c -Oqv 10.0.0.254 1.3.6.1.4.1.9.9.13.1.3.1.3",shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    value = value_raw.stdout
    return value.strip()

def insert_tables_line(_get):
    exec_command.execute(f"insert into line_notify (display,host_ip,code,message,update_time) values ('CoreSW','10.0.0.254','Temperature','{_get}',now());")
    db_cacti.commit()

if __name__ == "__main__":
    value_int = int(temperature())
    if value_int >= 41:
        print(f"Temperature too hight !!!")
        insert_tables_line(value_int)
    else:
        pass
    print(f"Temperature {value_int} {time_stamp}")
    db_cacti.close()