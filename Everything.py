# -*- coding: utf-8 -*-

import os.path

import ctypes
import datetime
import struct

#defines
EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
EVERYTHING_REQUEST_EXTENSION = 0x00000008
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_CREATED = 0x00000020
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
EVERYTHING_REQUEST_DATE_ACCESSED = 0x00000080
EVERYTHING_REQUEST_ATTRIBUTES = 0x00000100
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME = 0x00000200
EVERYTHING_REQUEST_RUN_COUNT = 0x00000400
EVERYTHING_REQUEST_DATE_RUN = 0x00000800
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED = 0x00001000
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME = 0x00002000
EVERYTHING_REQUEST_HIGHLIGHTED_PATH = 0x00004000
EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME = 0x00008000


class Everything:
    def __init__(self):
        self.importDll()
    
    #dll imports    
    def importDll(self,dllPath="Everything32.dll"):
        '''导入Everything32.dll,文件必须在同一个目录'''
        if os.path.exists(dllPath):
            self.everything_dll = ctypes.WinDLL (dllPath)
            self.everything_dll.Everything_GetResultDateModified.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_ulonglong)]
            self.everything_dll.Everything_GetResultSize.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_ulonglong)]
        else:
            print("Cannot find \""+dllPath+"\"!")
            #Liu Wei-maybe later I need to add some code to handle this case
            return
        
    def setDllFile(self,dllPath):
        self.dllPath=dllPath

    #setup search
    def setupSearch(self,searchText):
        self.everything_dll.Everything_SetMatchPath(True)
        self.everything_dll.Everything_SetSearchW(searchText)
        self.everything_dll.Everything_SetRequestFlags(EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH | EVERYTHING_REQUEST_SIZE | EVERYTHING_REQUEST_DATE_MODIFIED)
    
    #execute the query    
    def executeSearch(self):
        self.everything_dll.Everything_QueryW(1)

    #get the number of results
    def getNumResult(self):
        self.num_results = self.everything_dll.Everything_GetNumResults()

#show the number of results
#print("Result Count: {}".format(num_results))

    def get_time(self,filetime):
        """Convert windows filetime winticks to python datetime.datetime."""
        #convert a windows FILETIME to a python datetime
        #https://stackoverflow.com/questions/39481221/convert-datetime-back-to-windows-64-bit-filetime
        WINDOWS_TICKS = int(1/10**-7)  # 10,000,000 (100 nanoseconds or .1 microseconds)
        WINDOWS_EPOCH = datetime.datetime.strptime('1601-01-01 00:00:00',
                                                   '%Y-%m-%d %H:%M:%S')
        POSIX_EPOCH = datetime.datetime.strptime('1970-01-01 00:00:00',
                                                 '%Y-%m-%d %H:%M:%S')
        EPOCH_DIFF = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()  # 11644473600.0
        WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF * WINDOWS_TICKS  # 116444736000000000.0
        
        winticks = struct.unpack('<Q', filetime)[0]
        microsecs = int((winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS)
        try:
            d=datetime.datetime.fromtimestamp(microsecs)
            s=str(d.year)+"-"+str(d.month)+"-"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)
            return s
        except Exception as e:
            print(microsecs)
            print(str(e))
            return '2000-01-01 00:00:00'
        #print(s)
        
    
    #create buffers
    def createBuffers(self):
        self.filename = ctypes.create_unicode_buffer(260)
        self.date_modified_filetime = ctypes.c_ulonglong(1)
        self.file_size = ctypes.c_ulonglong(1)

    #show results
    def showResult(self):
        for i in range(self.num_results):        
            self.everything_dll.Everything_GetResultFullPathNameW(i,self.filename,260)
            self.everything_dll.Everything_GetResultDateModified(i,self.date_modified_filetime)
            self.everything_dll.Everything_GetResultSize(i,self.file_size)
            print("Filename: {}\nDate Modified: {}\nSize: {} bytes\n".format(ctypes.wstring_at(self.filename),self.get_time(self.date_modified_filetime),self.file_size.value))
            
    #show results
    #def getResult(self):
        #list=[]
        #for i in range(self.num_results):            
            #self.everything_dll.Everything_GetResultFullPathNameW(i,self.filename,260)
            #self.everything_dll.Everything_GetResultDateModified(i,self.date_modified_filetime)
            #self.everything_dll.Everything_GetResultSize(i,self.file_size)
            #d={"FileName":format(ctypes.wstring_at(self.filename)),"DateModified":self.get_time(self.date_modified_filetime),"FileSize":self.file_size.value}
            #list.append(d)
        #return list
    
    def getResult(self,searchStr):
        '''result是一个Tuple Set'''
        self.setupSearch(searchStr)
        self.executeSearch()
        self.getNumResult()
        num=self.num_results
        if self.num_results>3000:#大于3000条则只取3000条
            num=3000
        else:
            num=self.num_results
        self.createBuffers()
        result=set()
        for i in range(num):            
            self.everything_dll.Everything_GetResultFullPathNameW(i,self.filename,260)
            self.everything_dll.Everything_GetResultDateModified(i,self.date_modified_filetime)
            self.everything_dll.Everything_GetResultSize(i,self.file_size)
            if self.file_size.value==18446744073709551615:
                self.file_size.value=0
            fullName=format(ctypes.wstring_at(self.filename))
            # fileName=os.path.basename(fullName)
            # fileDir=os.path.dirname(fullName)
            
            # if not os.path.isdir(fullName):
            d=(fullName,str(self.file_size.value),self.get_time(self.date_modified_filetime))
            result.add(d)
                # d={"FileName":fileName,"FileDir":fileDir,"DateModified":self.get_time(self.date_modified_filetime),"FileSize":self.file_size.value}
            # d=set()
            # d.add(fullName)
            # d.add(str(self.file_size.value))
            # d.add(self.get_time(self.date_modified_filetime))
            # d=[fullName,str(self.file_size.value),self.get_time(self.date_modified_filetime)]
            #print(self.get_time(self.date_modified_filetime))
            #print(self.file_size)

        return result      

if __name__=="__main__":
    e=Everything()
    d=e.getResult("abb")
    #print(len(d))
    print(d)
    #print(len(d))