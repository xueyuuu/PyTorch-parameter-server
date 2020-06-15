# KEY_PEM_NAME=HongyiScript.pem
#!/bin/bash
export DEEPLEARNING_WORKERS_COUNT=`wc -l < ${HOME}/PyTorch-parameter-server/tools/hosts_address`
MASTER_PUB_IP="$1"
WORKING_DIR=${HOME}/PyTorch-parameter-server/src

host_file="${HOME}/PyTorch-parameter-server/tools/hosts_address"

host_ip=`cat $host_file | awk '{ print $0 }'`
i=0
for ip in $host_ip;
  do
    ((i++))
    ssh $ip "cd ${WORKING_DIR}; nohup bash ${WORKING_DIR}/run_pytorch_dist.sh \"$((${i}-1))\" \"${DEEPLEARNING_WORKERS_COUNT}\" \"${MASTER_PUB_IP}\" &>/dev/null &"
  done

#for i in $(seq 1 $DEEPLEARNING_WORKERS_COUNT);
#  do
#    ssh worker${i} "cd ${WORKING_DIR}; nohup bash ${WORKING_DIR}/run_pytorch_dist.sh \"$((${i}-1))\" \"${DEEPLEARNING_WORKERS_COUNT}\" \"${MASTER_PUB_IP}\" &>/dev/null &"
#  done