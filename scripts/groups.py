import json
import os
import re
import xml.dom.minidom as minidom
import sys

from xml.etree import ElementTree

sys.path.append("../repository/plugin.video.webshare/")

from resources.lib.WebshareAPI import WebshareAPI

if __name__ == '__main__':
  api = WebshareAPI()
  api.login("levik0", "ASDqwe123")

  search = "house"

  names = []

  # search
  data = api.search(search, limit=10000)
  
  print(data['total'])

  for file in data['file']:
    name = os.path.splitext(file['name'])[0]
    name = name.lower()

    # nahrad znaky za bodku
    name = re.sub(r"[\s\-_,\.\+]+", ".", name)

    # odstran to co je v zatvorkach
    name = re.sub(r"\([\w\.]+\)|\[[\w\.]+\]|\{[\w\.]+\}", "", name)

    # odstran metadata
    name = re.sub(r"\.(h\.?264|1080p|2160p|x26[45]|hevc|4k|hdr|avc)", "", name)
    name = re.sub(r"\.(5\.1\.atmos|ac3.5.1|5.1|dts|ac3|eac3)", "", name)
    name = re.sub(r"\.(cz|en|dab)", "", name)

    # blud
    name = re.sub(r"\.(web|bluray|5.1cz|sub|ddp5.1.dual.alfahd|titulky|xvid|dvdrip)", "", name)

    # odstran rok
    name = re.sub(r"\.[12]\d{3}", "", name)

    # cistenie botiek
    name = re.sub(r"(\.{2,})", ".", name)
    name = re.sub(r"(\.$)", "", name)

    # orezanie po cisle
    name = re.sub(r"\.\d.*$", "", name)
    name = re.sub(r"\.s\d{2}e\d{2}.*$", "", name)
    name = re.sub(r"\.i+$", "", name)

    names.append(name)

  names = list(set(names))

  print(json.dumps(names, indent = 2))
