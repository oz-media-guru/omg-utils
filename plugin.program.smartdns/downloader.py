import xbmcgui
import urllib

def download(url, dest, dp , data, name):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Status...","Checking Installation",' ', ' ')
    dp.update(0)
    (finame, hdrs) = urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp,name), data)
    dp.close()
    print hdrs
    if 'Content-Type: text/html' in str(hdrs):
        file = open(dest, 'r')
        errorReturned = file.read()
        file.close()
        raise Exception("Failed: "+errorReturned)

 
def _pbhook(numblocks, blocksize, filesize, url, dp,name):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        if filesize > 10485760:
            line1 = name+": "+str(min(filesize/1048576, (numblocks*blocksize)/1048576)) + " MB / " +str(filesize/1048576)+" MB"
        elif filesize > 10240:
            line1 = name+": "+str(min(filesize/1024, (numblocks*blocksize)/1024)) + " KB / " +str(filesize/1024)+" KB"
        else:
            line1 = name+": "+str(min(filesize,(numblocks*blocksize))) + " bytes / " +str(filesize)+" bytes"
        dp.update(percent,line1)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()
