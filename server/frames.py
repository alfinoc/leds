from neopixel import Adafruit_NeoPixel, Color
from threading import Timer

BLACK = Color(0, 0, 0)

class StripController:
  def __init__(self):
    self.ledCount_ = 9 # 100
    self.height_ = 3 # 10
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
      raise Exception('setting out of bounds pixel', index)
    self.neopixel_.setPixelColor(index, color)

  def show(self):
    self.neopixel_.show()

  def cleanUpGrid(self):
    width = self.ledCount_ / self.height_
    return [[BLACK] * width] * self.height_

class Frame:
  def __init__(self, grid, interval):
    self.grid_ = grid
    self.interval_ = interval

    if len(set([len(row) for row in self.grid_])) != 1:
      raise Exception('inconsistent row lengths in frame', self.grid_)

  def interval(self):
    return self.interval_

  def write(self, controller):
    index = 0
    for row in self.grid_:
      for pixel in row:
        controller.set(index, pixel)
        index += 1
    controller.show()

class PlayableFrames:
  def __init__(self, controller, frames):
    self.controller_ = controller
    self.frames_ = frames
    self.currentFrameIndex_ = -1
    self.successorTimer_ = None

    # Clear the grid upon completion of all frames.
    self.frames_.append(Frame(controller.cleanUpGrid(), 0))

  def play(self):
    self.playNextFrame_().start()

  def playNextFrame_(self):
    # Bootstrap by playing first frame at no delay.
    if self.currentFrameIndex_ == -1:
      delay = 0
    else:
      delay = self.frames_[self.currentFrameIndex_ - 1].interval()
    return Timer(delay, self.writeAndEnqueSuccessor_)

  def writeAndEnqueSuccessor_(self):
    self.currentFrameIndex_ += 1
    self.frames_[self.currentFrameIndex_].write(self.controller_)

    # On the last frame, avoid enqueuing a successor.
    if self.currentFrameIndex_ >= len(self.frames_) - 1:
      self.reset_()
    else:
      self.successorTimer_ = self.playNextFrame_()
      self.successorTimer_.start()

  def stop(self, reset=False):
    if self.successorTimer_ != None:
      self.successorTimer_.cancel()
      self.currentFrameIndex_ -= 1

      if reset:
        self.reset_()

  def reset_(self):
    self.currentFrameIndex_ = -1
    self.successorTimer_ = None
