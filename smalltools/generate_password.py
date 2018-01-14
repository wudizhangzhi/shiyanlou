"""
Generate Password.
Usage:
    generate.py [-n NUM]
    generate.py (-h | --help)
    generate.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -n NUM --num NUM output password nums.
"""
from string import ascii_letters, digits, punctuation 
from random import choice
from docopt import docopt

char_pool = ascii_letters + digits + punctuation

def generate_password(num=8):
    password = ''
    for _ in range(num): 
        password += choice(char_pool)
    print(password)
    return password

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    generate_password(int(arguments.get('--num')))
