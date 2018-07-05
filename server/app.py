from flask import Flask, request, render_template, redirect, url_for
from json import loads
from frames import Frames
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
  return 'unimplemented'

@app.route('/play_reset')
def playPreset():
  return 'unimplemented'

@app.route('/reset')
def stop():
  return 'unimplemented'

if __name__ == "__main__":
  app.run(debug=True)
