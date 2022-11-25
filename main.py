import requests
import subprocess

# update_file is the name of the update file
update_file = 'brightsign-8.5.31-update.bsfw'
# current ip is the LAN ip of this device, will make this automatic later
current_ip = '192.168.1.241'
# player ip is the ip of the brightsign player
player_ip = '192.168.1.122'

# file_url represents where the player can download the update file from
fileurl = f'http://{current_ip}:8000/{update_file}'
# req_url is where the request is sent to on the brightsign
req_url = f'http://{player_ip}/api/v1/download-firmware?url={fileurl}'


# starts the http server
process = subprocess.Popen('python -m http.server', shell=True, stdout=subprocess.PIPE)


try:
    print(f'Starting on {player_ip}')
    
    # Send request
    res = requests.get(req_url)

    # Try to log
    with open('json.log', 'a') as file:
        file.write(f'{player_ip} : {res.status_code}\n')
        file.write(f'{res.text}\n')

    print(f'Finished on {player_ip}, status {res.status_code}')

except Exception as exc:
    print("Exception:", exc)
    # Log exception that occurred
    with open('json.log', 'a') as file:
        file.write(f'{player_ip} (ERROR): {exc}\n')

# kill http server
process.kill()
