from requests import get as requestsGet, exceptions as requestsExec
from json import loads as jsonLoads, decoder as jsonDecoder
from datetime import datetime as dt
    
# specify is a bs object should log by default
LOG_DEFAULT = True

# specify the default update version
LATEST_VER = '8.5.31'

class brightsign:
    
    def __init__(self, player_ip: str, log_enable: bool = LOG_DEFAULT):
        self.log_enable = log_enable
        
        self.player_ip = player_ip
        self.req_url = f'http://{self.player_ip}/api/v1'
        # player info used to get correct update
        self.player_family = None
        self.version = None
        self.status = None
        
        self._getPlayerInfo()
        self._logInfo()
      
      
    def _logInfo(self) -> None:
        # log the info gathered from a player.
        self._log(f'INFO: (family: {self.player_family}, status: {self.status}, version: {self.version})')
    
    
    def _log(self, msg: str) -> None:
        # log/print the log msg 
        time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f'{time}> {(self.player_ip)} {msg}'
        print(log_msg)
        
        # only write log if option is enabled
        if self.log_enable:
            with open('log', 'a') as file:
                file.write(log_msg + '\n')

        
    def _getPlayerInfo(self) -> None:
        # checks status, version, and family of brightsign
        try:
            # send health request to player and try to parse json for result
            health_res = requestsGet(f'{self.req_url}/health')
            json_res = jsonLoads(health_res.text)
            self.status = json_res['data']['result']['status']

        except KeyError as exc:
            # Log error
            self._log(f'Error: {health_res.status_code}')
            self._log(f'Error: {exc}; Couldn\'t find health in json')
            self._log(json_res)
            return
        except requestsExec.ConnectionError as exc:
            self._log(f'Error connecting to player at {self.player_ip}: {exc}')
            return
        except jsonDecoder.JSONDecodeError as exc:
            # Log error
            # This error could be caused by a password protected player
            self._log(f'Error: {health_res.status_code}')
            self._log(f'Error decoding JSON: {exc}')
            return
        
        try:
            # send version request to player and try to parse json for result
            health_res = requestsGet(f'{self.req_url}/info')
            json_res = jsonLoads(health_res.text)
            self.player_family = json_res['data']['result']['family']
            self.version = json_res['data']['result']['FWVersion']

        except KeyError as exc:
            # Log error
            self._log(f'Error: {health_res.status_code}')
            self._log(f'Error: {exc}; Couldn\'t find a key in json')
            self._log(json_res)
            return
    
    
    def update(self, version: str = LATEST_VER):
        # check health before trying to do anything
        if self.status != 'active':
            # stop if player is inactive
            self._log(f'Not attempting to update, status is not active ({self.status})')
            return
        
        # make sure the player isn't already up to date
        if version == self.version:
            # Log already UTD
            self._log(f'Player already up-to-data, version {self.version}')
            return

        # the endpoint to update firmware
        # this does require that they stick to their standard naming scheme every update
        update_endpoint = f'/download-firmware?url=https://bsncloud.s3.amazonaws.com/public/{self.player_family}-{self.latest_ver}-update.bsfw'

        self._log(f'Attempting update to {version}')
        try:
            # Send request
            res = requestsGet(f'{self.req_url}{update_endpoint}')
            # Try to log and check if update worked
            res_text = res.text
            update_status_code = res.status_code
            res.close()
            
            # parse response text
            update_status_code = res.status_code
            json_update = jsonLoads(res_text)
            update_status = json_update['data']['result']
            
            self._log(f'Finished, request status: ({update_status_code}), update status: ({update_status})')
        
        except KeyError as exc:
            # log key error
            self._log(f'Error: {exc}; possibly problem reading json.')
            self._log('INFO: response json: {res_text}')
        except Exception as exc:
            # Log exception that occurred
            self._log(f'Error: {exc}')
            return
    
