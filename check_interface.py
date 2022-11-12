import mysql.connector
import time
import subprocess
import re


t1 = time.time()

object_1 = r"(10.)"

db_cacti = mysql.connector.connect(host="127.0.0.1",user="admin",password="1qaz2wsx",database="automation")
get_host = db_cacti.cursor()

db_automation = mysql.connector.connect(host="127.0.0.1",user="admin",password="1qaz2wsx",database="automation")
exec_command = db_automation.cursor()

def insert_db(host,port,speed):
    exec_command.execute(f"insert into line_notify (display,host_ip,message,update_time) values ('Switch','{host}','Interface : {port} {speed}',now());")
    db_automation.commit()

def _get_host():
    get_host.execute(f"select * from hostCacti where code = '001';")
    host_list = []
    online_list = []
    code_list = []
    for firsh_fetch in get_host:
        host = firsh_fetch[1]
        online = firsh_fetch[4]
        code = firsh_fetch[5]
        host_list.append(host)
        online_list.append(online)
        code_list.append(code)
    return host_list,online_list,code_list

def finish(inp):
    for host in inp:
        if re.match(object_1, host):
            #print(host)
            total = subprocess.run(f"snmpget -v2c -c htvnms -Oqv {host} .1.3.6.1.2.1.2.1.0 -On",shell=True,stdout=subprocess.PIPE,encoding='utf-8')
            total_remove = total.stdout
            output1 = total_remove.strip()
            re_type = int(output1)
            for state in range(1,re_type + 1):
                #print(state)
                check_state_port = subprocess.run(f"snmpget -v2c -c htvnms -Oqv {host} .1.3.6.1.2.1.2.2.1.8.{state} -On",shell=True,stdout=subprocess.PIPE,encoding='utf-8')
                state_remove = check_state_port.stdout
                output2 = state_remove.strip()
                if output2 != 'down':    
                    check_speed_port = subprocess.run(f"snmpget -v2c -c htvnms -Oqv {host} .1.3.6.1.2.1.2.2.1.5.{state} -On",shell=True,stdout=subprocess.PIPE,encoding='utf-8')
                    speed_remove = check_speed_port.stdout
                    output3 = speed_remove.strip()
                    if output3 == '100000000':
                        speed = '100M'
                        print(f"{host} : {state} 100M")
                        insert_db(host,state,speed)
                    else:
                        pass
                else:
                    pass

display = _get_host()
result1 = display[0]
result2 = display[1]
result3 = display[2]
for x,y,z in zip(result1,result2,result3):
    print(x,y,z)
finish(result1)
t2 = time.time() - t1
print(f"{t2:0.2f}")
db_cacti.close()
db_automation.close()

# Total Interface = .1.3.6.1.2.1.2.1.0
# Check Brand = .1.3.6.1.2.1.1.1.0
# Check State = .1.3.6.1.2.1.2.2.1.8.(Num)
# Check Speed = .1.3.6.1.2.1.2.2.1.5.(Num)