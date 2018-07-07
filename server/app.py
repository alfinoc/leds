from flask import Flask, request, render_template, redirect, url_for, g as global_context, send_from_directory
from json import loads
from frames import Player, Frame, StripController
from jinja2 import Environment, FileSystemLoader

PERMANENT_FRAME_INTERVAL = 60 * 60 # 1hr

player = Player(StripController())
app = Flask(__name__, static_url_path='/static')

@app.route('/static/<path:path>')
def sendStatic(path):
  return send_from_directory('static', path)

@app.route('/display_frame', methods=['POST'])
def displayFrame():
  player.stop()
  player.play([Frame(loads(request.data)['frame'], PERMANENT_FRAME_INTERVAL)])
  return 'ok'

@app.route('/play_frames')
def playFrames():
  base = [
    Frame([[0,0,0], [0,0,0], [0,0,0]], 1),
    Frame([[0,0,0], [1,0,0], [0,0,0]], 2),
    Frame([[0,0,0], [1,1,0], [0,0,0]], 1),
    Frame([[0,0,0], [1,1,1], [0,0,0]], 1)
  ]
  reversed = base[:]
  reversed.reverse()

  player.play(base + reversed + base + reversed)
  return 'playing'

@app.route('/play_reset')
def playPreset():
  return 'unimplemented'

@app.route('/stop')
def stop():
  player.stop()
  return 'stop'

if __name__ == "__main__":
  app.run(debug=True)
