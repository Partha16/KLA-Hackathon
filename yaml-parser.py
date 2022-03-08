from glob import glob
import yaml
from yaml.loader import SafeLoader
import datetime
import time as t

with open('Milestone1/Milestone1A.yaml','r') as f:
    data = yaml.load(f, Loader=SafeLoader)
time = 0

class Sequential:
    
    data = {}
    cur = ''
    def __init__(self,data,cur = ''):
        global time
        self.data = data
        self.cur = cur
        print(str(datetime.datetime.now())+';'+self.cur+' Entry')
        k = data['Activities']
        for j in k:
            if k[j]['Type'] =='Task':
                #print(j)
                self.exec_func(j,k[j]['Function'],k[j]['Inputs'])
            else:
                #print(k[j])
                next = Sequential(data = k[j],cur = self.cur+'.'+j)
                #self.time += p2.time
                del next

    def __del__(self):
        global time 
        print(str(datetime.datetime.now())+';'+self.cur+' Exit')

    def TimeFunction(self,i):
        #global time
        #time += datetime.timedelta(0,int(i))
        t.sleep(int(i))
        #print(self.time)
    
    def exec_func(self,name,func,inputs):
        global time
        print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Entry')
        if func == "TimeFunction":
            print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ( '+inputs['FunctionInput']+' , '+inputs['ExecutionTime']+' )' )
            self.TimeFunction(inputs['ExecutionTime'])
        print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Exit')

class Concurrent:

    data = {}
    cur = ''
    def __init__(self,data,cur = ''):
        global time
        self.data = data
        self.cur = cur

time = datetime.datetime.now()
for i in data:
    print(i)
    if data[i]['Execution'] =='Sequential':
        p1 = Sequential(data[i],i)
        del p1