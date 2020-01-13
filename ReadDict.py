import ast

def readList(filename):
    newList=[]
    # open file and read the content in a list
    with open(filename, 'r') as store:  
        filecontents = store.readlines()
        for line in filecontents:
            # remove linebreak which is the last character of the string
            current_place = line.strip()[1:-1]
            if current_place !='':
                # add item to the list
                newList.append(current_place)
    store.close()
    return(newList)


def readData(filename):
    try:
        with open(filename) as f:
            data = ast.literal_eval(f.read())
    except:
        print("No file found.  Creating an empty file")
        writeData(filename, '')
        data=''
        
    return data

def readData2(filename):
    mainType=''
    data=''
    tempList=[]
    tempDict={}
    # open file and read the content in a list
    with open(filename, 'r') as store:  
        filecontents = store.readlines()
        for line in filecontents:
            if '{' in line and mainType=='':
                mainType='dict'
                data={}
            if '[' in line and mainType=='':
                mainType='list'
                data=[]
            #######  Dropped trying to write, as I cant find an elegant way to do it  ####
            ##      regex would definitely be possible, but difficult, and I have       ##
            ##      already found an alternative, ast.literal_eval()                    ##
            ##############################################################################
            # remove linebreak which is the last character of the string
            #current_place = line.strip()[1:-1]
            #if current_place !='':
                # add item to the list
            #    newList.append(current_place)
    store.close()
    return(data)




def formatSet(data, nest=0, hasKeys=False):
    clip=""
    op=''
    ed=''
    pre=''
    post=''
    hasLeaf=False

    if isinstance(data, str):
        op="'"
        ed="'"
    elif isinstance(data, list):
        op='['
        ed=']'
        hasLeaf=True
    elif isinstance(data, dict):
        op='{'
        ed='}'
        hasLeaf=True
        hasKeys=True
    x=0
    if hasKeys: x=nest
    while x<nest:
        clip+="\t"
        x+=1
    clip+=op

    if hasLeaf:
        for leaf in data:
            clip+="\n"+formatSet(leaf, nest+1)
            # check for keys if it is a dict
            if hasKeys:
                    clip+=': '+formatSet(data[leaf], nest+1, hasKeys)
                    haskeys=False
        clip+="\n"
        x=0
        while x<nest:
            clip+="\t"
            x+=1
                
    else:
        clip+=data

    clip+=ed
    return clip

def writeDataOld(filename, data):
    clip = formatSet(data)
    with open(filename, 'w') as store:
        store.write(clip)
        store.close()
    return        

def writeData(filename, data):
    with open(filename, 'w') as store:
        store.write(str(data))
        store.close()
    return
		

#create a list, print to screen to show, print to file to test;
def writetest():
#    list="test"
#    list={'1':['red',"green"]}
#    list={'1':'red','2':'blue','3':'green'}
#    list={'Jane The Virgin': {'Title': 'Jane The Virgin', 'Status:': 'Running', 'Prev-Name:': 'Chapter Eighty-Five', 'Prev-Date:': 'Wed Apr 17, 2019', 'Prev-Season:': '5', 'Prev-Episode:': '4', 'Next-Name:': 'Chapter Eighty-Six', 'Next-Date:': 'Wed Apr 24, 2019', 'Next-Season:': '5', 'Next-Episode:': '5'}}
#    list={'Jane The Virgin': {'Title': 'Jane The Virgin', 'Status:': 'Running', 'Prev-Name:': 'Chapter Eighty-Five', 'Prev-Date:': 'Wed Apr 17, 2019', 'Prev-Season:': '5', 'Prev-Episode:': '4', 'Next-Name:': 'Chapter Eighty-Six', 'Next-Date:': 'Wed Apr 24, 2019', 'Next-Season:': '5', 'Next-Episode:': '5'}, 'Game of Thrones': {'Title': 'Game of Thrones', 'Status:': 'Running', 'Prev-Name:': 'Winterfell', 'Prev-Date:': 'Sun Apr 14, 2019', 'Prev-Season:': '8', 'Prev-Episode:': '1', 'Next-Name:': 'TBA', 'Next-Date:': 'Sun Apr 21, 2019', 'Next-Season:': '8', 'Next-Episode:': '2'}, 'House of Cards 2013': {'Title': 'House of Cards 2013', 'Status:': 'Canceled/Ended'}, 'Santa Clarita Diet': {'Title': 'Santa Clarita Diet', 'Status:': 'Returning Series', 'Prev-Name:': 'Wuffenloaf (+9 more)', 'Prev-Date:': 'Fri Mar 29, 2019', 'Prev-Season:': '3', 'Prev-Episode:': '1, 2, 3, 4, 5, 6, 7, 8, 9, 10', 'Next-Next Episode': 'Sorry, no info about the next episode of Santa Clarita Diet is available yet.'}}
#    print(str(list))
    writeData(filename,list)
    return

def readtest():
    list = readData(filename)
    print(list['Jane The Virgin']['Status:'])
    return

