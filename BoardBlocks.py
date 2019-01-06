from PIL import Image
import gameconfig

class BoardBlocks(object):

    def __init__(self):
        self.blocked_blocks = []

    def load_level(self, path_to_lvl):
        
        img = Image.open(path_to_lvl)

        x = int((img.size[0] - 50) / 10)
        y = int((img.size[1] - 50) / 10)
        for xx in range(x):
            for yy in range(y):
                if img.getpixel((xx*10+25+5, yy*10+25+5)) == (0,0,0):
                    self.blocked_blocks.append((xx,yy))

    #@staticmethod
    @classmethod
    def load_level2(cls, path_to_lvl):
        
        img = Image.open(path_to_lvl)
        blocked_blocks = []
        x = int((img.size[0] - 50) / 10)
        y = int((img.size[1] - 50) / 10)
        for xx in range(x):
            for yy in range(y):
                if img.getpixel((xx*10+25+5, yy*10+25+5)) == (0,0,0):
                    blocked_blocks.append((xx,yy))
        return img.size[0], img.size[1], blocked_blocks



if __name__ == '__main__':
    bb = BoardBlocks()
    bb.load_level(gameconfig.level_name)
