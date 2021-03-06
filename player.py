#!/usr/bin/env python

import os
import time
import sys
import subprocess
import RPi.GPIO as GPIO

#mplayer -loop 0 PATH

class Player:

    def __init__(self, change_notify):
        print('player init')
        self.p = None
        self.status = 'stop'
        self.change_notify = change_notify

    def __del__(self):
        print('player del')

    def play(self, path):
        if self.status != 'stop':
            self.stop()

        dev_null = open(os.devnull, 'w')
        args = ['/usr/bin/mplayer', '-loop', '0', path]

#        self.p = subprocess.Popen(args, stdin=subprocess.PIPE)
        self.p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=dev_null, stderr=dev_null)
        self.status = 'play'
        self.status_notify()

    def stop(self):
        if self.status == 'stop':
            return

        #self.p.communicate('q')
        self.p.stdin.write('q')

        self.status = 'stop'
        self.status_notify()

    def pause(self):
        if self.status != 'play':
            return

        self.p.stdin.write('p')

        self.status = 'pause'
        self.status_notify()

    def resume(self):
        if self.status != 'pause':
            return

        self.p.stdin.write('p')

        self.status = 'play'
        self.status_notify()

    def inc_vol(self):
        if self.status != 'play':
            return

        self.p.stdin.write('0')

    def dec_vol(self):
        if self.status != 'play':
            return

        self.p.stdin.write('9')

    def status_notify(self):
        if self.change_notify != None:
            self.change_notify('media')

if __name__ == '__main__':
    player = Player()
    TEST_URL = 'http://sc.111ttt.com/up/mp3/11219/2A78B09675979C6093C58E3E39740FC8.mp3'
    TEST_LOCAL = '/home/pi/music/test.mp3'
    sleep = 5

    print('play url')
    player.play(TEST_URL)

    time.sleep(sleep)
    print('play local')
    player.play(TEST_LOCAL)

    time.sleep(sleep)
    print('pause')
    player.pause()

    time.sleep(sleep)
    print('resume')
    player.resume()

    time.sleep(sleep)
    print('inc_vol')
    player.inc_vol()
    print('inc_vol')
    player.inc_vol()

    time.sleep(sleep)
    print('dec_vol')
    player.dec_vol()
    print('dec_vol')
    player.dec_vol()

    time.sleep(sleep)
    print('stop')
    player.stop()

