import os
from subprocess import Popen, TimeoutExpired
import argparse
from time import sleep
import json

curdir = os.getcwd()
#curdir = os.getcwd().split('gpu')[0]
#curdir = f'{curdir}/source/libfabric/fabtests/scripts/feature_coverage'

def read_file(file_name):
    with open(file_name, 'r+') as file_out:
        output = file_out.read()
    return output

class ClientServerTest:
    def __init__(self, server_cmd, client_cmd, log_file):
        self.server_cmd = server_cmd
        self.client_cmd = client_cmd
        self.log_file = log_file
        self.server_log = f'server_log'
        self.client_log = f'client_log'
        self._timeout = 300

    def run(self):
        server_process = Popen(
            f"{self.server_cmd} > {self.server_log} 2>&1",
            shell=True, close_fds=True 
            )

        sleep(1)
        if self.client_cmd:
            client_process = Popen(
                f"{self.client_cmd} > {self.client_log} 2>&1",
                shell=True, close_fds=True
                )

        try:
            server_process.wait(timeout=self._timeout)
        except TimeoutExpired:
            server_process.terminate()
        if self.client_cmd:
            try:
                client_process.wait(timeout=self._timeout)
            except TimeoutExpired:
                client_process.terminate()

        server_output = read_file(self.server_log)
        if (f'{self.client_cmd}' != 'None'):
            client_output = read_file(self.client_log)
        with open(self.log_file, 'a+') as fp:
            fp.write(server_output)
            if (f'{self.client_cmd}' != 'None'):
                fp.write(client_output)

        if (f'{self.client_cmd}' != 'None'):
            print (server_process.returncode, client_process.returncode)
            return (server_process.returncode, client_process.returncode)
        else:
            print (server_process.returncode)
            return (server_process.returncode)

def parse_log(provider, log_file):
    base_list = []
    feature_list = []
    temp_list = []
    iterator = len(base_list)

    with open(log_file, 'r') as log:
        for line in log:
            if (('libfabric' not in line) and (':' in line) \
                and ('Address' not in line) and ('ret' not in line)):
                base_list.append(line.strip())

    for element in base_list:
        if 'fi_' in element:
            if (len(temp_list)!=0):
                new_temp_list = list(temp_list)
                feature_list.append(new_temp_list)
            temp_list.clear()
            temp_list.append(element)
            iterator = iterator - 1
        else:
            temp_list.append(element)
            iterator = iterator - 1
            if iterator==1:
                feature_list.append(temp_list)

    with open(f"{curdir}/feature_coverage_logs/{provider}/{log_file}_feature_list", 'w') \
            as fp:
        json.dump(feature_list, fp, indent=2)

    return 0

def cleanup(server_log, client_log, log_file):
    files = [server_log, client_log, log_file]
    for each_file in files:
        if (os.path.exists(f"{curdir}/{each_file}")):
            os.remove(f"{curdir}/{each_file}")
    return 0

if __name__ == "__main__":
    os.environ['FI_HOOK'] = 'trace'
    os.environ['FI_LOG_LEVEL'] = 'trace'
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server_cmd', type=str,
                        help='server command for the test. type:str')
    parser.add_argument('-c', '--client_cmd', type=str,
                        help='client command for the test. type:str')
    parser.add_argument('-p', '--provider', type=str,
                        help='provider type. type:str')

    args = parser.parse_args()
    server_cmd = args.server_cmd
    client_cmd = args.client_cmd
    provider = args.provider
    print("server_cmd: "f"{server_cmd}")
    print("client_cmd: "f"{client_cmd}")

    log = (server_cmd.split("/")[-1:])[0].split(" ")
    log_file = ("_").join([item for item in log if not ((item.isdigit() \
                            or item[0] == '-' and item[1:].isdigit()) \
                            or '-' in item)])

    err = ClientServerTest(server_cmd, client_cmd, log_file).run()
    if err!=(0, 0) or err!=(0):
        print("TEST COMPLETED")
    else:
        print(f"Exit CST with error: {err}")
        exit

    err = parse_log(provider, log_file)
    if err != 0:
        print(f"Exit PL with error: {err}")
        exit

    #cleanup('server_log', 'client_log', log_file)
    exit
