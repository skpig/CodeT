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
    --source_path_for_solution "./dataset/human_eval.jsonl" \
    --predict_path_for_solution "./chatgpt_data/human_eval/solutions.jsonl" \
    --source_path_for_test "./dataset/human_eval.jsonl" \
    --predict_path_for_test "./chatgpt_data/human_eval/test_cases.pkl" \
    --cache_dir ./.runtime \
    --timeout 0.1