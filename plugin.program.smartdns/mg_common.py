import xbmcaddon, xbmcgui,xbmc,xbmcplugin,urllib,urllib2, os, subprocess, re, sys
import fcntl, socket, struct, downloader
from xml.etree import ElementTree as ET

addon_id='plugin.program.smartdns'



settings=xbmcaddon.Addon(id=addon_id)

dnsprov=settings.getSetting('dns-provider')

class MyClass(xbmcgui.Window):
    def __init__(self):
        self.strActionFade = xbmcgui.ControlFadeLabel(100, 300, 400, 200, 'font24', '0xFFFFFF00')
        self.addControl(self.strActionFade)
        self.strActionFade.addLabel('XBMC Upgrading ... This will take a few minutes.')
        self.strActionFade1 = xbmcgui.ControlFadeLabel(100, 500, 600, 200, 'font24', '0xFFFFFF00')
        self.addControl(self.strActionFade1)
        self.strActionFade1.addLabel('DO NOT unplug whilst upgrading as it will damage the box.')




def is_valid_ipv4(ip):
    """Validates IPv4 addresses.
    """
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None



def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])


def updateMGServers():
    print "updateMGServers"
    mac = getHwAddr("eth0")
    print "mac: "+mac
    username = settings.getSetting('mg-username')
    password = settings.getSetting('mg-password')
    url = 'http://www.media-guru.com.au/dnsupdate.php'
    values = {'username' : username,
          'password' : password,
          'macaddr' : mac }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    dialog = xbmcgui.Dialog()
    ip_list = the_page.strip().split('|')
    for ip_addr in ip_list:
        if not is_valid_ipv4(ip_addr):
            dialog = xbmcgui.Dialog()
            dialog.notification("Smart DNS Settings", "Error: "+the_page)
            return None
    return ip_list





def getAvailableDownloads():
    print "getAvailableDownloads"
    mac = getHwAddr("eth0")
    print "mac: "+mac
    username = settings.getSetting('mg-username')
    password = settings.getSetting('mg-password')
    url = 'http://www.media-guru.com.au/getavailabledownloads.php'
    values = {'username' : username,
          'password' : password,
          'macaddr' : mac }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print the_page
    try:
        root = ET.fromstring(the_page)
        return root
    except:

        dialog = xbmcgui.Dialog()
        dialog.notification("Upgrade", "Error: "+the_page)
        return None


def getDownload(downloadFile):
    print "getDownload"
    mac = getHwAddr("eth0")
    print "mac: "+mac

    username = settings.getSetting('mg-username')
    while username == "":
        dialog = xbmcgui.Dialog()
        dialog.ok("Missing username!", "Please enter a forum username in the settings page")
        settings.show_settings()
    #password = settings.getSetting('mg-password')
        username = settings.getSetting('mg-username')


    dialog = xbmcgui.Dialog()
    password = dialog.input('Enter MG forum password for: '+username, type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)


    url = 'http://www.media-guru.com.au/getdownload.php'
    urlsc = 'http://www.media-guru.com.au/getscript.php'
    values = {'username' : username,
          'password' : password,
          'macaddr' : mac,
          'download' : downloadFile}
    data = urllib.urlencode(values)

    dp=xbmcgui.DialogProgress();
    dp.create("Downloading upgrade:","New file downloading...");
    try:
        downloader.download(url,'/storage/downloads/'+downloadFile+".tar",dp, data, downloadFile)

    except Exception as e:
        dialog = xbmcgui.Dialog()
        dialog.ok("Download failed!", str(e))
        return None

    try:
        downloader.download(urlsc,'/storage/downloads/script.sh',dp, data, "Script for "+downloadFile)
    except Exception as e:
        dialog = xbmcgui.Dialog()
        dialog.ok("Download failed!", str(e))
        return None


    file = open("/storage/downloads/upgfile", "w")
    file.write(downloadFile+".tar")
    file.close()

    dialog = xbmcgui.Dialog()
    ok = dialog.ok('Upgrade Files Downloaded', 'On selecting OK, XBMC/Kodi will appear to hang. It will be upgrading. This can take around 5 minutes and it will automatically restart - DO NOT pull out plug while upgrading as this will damage your box.')

    #p = subprocess.Popen(["chmod", "ugo+x", "/storage/downloads/script.sh"], stdout=subprocess.PIPE)
    #dialog = xbmcgui.Dialog()
    #dialog.notification("Upgrading", "Please wait whilst your box is being upgraded...")
    #xbmc.sleep(500)

    mydisplay = MyClass()
    #mydisplay.doModal()
    mydisplay.show()


    try:
        subprocess.call(["/storage/downloads/script.sh"])
    except subprocess.CalledProcessError:
        print "Exception raised: subprocess.CalledProcessError.output"

    del mydisplay

    return None



def addSmartDns():
    dns1=''
    dns2=''

    if dnsprov == '3':
        dns1=settings.getSetting('dns-serv-ip-1')
        dns2=settings.getSetting('dns-serv-ip-2')
    elif dnsprov == '0':
        dns1 = '103.1.187.68'
        dns2 = '54.252.112.136'
    elif dnsprov == '1':
        dns1 = '223.252.47.50'
        dns2 = '54.252.112.136'
    elif dnsprov == '2':
        dns1 = '118.88.19.172'
        dns2 = '54.252.112.136'
    elif dnsprov == '4':
        setupDns(None,None)

        #dns2 = None
        dnslist = updateMGServers()
        if len(dnslist) == 1:
            dns1 = dnslist[0]
            dns2 = None
        elif len(dnslist) == 2:
            dns1 = dnslist[0]
            dns2 = dnslist[1]

        if dns1 is None:
            #dialog = xbmcgui.Dialog()
            #dialog.notification("Smart DNS Settings", "MG Plus: Could not add user, left on default DNS")
            return
    elif dnsprov == '6':
        dns1 = '8.8.4.4'
        dns2 = '8.8.8.8'







    if (dns1=='') or (dns1=='0.0.0.0'):
        dns1=None
    if (dns2=='') or (dns2=='0.0.0.0'):
        dns2=None

    setupDns(dns1,dns2)




def setupDns(dns1,dns2):
    p = subprocess.Popen(["connmanctl", "services"], stdout=subprocess.PIPE)
    services=p.communicate()[0]

    activeServices=(re.compile('(^\*A[OR].*)', re.M).findall(services))

    for actServ in activeServices:
        connection=actServ.split()[2]


        p = subprocess.Popen(["connmanctl", "services", connection], stdout=subprocess.PIPE)


        details=p.communicate()[0]

        currDns=(re.compile('Nameservers = \[ (.+?) \]').findall(details)[0])

        connectionType=connection.split('_')[0]
        if connectionType=='wifi':
            connectionType+=' ('+actServ.split()[1]+")"

        #dialog = xbmcgui.Dialog();
        #dialog.notification("IP details - "+connectionType, currDns);

        eachDns = currDns.split(', ')
        totalDns = len(eachDns)

        updatedns1=False
        updatedns2=False
        reset=False

        if dns1 is None and dns2 is None:
            reset=True
        elif totalDns==1:
            if (not dns1 is None) and (dns2 is None):
                if not dns1==eachDns[0].strip():
                    updatedns1=True
            else:
                updatedns1=True
                updatedns2=True
        elif totalDns==2:
            if (not dns1==eachDns[0].strip()) or (not dns2==eachDns[1].strip()):
                    updatedns1=True
                    if not dns2 is None:
                        updatedns2=True
        else:
            updatedns1=True
            if not dns2 is None:
                updatedns2=True


        if reset:
            p = subprocess.Popen(["connmanctl", "config", connection, "--nameservers"], stdout=subprocess.PIPE)
            dialog = xbmcgui.Dialog()
            dialog.notification("Smart DNS Settings - "+connectionType, "Cleared settings to default.")
        elif updatedns1 and not updatedns2:
            p = subprocess.Popen(["connmanctl", "config", connection, "--nameservers", dns1], stdout=subprocess.PIPE)
            dialog = xbmcgui.Dialog()
            if dnsprov == '4':
                dialog.notification("Smart DNS Settings - "+connectionType, "Updated... MG Plus DNS set")
            else:
                dialog.notification("Smart DNS Settings - "+connectionType, "Updated... Now set to: "+dns1)
        elif updatedns1 and updatedns2:
            print ("conn: "+connection)
            print(" dns1:"+dns1)
            print(" dns2: "+dns2)
            p = subprocess.Popen(["connmanctl", "config", connection, "--nameservers", dns1, dns2], stdout=subprocess.PIPE)
            dialog = xbmcgui.Dialog()
            if dnsprov == '4':
                dialog.notification("Smart DNS Settings - "+connectionType, "Updated... MG Plus DNS set")
            else:
                dialog.notification("Smart DNS Settings - "+connectionType, "Updated... Now set to: "+dns1+" and "+dns2)
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification("Smart DNS Settings - "+connectionType, "No changes required - already set")


