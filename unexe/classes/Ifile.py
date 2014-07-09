class ifile():
    def __init__(self,fname,mode):
        #column of the user class
        self.file = open(fname,mode)
        
    def write(self,str):
        self.file.write(str)
    
    def close(self):
        self.file.close()    