import os
import argparse

prov_list = ['tcp', 'udp']

def create_dir():
	curdir = os.getcwd()
	#curdir = os.getcwd().split('gpu')[0]
	#curdir = f'{curdir}/source/libfabric/fabtests/scripts/feature_coverage'
	#prov_list = ['tcp','udp','verbs', 'psm3', 'shm']
	if not os.path.exists(f"{curdir}/feature_coverage_logs"):
		os.mkdir(f"{curdir}/feature_coverage_logs")
	for provider in prov_list:
		if not os.path.exists(f"{curdir}/feature_coverage_logs/{provider}"):
			os.mkdir(f"{curdir}/feature_coverage_logs/{provider}")
	return 0

unit_tests = [
    #"fi_getinfo_test -s SERVER_ADDR GOOD_ADDR",
	"fi_av_test -g 192.168.1.2 -n 1 -s 192.168.1.2 -e rdm",
	"fi_av_test -g 192.168.1.2 -n 1 -s 192.168.1.2 -e dgram",
	#"fi_dom_test -n 2",
	#"fi_eq_test",
	"fi_cq_test",
	#"fi_setopt_test",
	"fi_mr_test"
]

functional_tests = [
    "fi_av_xfer -e rdm",
	"fi_av_xfer -e dgram",
	"fi_cm_data",
	"fi_cq_data -e msg -o senddata",
	"fi_cq_data -e rdm -o senddata",
	"fi_cq_data -e dgram -o senddata",
	"fi_cq_data -e msg -o writedata",
	"fi_cq_data -e rdm -o writedata",
	"fi_cq_data -e dgram -o writedata",
	"fi_dgram",
	"fi_dgram_waitset",
	"fi_msg",
	"fi_msg_epoll",
	"fi_msg_sockets",
	"fi_poll -t queue",
	"fi_poll -t counter",
	"fi_rdm",
	"fi_rdm -U",
	"fi_rdm_rma_event",
	"fi_rdm_rma_trigger",
	"fi_shared_ctx",
	"fi_shared_ctx --no-tx-shared-ctx",
	"fi_shared_ctx --no-rx-shared-ctx",
	"fi_shared_ctx -e msg",
	"fi_shared_ctx -e msg --no-tx-shared-ctx",
	"fi_shared_ctx -e msg --no-rx-shared-ctx",
	"fi_shared_ctx -e dgram",
	"fi_shared_ctx -e dgram --no-tx-shared-ctx",
	"fi_shared_ctx -e dgram --no-rx-shared-ctx",
	"fi_rdm_tagged_peek",
	"fi_scalable_ep",
	"fi_rdm_shared_av",
	"fi_multi_mr -e msg",
	"fi_multi_mr -e rdm",
	"fi_multi_ep -e msg -v",
	"fi_multi_ep -e rdm -v",
	"fi_recv_cancel -e rdm",
	"fi_unexpected_msg -e msg -I 10 -v",
	"fi_unexpected_msg -e rdm -I 10 -v",
	"fi_inject_test -A inject -v",
	"fi_inject_test -N -A inject -v",
	"fi_inject_test -A inj_complete -v",
	"fi_inject_test -N -A inj_complete -v",
	"fi_bw -e rdm -v -T 1",
	"fi_bw -e rdm -v -T 1 -U",
	"fi_bw -e msg -v -T 1",
	#"fi_rdm_multi_client -C 10 -I 5",
	#"fi_rdm_multi_client -C 10 -I 5 -U"
]

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--nodes', type=str,
						help='nodes separate by commas. type:string')
	#parser.add_argument('-p', '--path', type=str,
	#					help='path to libfabric bin. type:string')
	args = parser.parse_args()
	nodes = args.nodes
	#path = args.path
	nodes = nodes.split(',')

	err = create_dir()
	if err != 0:
		print(f"Exit create_dir with error: {err}")
		exit
	curdir = os.getcwd()
	bin_path = curdir.split('source')[0]
	bin_path = f'{bin_path}gpu/reg/bin'
	#bin_path = "/home/jdesai/bin"
	
	#curdir = os.getcwd().split('gpu')[0]
	#curdir = f'{curdir}/source/libfabric/fabtests/scripts/feature_coverage'
	print(f'curdir: {curdir}')
	#prov_list = ['tcp']
	for provider in prov_list:
		for test in unit_tests:
			print("---------------------------------------------------------")
			print(f"Running {test.split()[0]} test for {provider}")
			os.system(f"python3.9 feature_coverage.py \
			 		  -s \"{bin_path}/{test} -p {provider}\" \
					  -p {provider}")

		for test in functional_tests:
			print("---------------------------------------------------------")
			print(f"Running {test.split()[0]} test for {provider}")
			if (len(nodes) == 1):
				os.system(f"python3.9 {curdir}/feature_coverage.py \
			  			  -s \"{bin_path}/{test} -p {provider}\" \
						  -c \"{bin_path}/{test} -p {provider} {nodes[0]}\" \
						  -p {provider}")
			elif (len(nodes) == 2):
				os.system(f"python3.9 {curdir}/feature_coverage.py \
			  			  -s \"{bin_path}/{test} -p {provider} {nodes[0]}\" \
						  -c \"{bin_path}/{test} -p {provider} {nodes[1]}\" \
						  -p {provider}")
			else:
				os.system(f"python3.9 {curdir}/feature_coverage.py \
			  			  -s \"{bin_path}/{test} -p {provider}\" \
						  -c \"{bin_path}/{test} -p {provider} 127.0.0.1\" \
						  -p {provider}")
	print("---------------------------------------------------------")
	exit
