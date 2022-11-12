import shutil
import subprocess
import requests

hostname = subprocess.run("hostname",shell=True,stdout=subprocess.PIPE,encoding='utf-8')
hostname_onlyname = hostname.stdout

url = 'https://notify-api.line.me/api/notify'
token = 'xoQZ0Qaq5e0lf4eFraNNs7bOVwOioE9YyNNq8zqBLjw' #<-- Token line
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}


path = "/home/"
total, used, free = shutil.disk_usage(path)
total_gb = total // (2**30)
used_gb = used // (2**30)
free_gb = free // (2**30)

print(total_gb)
print(used_gb)
print(free_gb)

massge = (f"\nServer : {hostname_onlyname}\nTaotal Disk : {total_gb} GB\nDisk Using : /home/ {used_gb} GB")

if used_gb >= 150:
    requests.post(url, headers=headers, data = {'message':massge})
