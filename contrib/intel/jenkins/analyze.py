import os
import sys

# add jenkins config location to PATH
sys.path.append(os.environ['CI_SITE_CONFIG'])

import ci_site_config
import argparse
import subprocess
import shlex
import common
import re
import shutil

"""
These are the different type of files that we want to analyze
choices = [  
            'shmem',
            'IMB', 
            'osu', 
            'oneccl',
            'mpichtestsuite', 
            'fabtests', 
            'onecclgpu'])
"""

if __name__ == "__main__":
#read Jenkins environment variables
    # In Jenkins,  JOB_NAME  = 'ofi_libfabric/master' vs BRANCH_NAME = 'master'
    # job name is better to use to distinguish between builds of different
    # jobs but with same branch name.
    jobname = os.environ['JOB_NAME']
    buildno = os.environ['BUILD_NUMBER']
    workspace = os.environ['WORKSPACE']
"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--build_item', help="build libfabric or fabtests",
                         choices=['libfabric', 'fabtests', 'builddir', 'logdir'])
    parser.add_argument('--ofi_build_mode', help="select buildmode debug or dl", \
                        choices=['dbg', 'dl'])

    args = parser.parse_args()
    build_item = args.build_item

    if (args.ofi_build_mode):
        ofi_build_mode = args.ofi_build_mode
    else:
        ofi_build_mode = 'reg'
"""
    logs_path = f'{ci_site_config.install_dir}/{jobname}/{buildno}/log_dir'

    log_files = os.listdir(logs_path)
    for log in log_files:
        if log.contains('shmem'):
            continue
        if log.contains('IMB'):
            continue
        if log.contains('osu'):
            continue
        if log.contains('oneccl'):
            continue
        if log.contains('mpichtestsuite'):
            continue
        if log.contains('fabtests'):
            continue
        if log.contains('onecclgpu'):
            continue
