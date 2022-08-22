import time
import requests

hosts = [{ 'host': '<other host>', 'time_ran': 0}, { 'host': 'http://voice.webaverse.com/tts', 'time_ran': 0}]

for host in hosts:
    start = time.time()
    data = { 'voice': '1kpEjZ3YqMN3chKSXODOqayEm581rxj4r', 's': 'Hi there, how are you? What is your name?' }
    response = requests.get(host['host'], params=data)
    end = time.time()
    time_ran = end-start
    host['time_ran'] = time_ran

print(hosts)
