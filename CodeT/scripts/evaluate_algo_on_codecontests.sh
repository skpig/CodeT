#!/bin/bash  
  
# 获取当前脚本文件的绝对路径  
script_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"  
  
# 获取脚本文件所在目录的父目录  
script_parent_dir="$(dirname "$(dirname "$script_path")")"  
  
# 打印当前工作目录  
echo "Current working directory: $(pwd)"  
  
# 将工作目录更改为脚本文件所在目录的父目录  
cd "$script_parent_dir"  
  
# 打印新的工作目录  
echo "New working directory: $(pwd)"  

python main.py \
    --source_path_for_solution "./dataset/CodeContests.jsonl" \
    --predict_path_for_solution "./algo_data/CodeContests/solutions.jsonl" \
    --source_path_for_test "./dataset/CodeContests.jsonl" \
    --predict_path_for_test "./algo_data/CodeContests/test_cases.pkl" \
    --cache_dir ./.runtime \
    --output_path "algo_data/CodeContests/code_sorted_algo.pkl" \
    --timeout 0.1