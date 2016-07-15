import praw
import OAuth2Util

class Bot:
    
    def __init__(self, ver, keywords_singular, keywords_plural):
        self.user_agent = 'CCJ_AidBot v.{} by /u/individual_throwaway'.format(ver)
        self.r = praw.Reddit(self.user_agent)
        self.o = OAuth2Util.OAuth2Util(self.r)
        self.keywords_singular = keywords_singular
        self.keywords_plural = keywords_plural
        
    def _look_for_keywords(self, comment):
        found = []
        return found
        
        
VERSION = '0.1'
KEYWORDS_SINGULAR = ['chalk',
                     'pof',
                     'honnold',
                     'gear',
                     'belay',
                     'aid']

KEYWORDS_PLURAL = ['quickdraw',
                   'anchor',
                   'shoe',
                   'hold',
                   'foothold',
                   'helmet',
                   'cam',
                   'nut',
                   'rope',
                   'ascender',
                   'belayer',
                   'jug',
                  'pinch']


def main():
    aid = Bot(VERSION, KEYWORDS_SINGULAR, KEYWORDS_PLURAL)

if __name__ == '__main__':
    main()