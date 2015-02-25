import mg_common, xbmcaddon

addon_id='plugin.program.smartdns'

settings=xbmcaddon.Addon(id=addon_id)

dnsprov=settings.getSetting('dns-provider')
mg_common.addSmartDns()
