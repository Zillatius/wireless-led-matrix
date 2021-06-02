import framebuf
def slim(symbol):
    buf = bytearray(4)
    lettr = framebuf.FrameBuffer(buf, 4, 8, framebuf.MONO_HLSB)
    if symbol == 1:
        lettr.line(2,0,0,2,1)
        lettr.line(2,0,2,6,1)
    if symbol == 2:
        lettr.rect(-1,0,4,4,1)
        lettr.rect(0,3,4,4,1)
        lettr.vline(3,3,5,0)
    if symbol == 3:
        lettr.rect(-1,0,4,4,1)
        lettr.rect(-1,3,4,4,1)
    if symbol == 4:
        lettr.rect(0,-1,3,5,1)
        lettr.vline(2,4,3,1)
    if symbol == 5:
        lettr.rect(0,0,4,4,1)
        lettr.rect(-1,3,4,4,1)
        lettr.vline(3,0,5,0)
    if symbol == 6:
        lettr.rect(0,0,4,4,1)
        lettr.rect(0,3,3,4,1)
        lettr.vline(3,0,5,0)
    if symbol == 7:
        lettr.hline(0,0,3,1)
        lettr.line(2,1,0,3,1)
        lettr.vline(0,4,3,1)
    if symbol == 8:
        lettr.rect(0,0,3,4,1)
        lettr.rect(0,3,3,4,1)
    if symbol == 9:
        lettr.rect(0,0,3,4,1)
        lettr.rect(-1,3,4,4,1)
    if symbol == 0:
        lettr.rect(0,0,3,7,1)
    if symbol == "deg":
        lettr.rect(1,0,2,2,1)
    if symbol == "C":
        lettr.rect(0,0,4,7,1)
        lettr.vline(3,0,8,0)
    return lettr