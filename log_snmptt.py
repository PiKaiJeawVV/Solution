import mysql.connector
import time
import datetime
import requests

url = 'https://notify-api.line.me/api/notify'
token = 'xoQZ0Qaq5e0lf4eFraNNs7bOVwOioE9YyNNq8zqBLjw' #<-- Token line
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

t1 = time.time()
#----------------------------------------------------------------------------------------------
# Cacti Database
db_cacti = mysql.connector.connect(host="10.1.0.27",user="admin",password="1qaz2wsx",database="snmptt")
fetch_db = db_cacti.cursor()
# NMS2 Database
db_nms2 = mysql.connector.connect(host="192.168.71.29",user="admin",password="htvnms",database="htv",port=3306)
insert_db = db_nms2.cursor()

timenow = datetime.datetime.now()
date = timenow.strftime("%d-%m-%Y")
date_yf = timenow.strftime("%Y-%m-%d")
time_now = timenow.strftime("%X")
#For fetch Mysql snmptt
time_format_snmp = timenow.strftime("%a %b %-d %-H:%-M:")
#-----------------------------------------------------------------------------------------------------------------------------------------------#
time_stamp = date + " " + time_now

# Time for cal
time_day_text = timenow.strftime("%a")
time_month_text = timenow.strftime("%b")
time_day_number = timenow.strftime("%-d")
time_h = timenow.strftime("%-H")
time_m = timenow.strftime("%M")
time_s = timenow.strftime("%-S")
now_5min = datetime.datetime.now() - datetime.timedelta(minutes=5)
day_text = now_5min.strftime("%a")
month_text = now_5min.strftime("%b")
day_number = now_5min.strftime("%-d")
time_h_2 = now_5min.strftime("%H")
time_m_2 = now_5min.strftime("%M")
time_s_2 = now_5min.strftime("%-S")
m_int = int(time_m_2)
d_int = int(day_number)

#print(time_format_snmp)
#print(now_5min)
#print(day_text)
#print(month_text)
#print(day_number)
#print(time_h_2)
#print(time_m_2)
#print(type(m_int))
#print(time_s_2)

#------------------------------------------------------------------------------------------------------------------------------------------------#
def fetch_snmptt(day_convert,min_convert):
#def fetch_snmptt():
    fetch_db.execute(f"select * from snmptt where agentip='10.5.0.253' and traptime like '{day_text} {month_text} {day_convert} {time_h_2}:{min_convert}:%';")
    #fetch_db.execute(f"select * from snmptt where agentip='10.5.0.253' and traptime like 'Tue Jul 26 10:55:%';")
    print(fetch_db.statement) #<-- Output command to file
    ip_list = []            
    time_list = []
    formatime_list = []
    for firsh_fetch in fetch_db:
        get_ip = firsh_fetch[7]
        get_time = firsh_fetch[11]
        get_formatime_list = firsh_fetch[12]
        ip_list.append(get_ip)
        time_list.append(get_time)
        formatime_list.append(get_formatime_list)
    return ip_list,time_list,formatime_list

def insert_nms(state,time_state,port):
    insert_db.execute(f"insert into PushMessage (display, host_ip, code, cus_id, message, update_time, LineBot) values ('Huawei FiberSW','10.5.0.253', '{state}','{time_state}','interface {port}', now() ,'IT_Alarm');")
    db_nms2.commit()

def insert_linenotify(state,time_state,port):
    fetch_db.execute(f"insert into line_notify (display,host_ip,code,cus_id,message,update_time) values ('Huawei FiberSW','10.5.0.253','{state}','{time_state}','interface {port}', now());")
    db_cacti.commit()

def convert_day(convert):
    if convert == 1: change = ' 1'
    elif convert == 2: change = ' 2'
    elif convert == 3: change = ' 3'
    elif convert == 4: change = ' 4'
    elif convert == 5: change = ' 5'
    elif convert == 6: change = ' 6'
    elif convert == 7: change = ' 7'
    elif convert == 8: change = ' 8'
    elif convert == 9: change = ' 9'
    else:
        return convert
    return change

#print(d_int)
#print(type(d_int))
if __name__ == "__main__":
    for pro_time in range(0,5):
        m_int += 1
        #print(f'{m_int} {type(m_int)} เก่า')
        if m_int == 0: m_str = '00'
        elif m_int == 1: m_str = '01'
        elif m_int == 2: m_str = '02'
        elif m_int == 3: m_str = '03'
        elif m_int == 4: m_str = '04'
        elif m_int == 5: m_str = '05'
        elif m_int == 6: m_str = '06'
        elif m_int == 7: m_str = '07'
        elif m_int == 8: m_str = '08'
        elif m_int == 9: m_str = '09'
        
    #print(f'{m_str} {type(m_str)} ใหม่')
    #print(m_int)
#--------------------------------------------------------------#
        day_con = convert_day(d_int)
        if m_int > 0 and m_int < 10:
            fetch = fetch_snmptt(day_con,m_str)
        else:
            fetch = fetch_snmptt(day_con,m_int)
        #fetch = fetch_snmptt()
        ip = fetch[0]
        _time = fetch[1]
        _format = fetch[2]
        for txt,time_proc in zip(_format,_time):
            txt_to_splite = txt.split()
            status = txt_to_splite[1]
#--------------------------------------------------------------#
            step1 = txt_to_splite[4]
            step2 = step1.replace('.','')
            step3 = int(step2)
            interface = step3 - 6
#--------------------------------------------------------------#
            step_1 = time_proc.split()
            time_event = step_1[3]
            insert_nms(status,time_event,interface)
            #insert_linenotify(status,time_event,interface)
            print(status,time_event,interface)
            #print(fetch_db.statement) #<-- Output command to file
        t2 = time.time() - t1
    print(f"{t2:0.2f}",time_stamp)
db_cacti.close()
db_nms2.close()
