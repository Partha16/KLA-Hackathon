import yaml
from yaml.loader import SafeLoader
import datetime
import time as t
import threading
import sys



class Sequential:
    
    data = {}
    cur = ''
    concur = False
    threadLock = threading.Lock()
    def __init__(self,data,cur = '',concurrent = False):
        global time
        self.data = data
        self.cur = cur
        self.concur = concurrent
        threads = []
        self.threadLock.acquire()
        print(str(datetime.datetime.now())+';'+self.cur+' Entry')
        self.threadLock.release()
        k = data['Activities']
        
        for j in k:
            if k[j]['Type'] =='Task':
                if self.concur:
                    t_temp = threading.Thread(target = self.exec_func,args=(j,k[j]['Function'],k[j]['Inputs']))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    self.exec_func(j,k[j]['Function'],k[j]['Inputs'])
            else:
                #print(k[j])
                l = k[j]['Execution'] == 'Concurrent'
                if self.concur:
                    t_temp = threading.Thread(target=Sequential, args = (k[j],self.cur+'.'+j,l))
                    threads.append(t_temp)
                    t_temp.start()
                else:
                    Sequential(data = k[j],cur = self.cur+'.'+j,concurrent = l)
                    #del next
        for x in threads:
            x.join()
        
        #self.__del__()
    def __del__(self):
        self.threadLock.acquire()
        print(str(datetime.datetime.now())+';'+self.cur+' Exit')
        self.threadLock.release()

    def TimeFunction(self,i):
        t.sleep(int(i))
    
    def exec_func(self,name,func,inputs):
        self.threadLock.acquire()
        print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Entry')
        self.threadLock.release()

        if func == "TimeFunction":
            self.threadLock.acquire()
            print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Executing '+func+' ( '+inputs['FunctionInput']+' , '+inputs['ExecutionTime']+' )' )
            self.threadLock.release()

            self.TimeFunction(inputs['ExecutionTime'])

        self.threadLock.acquire()
        print(str(datetime.datetime.now())+';'+self.cur+'.'+name+' Exit')
        self.threadLock.release()

## -------------------Milestoone 1A-----------------------------
with open('Milestone1\Milestone1A.yaml','r') as f:
    data = yaml.load(f, Loader=SafeLoader)

orig_stdout = sys.stdout
f = open('ml1a.txt', 'w')
sys.stdout = f

for i in data:
    #print(i)
    if data[i]['Execution'] =='Sequential':
        p1 = Sequential(data[i],i)
        del p1

sys.stdout = orig_stdout
f.close()

## -------------------Milestoone 1B-----------------------------
with open('Milestone1\Milestone1B.yaml','r') as f:
    data = yaml.load(f, Loader=SafeLoader)

orig_stdout = sys.stdout
f = open('ml1b.txt', 'w')
sys.stdout = f

for i in data:
    #print(i)
    if data[i]['Execution'] =='Sequential':
        p1 = Sequential(data[i],i)
        del p1

sys.stdout = orig_stdout
f.close()
