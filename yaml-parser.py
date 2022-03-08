from glob import glob
import yaml
from yaml.loader import SafeLoader
import datetime
import time as t
import threading

with open('Milestone1/Milestone1A.yaml','r') as f:
    data = yaml.load(f, Loader=SafeLoader)
time = 0

class Sequential:
    
    data = {}
    cur = ''
    concur = False
    def __init__(self,data,cur = '',concurrent = False):
        global time
        self.data = data
        self.cur = cur
        self.concur = concurrent
        threads = []
        print(str(datetime.datetime.now())+';'+self.cur+' Entry')
        k = data['Activities']

        for j in k:
            if k[j]['Type'] =='Task':
                if self.concur:
                    t_temp = threading.Thread(self.exec_func,args=(j,k[j]['Function'],k[j]['Inputs']))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    self.exec_func(j,k[j]['Function'],k[j]['Inputs'])
            else:
                #print(k[j])
                if self.concur:
                    t_temp = threading.Thread(target=Sequential, args = (k[j],self.cur+'.'+j,(k[j]['Execution'] == 'Concurrent')))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    next = Sequential(data = k[j],cur = self.cur+'.'+j,concurrent = (k[j]['Execution'] == 'Concurrent'))
                    #del next
        for x in threads:
            x.join()
        
        #self.__del__()
    def __del__(self):
        global time 
        print(str(datetime.datetime.now())+';'+self.cur+' Exit')

    def TimeFunction(self,i):
        t.sleep(int(i))
    
    def exec_func(self,name,func,inputs):
        global time
        print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Entry')
        if func == "TimeFunction":
            print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ( '+inputs['FunctionInput']+' , '+inputs['ExecutionTime']+' )' )
            self.TimeFunction(inputs['ExecutionTime'])
        print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Exit')



time = datetime.datetime.now()
for i in data:
    print(i)
    if data[i]['Execution'] =='Sequential':
        p1 = Sequential(data[i],i)
        #del p1