#coding=utf8

from PIL import Image
import argparse



ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    # 灰度公式
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    length = len(ascii_char)
    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('-o','--output')
    parser.add_argument('--height', type=int, default=80)
    parser.add_argument('--width', type=int, default=80)
    args = parser.parse_args()
    IMG = args.file
    OUTPUT = args.output
    WIDTH = args.width
    HEIGHT = args.height

    text = ''
    img = Image.open(IMG)
    img = img.resize((WIDTH, HEIGHT), Image.NEAREST)
    for i in xrange(WIDTH):
        for j in xrange(HEIGHT):
            text += get_char(*img.getpixel((i,j)))
        text += '\n'
    print text

    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(text)
    else:
        with open('output.txt', 'w') as f:
            f.write(text)

if __name__ == '__main__':
    main()

