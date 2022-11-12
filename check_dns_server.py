import mysql.connector
import datetime
import subprocess

db_cacti = mysql.connector.connect(host="127.0.0.1",user="admin",password="1qaz2wsx",database="automation")
exec_command = db_cacti.cursor()

re_check = r"(...)"

timestr = datetime.datetime.now()
date = timestr.strftime("%d-%m-%Y")
time_now = timestr.strftime("%X")
time_stamp = date + " " + time_now
create_file = "output_" + time_stamp + ".txt"

def insert_service_problem(_ip):
    exec_command.execute(f"insert into line_notify (display,host_ip,code,update_time) values ('DNS Server','{_ip}','Resovle fail',now());")
    db_cacti.commit()

def insert_tables_line(_ip):
    exec_command.execute(f"insert into line_notify (display,host_ip,code,update_time) values ('DNS Server','{_ip}','No response',now());")
    db_cacti.commit()

def bash_dns(_nember):
    try:
        value_raw = subprocess.run(f"/home/benz/python_engineer/project1/bash/nslookup_203_28_128_{_nember}.sh",shell=True,stdout=subprocess.PIPE,encoding='utf-8',timeout=0.5,)
        value = value_raw.stdout
        print(f"DNS {_nember} state : Working")
    except:
        pass
        insert_service_problem(_nember)
        print(f"DNS {_nember} state : Not Working")

def ping_dns(_get):
    state = subprocess.run(f"ping -c 1 203.28.128.{_get} > /dev/null 2>&1",shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    if state.returncode == 0:
        print(f"DNS {_get} Online")
        if _get == 1 or _get == 2:
            try:
                value_raw = subprocess.run(f"/home/benz/python_engineer/project1/bash/nslookup_203_28_128_{_get}.sh",shell=True,stdout=subprocess.PIPE,encoding='utf-8',timeout=0.5,)
                value = value_raw.stdout
                print(value)
                print(f"DNS {_get} state : Working")
            except:
                pass
                insert_service_problem(_get)
                print(f"DNS {_get} state : Not Working")
        else:
            pass
    else:
        print(f"DNS {_get} Offline")
        insert_tables_line(_get)
    


if __name__ == "__main__":
    print("---------------------")
    for orc in range(1,5):
        ping_dns(orc)

    db_cacti.close()
    print(time_stamp)
    print("---------------------")