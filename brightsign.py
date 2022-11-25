import requests
import json

class brightsign:
    _versions = {
        '8.5.31': 'https://bsncloud.s3.amazonaws.com/public/malibu-8.5.31-update.bsfw'
    }
    
    
    def __init__(self, player_ip: str):
        self.player_ip = player_ip
    
    def update(self, version: str = '8.5.31'):
        
        # check that passed version is in the versions dict
        try:
            self._versions[version]
        except KeyError:
            print(f'Invalid version passed! {version} is not in list of versions.')
            return
        
        
        # req_url is where api requests are made to the brightsign
        req_url = f'http://{self.player_ip}/api/v1'
        
        
        # check status of player
        try:
            # send health request to player and try to parse json for result
            res = requests.get(f'{req_url}/health')
            json_res = json.loads(res.text)
            status = json_res['data']['result']['status']
            
            # Log health
            with open('log', 'a') as file:
                file.write(f'{self.player_ip} Health: {status}\n')
            
        except KeyError as exc:
            # Log error
            with open('log', 'a') as file:
                file.write(f'(ERROR) {self.player_ip} : {res.status_code}\n')
                file.write(f'(ERROR) {exc} : Couldn\'t find version in json\n')
            print(f'KeyError: {exc}. Couldn\'t get the current version.')
            return
        
        # make sure the player isn't already up to date
        if version == self._check_version():
            print(f'{self.player_ip} already up to date')
            # Log UTD
            with open('log', 'a') as file:
                file.write(f'{self.player_ip} : Already up to date, aborting.\n')
            return


        # the endpoint to update firmware
        update_endpoint = f'/download-firmware?url={self._versions[version]}'

        print(f'Starting on {self.player_ip}')
        try:
            # Send request
            res = requests.get(f'{req_url}{update_endpoint}')
            # Try to log
            with open('log', 'a') as file:
                file.write(f'{self.player_ip} : {res.status_code}\n')
                file.write(f'{res.text}\n')
            
            print(f'Finished on {self.player_ip}, status {res.status_code}')
        except Exception as exc:
            print("Exception:", exc)
            # Log exception that occurred
            with open('log', 'a') as file:
                file.write(f'(ERROR) {self.player_ip}: {exc}\n')
            return


    def _check_version(self) -> str:
        req_url = f'http://{self.player_ip}/api/v1'
        # gets the current version of the brightsign
        try:
            # send info request
            res = requests.get(f'{req_url}/info')
            json_res = json.loads(res.text)
            version = json_res['data']['result']['FWVersion']

            # Log current version
            with open('log', 'a') as file:
                file.write(f'{self.player_ip} Current Version: {version}\n')
            
            return version

        except KeyError as exc:
            # Log error
            with open('log', 'a') as file:
                file.write(f'(ERROR) {self.player_ip} : {res.status_code}\n')
                file.write(
                    f'(ERROR) {exc} : Couldn\'t find status in json, player assumed not healthy\n')
            print(
                f'KeyError: {exc}. Player assumed not healthy, not attempting to update.')
            return
        except Exception as exc:
            # Log error
            with open('log', 'a') as file:
                file.write(f'(ERROR) {self.player_ip} : {res.status_code}\n')
                file.write(
                    f'(ERROR) {exc}: unexpected exception, not attempting to connect.\n')
            print(f'{exc} : Player assumed not healthy, not attempting to update.')
            return
