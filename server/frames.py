import time
from neopixel import Adafruit_NeoPixel, Color

BLACK = Color(0, 0, 0)

class StripController:
  def __init__(self):
    self.ledCount_ = 100
    self.height_ = 10
    self.neopixel_ = Adafruit_NeoPixel(
        self.ledCount_,  # LED count
        18,  # LED pin
        800000,  # LED signal frequency (Hz)
        10,  # DMA channel
        False,  # Invert signal
        100,  # Brightness (0, 255)
        0)  # LED channel
    self.neopixel_.begin()

  def set(self, index, color):
    if index >= self.ledCount_:
      raise 'setting out of bounds pixel', index
    self.neopixel_.setPixelColor(index, color)

  def show(self):
    self.neopixel_.show()

  def cleanUpGrid(self):
    width = self.ledCount_ / self.height_
    return [[BLACK for j in range(0, width)] for i in range(0, self.height_)]

class MockStripController:
  def __init__(self):
    pass

  def set(self, index, color):
    pass

  def show(self):
    pass

class Frame:
  def __init__(self, grid, interval):
    self.grid_ = grid
    self.interval_ = interval

    if set([len(row) for row self.grid_]) != 1:
      raise 'inconsistent row lengths in frame', self.grid_

  def interval(self):
    return self.interval_

  def write(self, controller):
    index = 0
    for row in self.grid_:
      for pixel in row:
        controller.set(index, pixel)
    controller.show()

  def cleanUp(controller):
    return Frame(controller.cleanUpGrid()).write(controller)

class PlayableFrames:
  def __init__(self, frames):
    self.frames_ = frames
    self.currentFrameIndex_ = -1
    self.successorTimer_ = None

    # Clear the grid upon completion of all frames.
    self.frames_append(Frame.cleanUp(controller))

  def play(self, controller):
    # Bootstrap by playing first frame at no delay.
    if self.currentFrameIndex_ == -1:
      delay = 0
    else:
      delay = self.frames_[self.currentFrameIndex_ - 1].getInterval()
    return Timer(delay, self.writeAndEnqueSuccessor_(controller))

  def writeAndEnqueSuccessor_(self, controller):
    self.currentFrameIndex_ += 1
    self.frames_[self.currentFrameIndex_].write(controller)

    # On the last frame, avoid enqueuing a successor.
    if currentFrameIndex_ >= len(self.currentFrameIndex_) - 1:
      self.successorTimer_ = None
    else:
      self.successorTimer_ = self.playNextFrame_(controller)

  def stop(self):
    if self.successorTimer_ != None:
      self.successorTimer_.cancel()
