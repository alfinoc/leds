from flask import Flask, request, render_template, redirect, url_for
from json import loads
from frames import PlayableFrames, Frame, StripController
import time

app = Flask(__name__)

"""
render_template('charts.html', charts=model, user=user)

@app.template_filter('format_date')
def format_date(timestamp):
  return datetime.fromtimestamp(int(timestamp)).strftime('%b %d')
"""

@app.route('/play_frames')
def playFrames():
  controller = StripController()
  frames = PlayableFrames(controller, [
    Frame([[0,0,0], [0,0,0], [0,0,0]], 1),
    Frame([[0,0,0], [1,0,0], [0,0,0]], 2),
    Frame([[0,0,0], [1,1,0], [0,0,0]], 1),
    Frame([[0,0,0], [1,1,1], [0,0,0]], 1)
  ])
  frames.play()
  return 'playing'

@app.route('/play_reset')
def playPreset():
  return 'unimplemented'

@app.route('/reset')
def stop():
  return 'unimplemented'

if __name__ == "__main__":
  app.run(debug=True)
