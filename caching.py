from collections import OrderedDict
import time,sys,os.path

class cacheForLRU:
    def __init__(self):
        self.cache = OrderedDict()
        if os.path.isfile('backup.txt'):
            self.cache = OrderedDict()
            fr = open('backup.txt','r')
            for line in fr:
                if len(line.strip())>0:
                    data = line.split('\t')
                    self.cache[data[0]] = data[1]
            fr.close()
        self.maxSize,self.ttl,self.ttlCache = 5,30,{}
        
    def refreshCache(self):
        try:
            print('In Refresh Cache')
            fw = open('backup.txt','w')
            for key,val in self.cache.items():
                fw.write(key+'\t'+val+'\n')
                fw.flush()
                
            current = time.time()
            for key,val in self.ttlCache.items():
                if current-val > self.ttl: del self.cache[key]
            fw.close()
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),e)
    
    def get(self,key):
        try:
            if key not in self.cache: return -1
            else:
                self.cache.move_to_end(key)
                self.ttlCache[key] = time.time()
                return self.cache[key]
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),e)
    
    def put(self,key,val):
        try:
            self.cache[key],self.ttlCache[key] = val,time.time()
            self.cache.move_to_end(key)
            if len(self.cache)/self.maxSize >= 0.75: self.refreshCache()
            if len(self.cache) > self.maxSize: self.cache.popitem(last=False)
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),e)    
