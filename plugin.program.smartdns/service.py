import xbmcaddon, xbmcgui,xbmc,xbmcplugin,urllib,urllib2, os, subprocess, re, sys, mg_common
import fcntl, socket, struct


try: 			from addon.common.addon 	import Addon
except:
    try: 		from t0mm0.common.addon import Addon
    except: from t0mm0_common_addon import Addon
addon_id='plugin.program.smartdns';



settings=xbmcaddon.Addon(id=addon_id);

dnsprov=settings.getSetting('dns-provider');



mainPath=xbmc.translatePath(os.path.join('special://home','addons',addon_id));
fanart=xbmc.translatePath(os.path.join(mainPath,'fanart.jpg')); #fanart=artPath+'fanart.jpg'; #fanart=xbmc.translatePath(os.path.join('special://home','addons',addon_id+'/'))+'fanart.jpg'; #fanart=getArtworkJ('fanart')
iconart=xbmc.translatePath(os.path.join(mainPath,'icon.png')); #print ['fanart',fanart,'iconart',iconart];
base_url='http://media-guru.com.au/'

__addon__        = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__      = __addon__.getAddonInfo('id')
__addonname__    = __addon__.getAddonInfo('name')




#****************************************************************

def log(txt):
    message = '%s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGWARNING)

class Main:
  def __init__(self):

    log('Inside MG Media Player on startup')
    if dnsprov=='4':
        while xbmc.getIPAddress() == '0.0.0.0':
            log('Waiting for IP address')
            xbmc.sleep(10)
        log('Going to update MG DNS')
        try:
            mg_common.addSmartDns()

        except:
            log('Error executing MG NDS')



log('MediaGuru startup script (version %s) started' % __addonversion__)
log('MediaGuru DNS provider setting (%s) started' % dnsprov)
Main()



