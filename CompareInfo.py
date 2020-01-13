from ReadDict import readData, writeData
import re
import ast
import pdb

showInfoLocation='info.txt'


#Take name of show, pass back formatted version to fit with web address 
def formatName(cont):
    cont=cont.lower();
    cont=cont.replace(" ","-")
    return cont 

#take show name, access its website, and return the page 
def getShowData(show):
    info={}
    try:
        # Retrieve Website, decode text, get ready to read
        from urllib.request import urlopen, Request
        url = "https://next-episode.net/"+show
        request = Request(url)
        response = urlopen(request)
        html = response.read()
        pageText = html.decode("utf-8")
        response.close()
        #parse info
        info = getInfo(toTags(pageText))

    except Exception as e:
        print ("Error in GetShowData - ",str(e))
        return "404"

    return info

#parse cleaned tags for usefull information about show
def getInfo (tags):
    info ={}
    field = ""
    prefix=""
    prNext = False
    for x in tags:
        if "HTTP Error 404: Not Found" in x:
            print("found 404 error")
            return "404"
        #split previous and next info    
        if "Previous Episode" in x:
            prefix="Prev-"
        if "Next Episode" in x:
            prefix="Next-"
            
        if ("Status" in x or
            "Date" in x or
            "Name" in x or
            "Season" in x or
            "Episode" in x or
            "Airs on" in x):
            prNext=True
            field = ""+prefix+x.replace(':','')
        elif prNext == True:
            info[field]=x
            prNext=False
        else:
            prNext=False
    return info

# convert page to list of tags, and strip away useless information
def toTags(cont):
    tags=[]
    #remove scripts
    cont = re.sub( '\<script.*?\\\script\>','',cont)
    cont=re.split("\<.*?\>",cont)
    adding= False
    
    for x in cont:
        #find start of usefull information
        if "to watchlist" in x:
            adding=True
        
        if adding:
            tacont = x.strip();
            if tacont!='' and len(tacont)<255:
                tags.append(tacont)
        #end of useful information
        if "Episodes Guide and Summaries" in x:
            adding= False
            
    #cant remove duplicates
    #tags=list(dict.fromkeys(tags))
            
    return tags


def makeDict(show):
    shows = {}
    for names in show:
        info = getShowData(formatName(names))
        if info == "404":
            return info

        #ensure shows have some value for this, even if scrubber found nothing
        shows[names]= {
            'Title':names,
            'Airs On':'',
            'Status':'',
            'Prev-Name':'',
            'Prev-Date':'',
            'Prev-Season':'',
            'Prev-Episode':'',
            'Next-Name':'',
            'Next-Date':'',
            'Next-Season':'',
            'Next-Episode':'',
            'Out-of-Date':[]
            }
        for x in info:
            shows[names][x]=info[x]
        
    return shows






# pull new info, updat the log as required, and return info
def updateData(showNames):
    newInfo=(makeDict(showNames))
    if newInfo == "404":
        return newInfo

    oldInfo={}
    try:
        oldInfo=readData(showInfoLocation)
        if oldInfo=='':
            raise Exception('Old info is empty')
    except Exception as error:
        print(repr(error)," - Passing all new information")
        oldInfo=newInfo

    #compare oldinfo next to new info next
    #if same, do nothing.  If changed, add episode to Out-of-Date;
    for show in newInfo:
        for details in newInfo[show]:
            try:    #compare old data to new
                if newInfo[show][details]!=oldInfo[show][details] and details!='Out-of-Date':
                    if 'Prev-Name' in details:
                        oldInfo[show]['Out-of-Date'].append(newInfo[show][details])
                    #print('changing:',oldInfo[show][details],' - ',newInfo[show][details])
                    oldInfo[show][details] = newInfo[show][details]
            except:
                print('Error - Prev log does not match new formating.  Adding missing field for', newInfo[show][details])
                oldInfo[show]=newInfo[show]
#    pdb.set_trace()
    return oldInfo

def checkNew():
    data = updateData()
    for show in data:
        outdate = data[show]['Out-of-Date']
        if outdate!=[]:
            print(show,'Has ',len(outdate), 'unwatched episodes:')
            for eps in outdate:
                print(eps)
    return
