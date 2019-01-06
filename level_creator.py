from PIL import Image, ImageDraw
import numpy as np
x = 100
y = 100
n = x*10+50
m = y*10+50

img = Image.new('RGB', (n,m), (150, 150, 150))

draw = ImageDraw.Draw(img)

xx = 10*10+25
yy = 10*10+25

for xx in range(x):
    for yy in range(y):
        if (xx == 0) and (yy < 30):
            draw.rectangle(((xx*10+25, yy*10+25), (xx*10+34, yy*10+34)), fill="red")
            draw.rectangle(((xx*10+25+1, yy*10+25+1), (xx*10+34-1, yy*10+34-1)), fill="black")            
        else:
            draw.rectangle(((xx*10+25, yy*10+25), (xx*10+34, yy*10+34)), fill="red")
            draw.rectangle(((xx*10+25+1, yy*10+25+1), (xx*10+34-1, yy*10+34-1)), fill="white")

img.save("ima.bmp", "bmp")



