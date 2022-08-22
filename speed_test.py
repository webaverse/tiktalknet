import time
import requests

hosts = [{ 'host': '<other host>', 'last_time_ran': 0, 'total_time_ran': 0, 'avatarage_time_ran': 0}, { 'host': 'http://voice.webaverse.com/tts', 'last_time_ran': 0, 'total_time_ran': 0, 'avatarage_time_ran': 0}]
i = 0
loops = 50

while i < loops:
    for host in hosts:
        start = time.time()
        data = { 'voice': '1kpEjZ3YqMN3chKSXODOqayEm581rxj4r', 's': 'Hi there, how are you? What is your name?' }
        response = requests.get(host['host'], params=data)
        end = time.time()
        time_ran = end-start
        host['last_time_ran'] = time_ran
        host['total_time_ran'] += time_ran
    i += 1

for host in hosts:
    host['avatarage_time_ran'] = host['total_time_ran'] / loops
    print('Host:', host['host'])
    print('Last time ran:', host['last_time_ran'])
    print('Total time ran:', host['total_time_ran'])
    print('Average time ran:', host['avatarage_time_ran'])
    print('----------------------------------------------------')
