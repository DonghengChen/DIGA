import json
import superio as sio
buffer = {}
def cut_gen(id,lean4):
    if lean4 in buffer:
        return id,buffer[lean4]
    #用tempfile创建临时文件，返回文件名
    with open("/home/limengze/Lean_Test/automatic-lean4-compilation/temp/t%d.lean"%id,'w') as f:
        f.write(lean4)
    cio = sio.consistentIO()
    state = cio.load_file("/home/limengze/Lean_Test/automatic-lean4-compilation/temp/t%d.lean"%id)
    buffer[lean4] = state
    return id, state

import concurrent.futures

from func_timeout import func_set_timeout

def parallel_requests(func,prompts_list,max_process=16):
    Flag = True
    results = [0]*len(prompts_list)
    # 使用线程池来并行处理请求
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_process) as executor:
        # 提交所有的请求到线程池
        futures = [executor.submit(func,id,item) for id,item in enumerate(prompts_list)]
        # 收集所有请求的结果
        for future in concurrent.futures.as_completed(futures):
            try:
                id,result = future.result()
                results[id]= result
            except Exception as exc:
                Flag = False
    return Flag,results

with open("/home/limengze/Lean_Test/automatic-lean4-compilation/MATH.json",'r') as f:
    data = json.load(f)
wait_test=[]
for item in data:
    lean4 = item['lean4']
    head = 'import Mathlib\n'
    # 处理sorry
    if lean4.find('sorry')>0:
        lean4 = lean4[:lean4.find('sorry')]
        lean4 = head + lean4 + ' sorry'
    elif lean4.find('by')>0:
        lean4 = lean4[:lean4.find('by')]
        lean4 = head + lean4 + ' sorry'
    elif lean4.rfind(':=')>0:
        lean4 = lean4[:lean4.rfind(':=')]
        lean4 = head + lean4 + ' := sorry'
    else:
        print(lean4)
    wait_test.append(lean4)

test_res=parallel_requests(cut_gen,wait_test,128)

print(len(wait_test))
