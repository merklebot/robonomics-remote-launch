import os
from robonomicsinterface import Launch, Account
from pinata_python.pinning import Pinning

# Get account to listen, pinata jwt token and account seed from environmental variables
ROBONOMICS_LISTEN_ROBOT_ACCOUNT = os.environ.get("ROBONOMICS_LISTEN_ROBOT_ACCOUNT")
PINATA_JWT_TOKEN = os.environ.get('PINATA_JWT_TOKEN')
ACCOUNT_SEED = os.environ.get('SEED')

# connect to Pinata
pinata = Pinning(AUTH="jwt", PINATA_JWT_TOKEN=PINATA_JWT_TOKEN)

test_json = {"a": "b"}

# Pin Json with message to Pinata
resp = pinata.pin_json_to_ipfs(test_json)
ipfs_hash = resp["IpfsHash"]
print("Pinned IPFS Hash: ", ipfs_hash)

# Initialize account with seed
account_with_seed = Account(ACCOUNT_SEED, remote_ws='wss://kusama.rpc.robonomics.network')

# Create launcher and send launch event
launch = Launch(account_with_seed)
res = launch.launch(ROBONOMICS_LISTEN_ROBOT_ACCOUNT, ipfs_hash)
print('created launch', res)
