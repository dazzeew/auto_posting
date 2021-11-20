import os
import sys



def list_write():
    f = open('text.txt')
    l = [line.strip() for line in f] 
    f.close()
    return l

print(list_write())