import requests, json, os
import robonomicsinterface as RI
from robonomicsinterface import Launch, Account


URL = "https://api.merklebot.com/spot-demo/process_command"
command_params = {"task_type":"code_execution", "code":open('spot_logic.py', 'r').read()}
res = requests.post(URL, params={'command_params': json.dumps(command_params)})
ipfs_hash = res.json()['IpfsHash']

account_with_seed = Account(os.environ.get('SEED'), remote_ws='wss://kusama.rpc.robonomics.network')
launch = Launch(account_with_seed)
print('running command with hash', ipfs_hash)
res = launch.launch('4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j', ipfs_hash)
print('created launch', res)
