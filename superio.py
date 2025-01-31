import os
import json
import asyncio
import select
import time
import sys
import ptyprocess
import pickle

def load(path:str):
    with open(path, 'rb') as f:
        return pickle.load(f)
def save(path:str,obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

class consistentIO:
    def __init__(self):
        self.pt= ptyprocess.PtyProcess.spawn(['lake','exe','repl'])
        # self.pt.read()  #去头
        self.outputs=[]
        
    def get_output(self,input,sp='\r\n\r\n'):#输入json，输出结果
        head=json.dumps(input) #循环切除用
        # print(head)

        input=head+'\n\n' #转化为字符串,并且加上换行符
        input_raw=input.encode('utf-8') #转化为字节
        self.pt.write(input_raw) #输入一个命令
        raw=''
        while raw.rfind('"env":')<0:
            raw = raw + self.pt.read().decode('utf-8', errors='ignore')
            raw = raw.replace(head,'')#切掉输入
        #读到有env的行

        output= raw.strip().split(sp)[-1].strip() #去掉前面的无用信息，并去掉头尾换行
        self.outputs.append(json.loads(output))
        return self.outputs[-1]
    
    def get_tactic_output(self,input):#输入json，输出结果
        head=json.dumps(input) #循环切除用

        print(head)

        input=head+'\n\n' #转化为字符串,并且加上换行符
        input_raw=input.encode('utf-8') #转化为字节
        self.pt.write(input_raw) #输入一个命令
        
        raw=(self.pt.read().decode('utf-8'))#获取原始输出
        raw = raw.replace(head,'')#切掉输入
        while raw.count('{')!=raw.count('}') or raw.find('proofState')<0:
            if raw.find('Lean error')>=0:
                return 'ERROR'
            raw = raw + self.pt.read().decode('utf-8')
            raw = raw.replace(head,'')#切掉输入
        #读到有env的行

        output= raw.strip().split("\r\n\r\n")[-1].strip() #去掉前面的无用信息，并去掉头尾换行
        self.outputs.append(json.loads(output))
        return self.outputs[-1]




    def comd_append(self,command:str,env=None):#命令声明
        input={"cmd":command}
        if env!=None:
            input["env"]=env
        return self.get_output(input)

    def tactic_append(self,command:str,proof_state=0):#tactic 注入
        input={"tactic":command,"proofState":proof_state}
        return self.get_tactic_output(input)

    
    def save_env(self,path:str,env): #保存环境
        input={"pickleTo": path, "env": env}
        return self.get_output(input)

    
    def load_env(self,path:str): #加载环境
        input={"unpickleEnvFrom": path}
        return self.get_output(input,'\r\n')

    
    def save_state(self,path:str,state): #保存状态
        input={"pickleTo": path, "proofState": state}
        return self.get_output(input)
    
    def load_state(self,path:str): #加载状态
        input={"unpickleProofStateFrom": path}
        return self.get_output(input)
    
    def load_file(self,path:str): #加载文件
        input={"allTactics": False,'path':path}
        return self.get_output(input)

    def __exit__(self): #关闭管道
        self.pt.close()

if __name__ == '__main__':
    io=consistentIO()
    res=io.load_file('/home/limengze/Lean_Test/automatic-lean4-compilation/1011/temp.lean')
    print(res)