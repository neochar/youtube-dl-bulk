
# So the task is to develop bulk mp3 download from youtube.
# We get *urls.txt files and *playlists.txt files.
# Urls file contains list of urls each per line.
# For every url we run youtube-dl and download it to corresponding folder.
# After that we implement also playlist parsing and download.

import sys
import os
from subprocess import Popen


if __name__ == '__main__':

    args = sys.argv[1:]

    processed = []
    procs = []

    if len(args) < 1:
        print('Provide filename with urls.')
        exit()

    for arg in args:
        with open(arg, 'r') as f:

            # Let's extract url format (watch / playlist)
            # and genre (name). We use genre as folder name.
            name = os.path.basename(arg)
            genre = name \
                .replace('-urls.txt', '') \
                .replace('-playlists.txt', '') \
                .replace('-urls-test.txt', '')

            path = 'data/mp3/{}'.format(genre)
            if not os.path.exists(path):
                os.makedirs(path)

            urls = list(filter(None, f.read().split('\n')))
            for i, url in enumerate(urls):
                if url in processed:
                    continue
                processed.append(url)

                # Run shell command to download mp3(s) with youtube-dl
                procs.append(Popen([
                    'youtube-dl',
                    '--output',
                    '{}/%(title)s.%(ext)s'.format(path),
                    '--extract-audio',
                    '--audio-format',
                    'mp3',
                    url
                ]))
                if i > 0 and i % 4 == 0 or i == len(urls) - 1:
                    for proc in procs:
                        proc.wait()
                        procs.remove(proc)
    print('{} url(s) processed.'.format(len(processed)))
