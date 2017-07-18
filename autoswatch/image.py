import PIL

class Image:
    def __init__(self, size=(20,20), color='#ffffff', image_mode='RGB', image_format='PNG'):
        # ^#(?:[0-9a-fA-F]{1,2}){3}$ <-- Hex color code def…

        self.size   = size
        self.color  = color
        self.mode   = image_mode
        self.format = image_format

