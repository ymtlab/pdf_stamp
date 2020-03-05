import math
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import red
from reportlab.pdfbase.ttfonts import TTFont

def circle_stamp(stamp_name, paper_size, stamp_size, stamp_coordinate, texts):
    c = canvas.Canvas(stamp_name)
    c.setPageSize(paper_size)
    c.setStrokeColor(red)
    
    rx, ry = stamp_size[0]/2.0, stamp_size[1]/2.0
    draw_circle(c, stamp_coordinate[0], stamp_coordinate[1], rx, ry)
    c.setStrokeColor(red)
    draw_upper_line(c, stamp_coordinate[0], stamp_coordinate[1], rx, ry)
    draw_lower_line(c, stamp_coordinate[0], stamp_coordinate[1], rx, ry)
    draw_string(c, stamp_coordinate[0], stamp_coordinate[1], ry, texts)

    c.save()
    return c

def draw_circle(c, xc, yc, rx, ry):
    c.setStrokeColor(red)
    c.ellipse(xc-rx, yc-ry, xc+rx, yc+ry)

def draw_upper_line(c, xc, yc, rx, ry):
    y = ry / 3.0
    t = math.asin(1.0/3.0)
    x = rx * math.cos(t)
    c.line(xc + x, yc + y, xc - x, yc + y)

def draw_lower_line(c, xc, yc, rx, ry):
    y = -1.0 * ry / 3.0
    t = math.asin(1.0/3.0)
    x = rx * math.cos(t)
    c.line(xc + x, yc + y, xc - x, yc + y)

def draw_string(c, xc, yc, ry, texts):
    c.setFillColor(red)
    text = texts[0]
    fp, fs, s = text['font_path'], text['font_size'], text['text']
    pdfmetrics.registerFont(TTFont(fp.stem, str(fp)))
    c.setFont(fp.stem, fs)
    c.drawCentredString(xc, yc-fs*0.6+10.0*ry/15.0, s)
    
    text = texts[1]
    fp, fs, s = text['font_path'], text['font_size'], text['text']
    pdfmetrics.registerFont(TTFont(fp.stem, str(fp)))
    c.setFont(fp.stem, fs)
    c.drawCentredString(xc, yc-fs*0.6+1.0, s)
    
    text = texts[2]
    fp, fs, s = text['font_path'], text['font_size'], text['text']
    pdfmetrics.registerFont(TTFont(fp.stem, str(fp)))
    c.setFont(fp.stem, fs)
    c.drawCentredString(xc, yc-fs*0.6-7.5*ry/15.0, s)

if __name__ == '__main__':
    texts = [
        {'font_path':Path('C:/Windows/Fonts/msgothic.ttc'), 'font_size':6.5, 'text':'test1'},
        {'font_path':Path('C:/Windows/Fonts/msgothic.ttc'), 'font_size':5.0, 'text':'2020/03/04'},
        {'font_path':Path('C:/Windows/Fonts/msgothic.ttc'), 'font_size':6.5, 'text':'test2'}
    ]
    
    circle_stamp('__test__.pdf', (595.276, 841.89), (10, 10), (200, 400), texts)
