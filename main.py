import os
import robonomicsinterface as RI
import requests
import docker
client = docker.from_env()


ROBONOMICS_LISTEN_ROBOT_ACCOUNT = os.environ.get("ROBONOMICS_LISTEN_ROBOT_ACCOUNT",
                                                 "4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j")
IPFS_COMMAND_GATEWAY = os.getenv('IPFS_COMMAND_GATEWAY', 'https://merklebot.mypinata.cloud/ipfs')



def robonomics_transaction_callback(data, launch_event_id):
    sender, recipient, command_params_32_bytes = data
    command_params_ipfs_hash = RI.ipfs_32_bytes_to_qm_hash(command_params_32_bytes)
    task = requests.get(f'{IPFS_COMMAND_GATEWAY}/{command_params_ipfs_hash}').json()
    print('Got task from', sender)
    if task['task_type']=='code_execution':
        code = task['code']
        execute_code(code, launch_event_id)

def execute_code(code, launch_event_id):
    print('Starting container with code for launch', launch_event_id)
    output = start_container(code)

def launch_robonomics_subsciber():
    interface = RI.Account(remote_ws="wss://kusama.rpc.robonomics.network")
    print("Robonomics subscriber starting...")
    subscriber = RI.Subscriber(interface, RI.SubEvent.NewLaunch, robonomics_transaction_callback,
                               ROBONOMICS_LISTEN_ROBOT_ACCOUNT)


def build_image():
    try:
        image = client.images.get('code_executor:latest')
    except:
        print('Image not found. Building...')
        client.images.build(path='container', tag='code_executor')

def start_container(code):
    output = client.containers.run("code_executor-splines", f"python3.8 < {code}", detach=False, environment=open('envs.txt', 'r').read().split('\n'))
    print('Code executed')
    print('Output:\n___________')
    print(output)
    print('___________')
    return output

def main():
    print('Getting image...')
    build_image()
    launch_robonomics_subsciber()
if __name__=='__main__':
    main()

