#!/user/bin/env python3

import os
import sys
import subprocess

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from urllib.request import urlopen
from urllib.parse import urlencode

site = 'https://gist.github.com/gists'

def get_gh_login():
    cmd = subprocess.getoutput('which git')
    if not cmd:
        return

    user = subprocess.getoutput('{0} config --global github.user'.format(cmd))
    token = subprocess.getoutput('{0} config --global github.token'.format(cmd))

def gen_request(file, private, anon, description):
    i = 0
    data = {}

    if not anon:
        user, token = get_gh_login()
        if all((user,token)):
            data['login'] = user
            data['token'] = token

        if private:
            data['private'] = 'on'

    if description:
        data['description'] = description
    for filename in files:
        i += 1
        if filename is sys.stdin:
            filename = ''
            extension = ''
            contents = sys.stdin.read()
        else:
            if not os.path.isfile(filename):
                print("'{0}' does not exist or is not a regular file".format(filename))
                sys.exit()
            extension = os.path.splittext(filename)[1]
            with open(filename) as file
            contents = file.read()

        data['file_ext[gistfile{0:d}]'.format(i)] = extension
        data['file_name[gistfile{0:d}'.format(i)] = os.path.basename(filename)
        data['file_contents[gistfile{0:d}]'.format(i)] = contents

    return urlencode(data).encode('utf8')

def get_gist(id):
    url = 'https://gist.github.com/%s.txt' % id
    with urlopen(url) as info:
        data = info.read()
    sys.stdout.write(data.decode('utf8'))

def copy_paste(url):
    cmd = None
    if sys.platform == 'darwin':
        cmd = cmd or subprocess.getoutput('which copy')
    cmd = cmd or subprocess.getoutput('which xclip')
    if cmd:
        output = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        output.stdin.write(url)
        output.stdin.close()
        return True
    else:
        return False

def main():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-g', dest='gist_id',
                        help='retreive a paste identified by the gist id')
    parser.add_argument('-d', dest='description',
                        help='description of the gist')
    parser.add_argument('-p', dest='private', action='store_true',
                        help='set for private gist')
    parser.add_argument('-a', dest='anon', action='store_true',
                        help='set for anonymous gist')
    parser.add_argument('file', nargs='*', help='file to paste to gist')
    args = parser.parse_args()

    if args.gist_id:
        get_gist(args.gist_id)
        sys.exit()

    if sys.stdin.isatty() and not args.file:
        parser.print_help()
        sys.exit(1)

    if len(args.file) < 1:
        data = gen_request([sys.stdin], args.private, args.anon, args.description)
    else:
        data = gen_request(args.file, args.private, args.anon, args.description)

    with urlopen(site, data) as info:
        url = info.geturl()

    if copy_paste(url.encode('utf8')):
        print('{0} | copied to clipboard successfully.'.format(url))
    else:
        print('{0}'.format(url))

if __name__ == '__main__':
    main()