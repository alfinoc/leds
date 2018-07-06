from flask import Flask, request, render_template, redirect, url_for, g as global_context
from json import loads
from frames import Player, Frame, StripController
import time

# TODO: make threadsafe
player = Player(StripController())
app = Flask(__name__)

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
