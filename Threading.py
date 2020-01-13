from tkinter import Tk, Frame, Label, Text, Entry, Listbox, Button, Scrollbar
from tkinter import StringVar, IntVar, END, N, S, E, W, X, Y, BOTH 
from tkinter import INSERT
import tkinter.ttk as ttk
import time
import threading
from ReadDict import readData
from ReadDict import writeData
from CompareInfo import updateData
import pdb
import math

showLocation = "Show Names.txt"
showInfoLocation = "info.txt"


def main():
    showList = []
    temp_show_data={}
    
    print('getting data')
    showList = readData(showLocation)


    for show in showList:
        print('\n',show)
        showInfo = updateData([show])
        if showInfo == "404":
            print("Server Error on '",show,"', getting 404")
        else:
            print('\n---------- ',showInfo)

    #print(temp_show_data)
#

main()
