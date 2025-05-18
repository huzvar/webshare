# https://webshare.cz/apidoc/

import hashlib
import math
import re
import requests
import uuid

from xml.etree import ElementTree

from resources.lib.md5crypt import md5crypt

class WebshareAPI:
  def __init__(self):
    self._base_url = "https://webshare.cz/api/"
    self._username = None
    self._password = None
    self._password_encrypted = None
    self._password_digest = None
    self._token = None
    self._devoce_uuid = str(uuid.uuid4())

    self._session = requests.Session()
    # {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    self._session.headers.update({'User-Agent': "UA", 'Referer': "BASE"})

  def _format_size(self, size_string: str, units=["B", "KB", "MB", "GB"]):
    if size_string:
      size = float(size_string)
      
      for i, unit in enumerate(units):
        if size < 1024:
          if i == 0:
            return f"{int(size)} {unit}"
  
          else:
            return f"{round(size, 2)} {unit}"
      
        size /= 1024
    
    return size_string

  def _salt(self):
    # check input
    assert self._username

    # call
    response = self._session.post(self._base_url + "salt/", {
      'username_or_email': self._username,
    })

    # check call
    assert(response.status_code == 200)

    xml = ElementTree.fromstring(response.content)

    # check data
    assert xml.find('status').text == "OK"
    
    salt = xml.find('salt').text

    # check salt
    assert salt

    self._password_encrypted = hashlib.sha1(md5crypt(self._password.encode('utf-8'), salt.encode('utf-8')).encode('utf-8')).hexdigest()
    self._password_digest = hashlib.md5(self._username.encode('utf-8') + ":Webshare:".encode('utf-8') + self._password_encrypted.encode('utf-8')).hexdigest()

    return

  def _to_dict(self, xml, skip=[]) -> dict:
    result = {}

    for element in xml:
      if element.tag in skip:
        continue

      if len(list(element)) == 0:
        value = element.text

      else:
        value = self._to_dict(element, skip)

      if element.tag in result:
        if isinstance(result[element.tag], list):
          result[element.tag].append(value)
  
        else:
          result[element.tag] = [result[element.tag], value]
  
      else:
        result[element.tag] = value

    return result

  def file_info(self, ident: str) -> dict:
    # check input
    assert self._token

    # call
    response = self._session.post(self._base_url + "file_info/", {
      'ident': ident,
      'wst': self._token,
      'maybe_removed': "true",
    })

    # check call
    assert(response.status_code == 200)

    xml = ElementTree.fromstring(response.content)

    # check data
    assert xml.find('status').text == "OK"

    return self._to_dict(xml)

  def file_link(self, ident: str) -> str:
    # check input
    assert self._token

    # call
    response = self._session.post(self._base_url + "file_link/", {
      'ident': ident,
      'download_type': "video_stream",
      'device_uuid': self._devoce_uuid,
      'wst': self._token,
    })

    # check call
    assert(response.status_code == 200)

    xml = ElementTree.fromstring(response.content)

    # check data
    assert xml.find('status').text == "OK"

    link = xml.find('link').text

    # check link
    assert link

    return link

  def login(self, username: str, password: str) -> str:
    # check input
    if not (username or password):
      return None
    
    # changed
    if self._username != username or self._password != password:
      self._username = username
      self._password = password

      self._salt()

    # call
    response = self._session.post(self._base_url + "login/", {
      'username_or_email': self._username,
      'password': self._password_encrypted,
      'digest': self._password_digest,
      'keep_logged_in': 1,
    })

    # check call
    assert(response.status_code == 200)

    xml = ElementTree.fromstring(response.content)

    # check data
    assert xml.find('status').text == "OK"

    self._token = xml.find('token').text

    # check token
    assert self._token

    return self._token

  def search(self, what: str, limit: int = 10, offset: int = 0, sort: str = 'largest') -> dict:
    # check input
    assert self._token

    # call
    response = self._session.post(self._base_url + "search/", {
      'category': "video",
      'what': what.encode('utf-8'),
      'sort': sort,
      'limit': limit,
      'offset': offset,
      'wst': self._token,
      'maybe_removed': "true",
    })

    # check call
    assert(response.status_code == 200)

    xml = ElementTree.fromstring(response.content)

    # check data
    assert xml.find('status').text == "OK"

    return self._to_dict(xml)

  def similar_files(self, what: str, sort: str = "largest", limit: int = 10, offset: int = 0) -> dict:
    # check input
    assert self._token

    # call
    response = self._session.post(self._base_url + "similar_files/", {
      'category': "video",
      'what': what.encode('utf-8'),
      'sort': sort,
      'limit': limit,
      'offset': offset,
      'wst': self._token,
      'maybe_removed': "true",
    })

    # check call
    assert(response.status_code == 200)

    xml = ElementTree.fromstring(response.content)

    # check data
    assert xml.find('status').text == "OK"

    data = self._to_dict(xml)
    
    return data

  def user_data(self, token) -> ElementTree:
    # check input
    assert token

    self._token = token

    # call
    response = self._session.post(self._base_url + "user_data/", {
      'wst': self._token,
    })

    # check call
    assert(response.status_code == 200)

    xml = ElementTree.fromstring(response.content)

    # check data
    assert xml.find('status').text == "OK"

    # print("xxx ", ElementTree.tostring(xml, encoding='unicode'))

    return xml

  def VideoList(self, search: str, pattern: str, page: int = 1, page_limit: int = 25) -> dict:
    if not (0 < page_limit <= 100): 
      page_limit = 25

    data = self.search(search, limit = 200)

    filtered_data = []

    for item in data['file']:
      if re.match(pattern, item['name']):
        item['size'] = self._format_size(item['size'])

        filtered_data.append(item)

    sorted_data = sorted(filtered_data, key=lambda x: x["name"])

    # check page
    if not (0 < page <= math.ceil(len(sorted_data) / page_limit)):
      page = 1

    return {
      'total': len(sorted_data),
      'page': page,
      'pages_count': math.ceil(len(sorted_data) / page_limit),
      'file': sorted_data[((page - 1) * page_limit):(page * page_limit)],
    }
