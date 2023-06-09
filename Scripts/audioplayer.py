import aud

class AudioPlayer:
    def __init__(self, volume: int=1.0):
        self.device = aud.Device()
        self.buffer = None
        self.volume = volume
        self.handle = None
    
    def load(self, filename: str):
        self.buffer = aud.Sound(filename)
    
    def play(self):
        if self.buffer is not None:
            self.handle = self.device.play(self.buffer)
    
    def stop(self):
        if self.handle is not None:
            self.handle.stop()
    
    def set_volume(self, volume: int):
        self.volume = volume
        if self.handle is not None:
            self.handle.volume = self.volume
    
    def get_volume(self):
        return self.volume, self.device.volume