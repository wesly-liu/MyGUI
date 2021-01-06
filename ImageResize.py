# -*- coding: utf-8 -*-
from PIL import Image
# from MyClipboard import *
import os
from sys import argv
def size(jpg,now_size):
    im = Image.open(jpg)
    width, height = im.size
    if width>now_size:
        n=width/now_size
        w=int(width/n)
        h=int(height/n)
        resizedIm = im.resize((w,h))
        splitName=os.path.splitext(jpg)
        fileName=splitName[0]+"-s"+splitName[1]
        resizedIm.save(fileName)
        return True
    else:
        print('无需缩放')
        return False

# def main(now_size):
#     #now_size = int(input('Please input the size of the file(1024=1024*768)'))
#     #file=input('要缩放的txt文本文件路径:')
#     #txt_file=file.replace('\"','').replace('\n','')
#     #txt_conte=open(txt_file,encoding='utf-8')
#     #txt_linst=txt_conte.readlines()
#     files=getText()
#     txt_linst=files.split('\n')
#     for i in txt_linst:
#         jpg=r'%s'%i.replace('\n','').replace('\"','').encode('utf-8').decode('utf-8-sig').strip()
#         ext=os.path.splitext(jpg)
#         if(ext[1].upper()!='.JPG'):
#             continue
#         if os.path.exists(jpg):
#             size(jpg, now_size)

# if __name__ == '__main__':
#     now_size=1280
#     if len(argv)==2:
#         now_size=int(argv[1])
#     main(now_size)