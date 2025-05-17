import sys

from urllib.parse import parse_qsl

from resources.lib.Gui import Gui

if __name__ == '__main__':
  params = dict(parse_qsl(sys.argv[2][1:]))

  gui = Gui(sys.argv[0], int(sys.argv[1]))

  # valid token and account
  while True:
    if gui.Token():
      break

  if params:
    if params['action'] == "search":
      gui.Search(params)

    elif params['action'] == "list":
      gui.List(params)

    elif params['action'] == "info":
      gui.Info(params)

    elif params['action'] == "play":
      gui.Play(params)

    else:
      gui.Menu()

  else:
    gui.Menu()
