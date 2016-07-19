import praw
import OAuth2Util

class AidBot:
    
    def __init__(self, ver, kw_singular, kw_plural):
        self.user_agent = 'CCJ_AidBot v.{} by /u/individual_throwaway'.format(ver)
        self.r = praw.Reddit(self.user_agent)
        self.o = OAuth2Util.OAuth2Util(self.r)
        self.kw_singular = kw_singular
        self.kw_plural = kw_plural
        self.found_kw = {}
        #self.comments = None
        self.replied_to = self._get_replied_list()
    
    def _get_replied_list(self):
        """Makes sure we don't reply to the same comment twice."""
    
    def _get_comments(self):
        self.o.refresh()
        ccj = self.r.get_subreddit('climbingcirclejerk')
        self.comments = [x for x in ccj.get_comments()]
        
    def _parse_comments(self, comments):
        """Look for keywords in comments, reply on the first hit."""
        pass
    
    def _reply(self, submission, found):
        pass
    
    def run(self):
        self._get_comments()
        print(len(self.comments))
        
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
                   'biner']


def main():
    aid = AidBot(VERSION, KEYWORDS_SINGULAR, KEYWORDS_PLURAL)
    aid.run()

if __name__ == '__main__':
    main()