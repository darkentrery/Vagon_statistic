from PIL import Image, ImageDraw, ImageFont
from Occupation_tracks import vars, Trains
from tracks import tracks
k = 5
x = 420*k
y = 297*k
black = (0, 0, 0)
red = (255, 0, 0)
lime = (0, 255, 0)
blue = (0, 0 ,255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
olive = (128, 128, 0)
colors = [red, lime, blue, yellow, cyan, magenta, olive]
#30 pixels per hour/ 0.5 pixels per 1 minute
#50 pixels per track
font = ImageFont.truetype('arial.ttf', 8*k)
font_2 = ImageFont.truetype('arial.ttf', 4*k)
image = Image.new("RGB", (x, y), (255, 255, 255))
draw = ImageDraw.Draw(image)
key_track = list(tracks.keys())
key_train = list(Trains.keys())
print(key_train)
#Draw vertical and gorizontal lines
def draw_grid():
    for t in range (13):
        draw.line((20*k+t*k*30, 20*k, 20*k+t*k*30, 20*k+len(tracks)*k*50), black, 5)
        draw.text((20*k+t*k*30-10, 10*k), str(t), black, font)
        if t < 12:
            draw.line((20 * k+k*15 + t * k * 30, 20 * k, 20 * k+k*15 + t * k * 30, 20 * k + len(tracks) * k * 50), black, 2)

    print(key_track)
    for t in range (len(tracks)+1):
        draw.line((20*k, 20*k + t*k*10, 20*k+360*k, 20*k+t*k*10), black, 5)
        if t < len(tracks):
            draw.text((10 * k, 20*k + t*k*10), str(key_track[t]), black, font)

def draw_variants():
    i = 0
    #for v in range(len(vars)):
    for v in range(2):

        #if v == '1':
        for t in range (len(vars[str(v)])):
            draw.line((20 * k+int(0.5*k*Trains[key_train[t]][0]), 20*k+int(10*k*key_track.index(vars[str(v)][t])
            )+5*k+i, 20 * k+int(0.5*k*Trains[key_train[t]][1]), 20*k+int(10*k*key_track.index(vars[str(v)][t]))+5*k+i), colors[v], 5)
            draw.text((20 * k + int(0.5*k*Trains[key_train[t]][0]), 15*k+int(10*k*key_track.index(vars[str(v)][t])
            )+5*k+i), str(key_train[t]), colors[v], font_2)
        i += 5 * k



draw_grid()
draw_variants()
image.show()
