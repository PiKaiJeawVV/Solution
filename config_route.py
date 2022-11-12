from paramiko import SSHClient
from paramiko import AutoAddPolicy
import mysql.connector
import time

db_cacti = mysql.connector.connect(host="10.1.0.50",user="admin",password="1qaz2wsx",database="automation")
exec_command = db_cacti.cursor()


def fetch_db():
    exec_command.execute(f"select * from automation_ros_host where status='000';")
    id_list = []
    ip_list = []
    status_list = []
    for firsh_fetch in exec_command:
        get_id = firsh_fetch[0]
        get_ip = firsh_fetch[2]
        get_status = firsh_fetch[4]
        id_list.append(get_id)
        ip_list.append(get_ip)
        status_list.append(get_status)
    return id_list,ip_list,status_list

def config_route(_gethost,_getip,_getmask,_getgate):
    ip = _gethost
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, port=22,username='admin',password='1qaz2wsx',timeout=0.2)
    stdin,stdout,stderr = client.exec_command(f"ip route add dst-address={_getip}{_getmask} gateway={_getgate}")
    time.sleep(0.5)
    client.close()


if __name__ == "__main__":
    query = fetch_db()
    get_ip = query[1]
    _ip = input("Ex. 100.64.111.0\nPlease input IP :")
    _mask = input("Ex. /24,/26\nPlease input mask :")
    _gateway = input("Please input gateway :")
    for host_ip in get_ip:
        try:
            config_route(host_ip,_ip,_mask,_gateway)
            print(host_ip,"Add already")
        except:
            print(host_ip,"Can't Add")
            pass
    db_cacti.close()