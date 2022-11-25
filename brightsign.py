import requests
import json
from datetime import datetime as dt


class brightsign:
    
    latest_ver = '8.5.31'
    
    def __init__(self, player_ip: str):
        self.player_ip = player_ip
        self.req_url = f'http://{self.player_ip}/api/v1'
        self.player_family = None
        self.version = None
        self.status = None
        self._getPlayerInfo()
        self._logInfo()
      
      
    def _logInfo(self) -> None:
        self._log(f'Info: (family: {self.player_family}, status: {self.status}, version: {self.version})')
    
    def _log(self, msg: str) -> None:
        
        with open('log', 'a') as file:
            time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write(f'{time}> {(self.player_ip)} {msg}\n')

        
    def _getPlayerInfo(self) -> None:
        # checks status, version, and family of brightsign
        try:
            # send health request to player and try to parse json for result
            health_res = requests.get(f'{self.req_url}/health')
            json_res = json.loads(health_res.text)
            self.status = json_res['data']['result']['status']

        except KeyError as exc:
            # Log error
            self._log(f'Error: {health_res.status_code}')
            self._log(f'Error: {exc}; Couldn\'t find health in json')
            self._log(json_res)
            return
        except requests.exceptions.ConnectionError as exc:
            self._log(f'Error connecting to player at {self.player_ip}: {exc}')
            return
        
        try:
            # send version request to player and try to parse json for result
            health_res = requests.get(f'{self.req_url}/info')
            json_res = json.loads(health_res.text)
            self.player_family = json_res['data']['result']['family']
            self.version = json_res['data']['result']['FWVersion']


        except KeyError as exc:
            # Log error
            self._log(f'Error: {health_res.status_code}')
            self._log(f'Error: {exc}; Couldn\'t find a key in json')
            self._log(json_res)
            return
    
    
    
    
    def update(self, version: str = latest_ver):
        # check health before trying to do anything
        if self.status != 'active':
            self._log(f'Not attempting to update, status is not active ({self.status})')
            print(
                f'{self.player_ip}: Not attempting to update, status is not active ({self.status})')
            return
        
        # make sure the player isn't already up to date
        if version == self.version:
            print(f'{self.player_ip} already up to date')
            # Log UTD
            self._log(f'Player already up-to-data, version {self.version}')
            return


        # the endpoint to update firmware
        update_endpoint = f'/download-firmware?url=https://bsncloud.s3.amazonaws.com/public/{self.player_family}-{self.latest_ver}-update.bsfw'

        print(f'Starting on {self.player_ip}')
        try:
            # Send request
            res = requests.get(f'{self.req_url}{update_endpoint}')
            # Try to log
            self._log(f'Request status ({res.status_code}) : {res.text}')
            res.close()
            
            print(f'{self.player_ip} completed.')
        except Exception as exc:
            print("Exception:", exc)
            # Log exception that occurred
            self._log(f'Error: {exc}')
            return


    