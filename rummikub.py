#!/usr/bin/env python
"""
Main rummikub status collection module.
"""


import argparse
from database import Database
from datetime import datetime
from datetime import timedelta
import os
from pathlib import Path
import pytz
import sys


def build_parser():
    """
    Collect command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d', '--database_file', default='rummikub.db',
                        help='file name of the sqlite database file. '
                        'default: %(default)s')
    parser.add_argument('--noisy',
                        default=False, action='store_true',
                        help = 'Be more noisy about what is going on. '
                        'default: %(default)s')
    parser.add_argument('--show_stats',
                        default=False, action='store_true',
                        help = 'Show statistics. '
                        'default: %(default)s')
    return parser


def now():
    """
    Return the real time, in the current time zone.
    """
    return datetime.now(tz=pytz.timezone(os.environ['TZ']))


class Rummikub():
    def __init__(self, database):
        self.database = database


    def input_loop(self):
        while True:
            sys.stdout.write('Press <ENTER> when starting the game... ')
            sys.stdout.flush()
            ans = sys.stdin.readline().strip().lower()
            if ans:
                break
            start_time = now()
            sys.stdout.write('Press <ENTER> when stopping game game... ')
            sys.stdout.flush()
            _ = sys.stdin.readline().strip()
            end_time = now()
            sys.stdout.write('Did I win? (y) ')
            sys.stdout.flush()
            ans = sys.stdin.readline().strip().lower()
            my_win = True if ans ==  'y' or not ans else False
            self.database.insert('stats', {'start_time': start_time,
                                      'end_time': end_time,
                                      'my_win': my_win,
                                      'timestamp': now()})
    def show_stats(self):
        rows = self.database.select(['start_time', 'end_time', 'my_win'], 'stats', 'TRUE')
        print(rows)



def main(args):
    """
    Starting point.
    """
    database = Database(args.database_file, args.noisy)
    rummi = Rummikub(database)
    if args.show_stats:
        rummi.show_stats()
    else:
        rummi.input_loop()

if __name__ == '__main__':
    sys.exit(main(build_parser().parse_args()))
