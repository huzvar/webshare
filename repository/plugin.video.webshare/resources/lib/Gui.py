import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

from urllib.parse import urlencode
from xml.etree import ElementTree

from resources.lib.WebshareAPI import WebshareAPI

NONE_WHAT = '%#NONE#%'

class Gui:
  def __init__(self, url: str, handle: int):
    self._url = url
    self._handle = handle

    self._addon = xbmcaddon.Addon()
    self._api = None

    self._api = WebshareAPI()

    self._lists = [
      {'name': "Star Wars - Dobrodruzstvi mladych Jediu", 'search': "Star Wars - Dobrodruzstvi mladych Jediu", 'pattern': "^Star Wars - Dobrodruzstvi mladych Jediu"},

      {'name': "Mandalorian", 'search': "Mandalorian", 'pattern': "^Mandalorian"},
      {'name': "MASH", 'search': "M.A.S.H.EP", 'pattern': "^M\.A\.S\.H\.EP"},
    ]

  def _get_url(self, **kwargs):
    return '{0}?{1}'.format(self._url, urlencode(kwargs, 'utf-8'))

  def _notification(self, message, icon = xbmcgui.NOTIFICATION_INFO, sound = False):
      xbmcgui.Dialog().notification(self._addon.getAddonInfo('name'), message, icon, 3000, sound)
  
  def Token(self) -> bool:
    token = self._addon.getSetting('token')

    # token not exists
    if not token:
      username = self._addon.getSetting('wsuser')
      password = self._addon.getSetting('wspass')

      if not (username and password):
        self._notification(self._addon.getLocalizedString(30101), sound = True)

        self._addon.openSettings()

        return False

      # login
      token = self._api.login(username, password)

      if token:
        self._addon.setSetting('token', token)

      else:
        self._notification(self._addon.getLocalizedString(30102), icon = xbmcgui.NOTIFICATION_ERROR, sound = True)

        self._addon.openSettings()

        return False

    # check VIP account
    xml = self._api.user_data(token)

    vip = xml.find('vip').text

    if vip != "1":
      self._notification(self._addon.getLocalizedString(30103), icon = xbmcgui.NOTIFICATION_WARNING)

      return False

    return True


  # TODO: zistit
  def fpsize(self, fps):
    x = round(float(fps),3)
    if int(x) == x:
       return str(int(x))
    return str(x)

  def _ShowList(self, data):
      # if offset > 0: #prev page
      #     list_item = xbmcgui.ListItem(label=_addon.getLocalizedString(30206))
      #     list_item.setArt({'icon': 'DefaultAddonsSearch.png'})
      #     xbmcplugin.addDirectoryItem(_handle, _get_url(action=action, what=what, category=category, sort=sort, limit=limit, offset=offset - limit if offset > limit else 0), list_item, True)
          
      for file in data['file']:
        list_item = xbmcgui.ListItem(label = file['name'] + ' (' + file['size'] + ')')

        if 'img' in file:
          list_item.setArt({'thumb': file['img']})

        list_item.setInfo('video', {
          'title': file['name'],
          'plot': self._addon.getLocalizedString(30501) + file['size']
        })

        text = self._addon.getLocalizedString(30501)

        xbmc.log(f"SEARCH: what = {text}", level=xbmc.LOGDEBUG)

        list_item.setProperty('IsPlayable', 'true')

        commands = [
          (self._addon.getLocalizedString(30211), 'RunPlugin(' + self._get_url(action='info', ident=file['ident']) + ')')
        ]

        list_item.addContextMenuItems(commands)

        xbmcplugin.addDirectoryItem(self._handle, self._get_url(action = 'play', ident = file['ident'], name = file['name']), list_item, False)
      
      # try:
      #   total = int(xml.find('total').text)
      # except:
      #   total = 0
          
      # if offset + limit < total: #next page
      #   list_item = xbmcgui.ListItem(label=_addon.getLocalizedString(30207))
      #   list_item.setArt({'icon': 'DefaultAddonsSearch.png'})
      #   xbmcplugin.addDirectoryItem(_handle, _get_url(action=action, what=what, category=category, sort=sort, limit=limit, offset=offset+limit), list_item, True)
      # else:
      #   popinfo(_addon.getLocalizedString(30107), icon=xbmcgui.NOTIFICATION_WARNING)


  
  def Info(self, params):
    data = self._api.file_info(params['ident'])
    
    if data:
      text = ""

      for key, value in data.items():
        if value is None:
          value = ""

        elif not isinstance(value, str):
          value = str(value)
      
        text += key + ": " + value + "\n"

      xbmcgui.Dialog().textviewer(self._addon.getAddonInfo('name'), text)

    else:
      self._notification(self._addon.getLocalizedString(30107), icon = xbmcgui.NOTIFICATION_WARNING)

  def List(self, params):
    index = int(params['index'])

    if 0 <= index < len(self._lists): 
      list = self._lists[index]

      xbmcplugin.setPluginCategory(self._handle, self._addon.getAddonInfo('name') + " \ " + self._addon.getLocalizedString(30201))
      
      data = self._api.VideoList(list['search'], list['pattern'])

      self._ShowList(data)
  
    else:
      #  TODO: upravit spravu
      self._notification(self._addon.getLocalizedString(30107), icon = xbmcgui.NOTIFICATION_WARNING)

    xbmcplugin.endOfDirectory(self._handle)

  def Menu(self):
    xbmcplugin.setPluginCategory(self._handle, self._addon.getAddonInfo('name'))

    # search
    list_item = xbmcgui.ListItem(label = self._addon.getLocalizedString(30201))
    list_item.setArt({'icon': 'DefaultAddonsSearch.png'})

    xbmcplugin.addDirectoryItem(self._handle, self._get_url(action = "search"), list_item, True)
    
    # lists
    for index, list in enumerate(self._lists):
      list_item = xbmcgui.ListItem(label = list['name'])
      list_item.setArt({'icon': 'DefaultPlaylist.png'})

      xbmcplugin.addDirectoryItem(self._handle, self._get_url(action = "list", index = index), list_item, True)
    
    xbmcplugin.endOfDirectory(self._handle)

  def Play(self, params):
    link = self._api.file_link(params['ident'])

    if link:
      list_item = xbmcgui.ListItem(label = params['name'], path = link)
      list_item.setProperty('mimetype', 'application/octet-stream')

      xbmcplugin.setResolvedUrl(self._handle, True, list_item)

    else:
      self._notification(self._addon.getLocalizedString(30107), icon = xbmcgui.NOTIFICATION_WARNING)

      xbmcplugin.setResolvedUrl(self._handle, False, xbmcgui.ListItem())

  def Search(self, params):
    updateListing = False

    xbmcplugin.setPluginCategory(self._handle, self._addon.getAddonInfo('name') + " \ " + self._addon.getLocalizedString(30201))
    
    what = ""
    
    if 'what' in params:
      what = params['what']
    
    what_last = self._addon.getSetting('what_last')

    if what_last != what:
      keyboard = xbmc.Keyboard(what_last, self._addon.getLocalizedString(30007))
      keyboard.doModal()

      if keyboard.isConfirmed():
        what = keyboard.getText()

        updateListing=True

    # check wath
    if what:
      xbmc.log(f"SEARCH: what = {what}", level=xbmc.LOGDEBUG)

      self._addon.setSetting('what_last', what)

      # if 'offset' not in params:
      #   self._addon.setSetting('what_last', what)

      # else:
      #   self._addon.setSetting('what_last', NONE_WHAT)
      #   updateListing=True

      offset = 0

      # call search
      data = self._api.search(what, offset=offset)

      self._ShowList(data)
  
    xbmcplugin.endOfDirectory(self._handle, updateListing = updateListing)
