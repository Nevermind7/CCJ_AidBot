import praw
import OAuth2Util

class Bot:
    
    def __init__(self, ver, keywords_singular, keywords_plural):
        self.user_agent = 'CCJ_AidBot v.{} by /u/individual_throwaway'.format(ver)
        self.r = praw.Reddit(self.user_agent)
        self.o = OAuth2Util.OAuth2Util(self.r)
        self.kw_singular = keywords_singular
        self.kw_plural = keywords_plural
        self.submissions = None
        self.found_kw = {}
    
    def _get_recent_submissions(self):
        self.o.refresh()
        ccj = self.r.get_subreddit('climbingcirclejerk')
        self.submissions = ccj.get_new(limit=10)
    
    def _parse_OP(self, submission):
        pass
        
    def _parse_comments(self, comments):
        pass
    
    def _reply(self, submission, found):
        pass
    
    def run(self):
        self.submissions = self._get_recent_submissions()
        for submission in self.submissions:
            self._parse_OP
            self._parse_comments
        if self.found_kw:
            self._reply()
        
VERSION = '0.1'
KEYWORDS_SINGULAR = ['chalk',
                     'pof',
                     'honnold',
                     'gear',
                     'belay',
                     'aid',
                     'harness']

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
                   'pinch',
                   'crimp',
                   'carabiner',
                   'biner',
                   ]


def main():
    aid = Bot(VERSION, KEYWORDS_SINGULAR, KEYWORDS_PLURAL)
    aid.run()

if __name__ == '__main__':
    main()