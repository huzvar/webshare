import json
import xml.dom.minidom as minidom
import sys

from xml.etree import ElementTree

sys.path.append("repository/plugin.video.webshare/")

from resources.lib.WebshareAPI import WebshareAPI

def pretty_xml(xml: ElementTree) -> str:
  xml_string = ElementTree.tostring(xml, encoding='utf-8')
  xml_minidom = minidom.parseString(xml_string)

  return xml_minidom.toprettyxml(indent="  ")

if __name__ == '__main__':
  api = WebshareAPI()
  api.login("levik0", "ASDqwe123")

  search = "Mandalorian"

  # xml = api.user_data()
  # print("xxx ", ElementTree.tostring(xml, encoding='unicode'))

  # search
  # print(json.dumps(api.search(search), indent = 2))

  # data = api.search(search, limit=1000)
  
  # print(data['total'])

  # for file in data['file']:
  #   print(file['name'])

  # similar_files
  # print(json.dumps(api.similar_files(search), indent = 2))

  # file_info
  # print(json.dumps(api.file_info("F3MbHDN2j8"), indent = 2))


  # print(json.dumps(api.VideoList(search, "^" + search), indent = 2))
  print(json.dumps(api.VideoList("M.A.S.H.EP", "^M\\.A\\.S\\.H\\.EP"), indent = 2))

  # data = api.VideoList(search, "^" + search)
  
  # for file in data['file']:
  #   print(file['name'])
