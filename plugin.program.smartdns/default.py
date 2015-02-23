import xbmcaddon, xbmcgui,xbmc,xbmcplugin,urllib,urllib2, os, subprocess, re, sys, mg_common, os.path, tarfile, t0mm0_common_addon
import fcntl, socket, struct

from t0mm0_common_addon 	import Addon

addon_id='plugin.program.smartdns'
addon=Addon(addon_id,sys.argv)


settings=xbmcaddon.Addon(id=addon_id)

dnsprov=settings.getSetting('dns-provider')

mainPath=xbmc.translatePath(os.path.join('special://home','addons',addon_id))
fanart=xbmc.translatePath(os.path.join(mainPath,'fanart.jpg'))
iconart=xbmc.translatePath(os.path.join(mainPath,'icon.png'))
base_url='http://media-guru.com.au/'

__addon__        = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__      = __addon__.getAddonInfo('id')
__addonname__    = __addon__.getAddonInfo('name')




artPath=xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art2/'))

def getArtwork(n): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art2',n))
def getArtworkJ(n): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art2',n+'.jpg'))
def getBackupScript(): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'scripts','backupMenu.sh'))
def getRestoreScript(): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'scripts','restoreMenu.sh'))
def getScriptDir(): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'scripts'))
def getScriptTar(): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'scripts',"menubackup.tar"))

#****************************************************************
def MAININDEX():


    addDir('Update network to SMART DNS','none','smartdns',getArtworkJ('updateDNS'))

    addDir('SMART DNS Settings','none','settings',getArtworkJ('settings'))
    addDir('Backup Menu Setup','none','backup',getArtworkJ('backup'))
    addDir('Restore Menu Setup','none','restore',getArtworkJ('restore'))

    AUTO_VIEW('')

#****************************************************************
def backupMenu():
    script = getBackupScript()
    if not os.path.isfile(script):
        tar = tarfile.open(getScriptTar())
        tar.extractall(getScriptDir())

    dialog = xbmcgui.Dialog()
    dialog.ok('Backup Menu', 'On pressing OK, XBMC will pause for a few seconds.','It will then restart')


    os.system('sh '+getBackupScript())
#****************************************************************
def restoreMenu():
    script = getRestoreScript()
    if not os.path.isfile(script):
        tar = tarfile.open(getScriptTar())
        tar.extractall(getScriptDir())

    dialog = xbmcgui.Dialog()
    dialog.ok('Restore Menu', 'On pressing OK, XBMC will pause for a few seconds.','It will then restart with the restored menu')

    os.system('sh '+getRestoreScript())


#****************************************************************
def AUTO_VIEW(content='',viewmode=''): # Set View
     viewmode=str(viewmode); content=str(content);
     if len(viewmode)==0:
         if settings.getSetting('auto-view')=='true':
             if content=='addons':  viewmode=settings.getSetting('addon-view')
             else:                  viewmode=settings.getSetting('default-view')
         else: viewmode='500'
     if len(content) > 0: xbmcplugin.setContent(int(sys.argv[1]),str(content))
     #if settings.getSetting('auto-view')=='true': xbmc.executebuiltin("Container.SetViewMode(%s)" % str(viewmode))
     if len(viewmode) > 0: xbmc.executebuiltin("Container.SetViewMode(%s)" % str(viewmode))
# HELPDIR**************************************************************
def addDir(name,url,mode,thumb):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name); ok=True;
        liz=xbmcgui.ListItem(name,iconImage=iconart,thumbnailImage=thumb);
        #liz.setInfo(type="Video",infoLabels={"title":name,"Plot":description})
        try: liz.setProperty("fanart_image",fanart)
        except: pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True); return ok

def get_params():
    param=[]; paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]; cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&'); param={}
        for i in range(len(pairsofparams)):
            splitparams={}; splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
    return param

def grbPrm(n):
    try:    return urllib.unquote_plus(params[n])
    except: return ''


params=get_params(); url=None; name=None; mode=None; year=None; imdb_id=None
url=grbPrm("url"); filetype=grbPrm("filetype"); iconimage=grbPrm("iconimage"); fanart=grbPrm("fanart"); description=grbPrm("description"); name=grbPrm("name"); repourl=grbPrm("repourl"); author=grbPrm("author"); version=grbPrm("version");
try:		mode=urllib.unquote_plus(params["mode"])
except: pass
print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
if mode==None or url==None or len(url)<1: MAININDEX()
try:
	if url: print url
except: pass
if   mode=='settings':  			addon.show_settings()																		# Settings
elif mode=='smartdns': 			    mg_common.addSmartDns()
elif mode=='backup': 			    backupMenu()
elif mode=='restore': 			    restoreMenu()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
