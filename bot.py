import sqlite3
import praw
import os

import OAuth2Util

class AidBot:
    
    def __init__(self, ver, kw_singular, kw_plural):
        self.user_agent = 'CCJ_AidThingy.{} by /u/individual_throwaway and u/tradotto'.format(ver)
        self.user_agent.encode('utf-8')
        self.r = praw.Reddit(self.user_agent)
        self.o = OAuth2Util.OAuth2Util(self.r)
        self.kw_singular = kw_singular
        self.kw_plural = kw_plural
        self.found_kw = {}
        self.comments = None
        self.replied_to = []
        if os.path.exists(os.path.join(os.getcwd(), 'done.db')):
            self.replied_to = self._get_replied_list()
        else:
            with sqlite3.connect('done.db') as conn:
                conn.execute('CREATE TABLE done (id text)')

    def _get_replied_list(self):
        """Make sure we don't reply to the same comment twice."""
        with sqlite3.connect('done.db') as conn:
            cur = conn.cursor()
            result = cur.execute('SELECT id FROM done').fetchall()
        self.replied_to = [str(x) for x in result]

    def _save_reply(self, comment):
        """Saves the comment we reply to in the done table by id."""
        with sqlite3.connect('done.db') as conn:
            conn.execute('insert into done (id) values (?)', (comment.id,))
            
    def _get_comments(self):
        """Ignore deleted comments (for some reason it still showed the comment bodies
           of spam posts you deleted from r/tradotto even though the API says
           they should have been set to None)."""
        self.o.refresh()
        sub = self.r.get_subreddit('tradotto')##('climbingcirclejerk')
        self.comments = [x for x in sub.get_comments(limit=100) if x.author is not None]
        
    def _reply_to_comments(self, comments):
        """Look for keywords in comments and reply with '<keyword> is aid'.
           Does not reply to itself and saves all comment IDs it replied to so it 
           doesn't reply to the same comment more than once."""
        #TODO: include KEYWORDS_PLURAL (reply to first match in either of them, but
        #for plural keywords, use 'are
        keyword = ''
        for comment in self.comments:
            if comment.author.name == 'Bots_are_aid' or comment.id in self.replied_to:
                continue
            s = comment.body.lower()
            for k in KEYWORDS_SINGULAR:
                if k in s:
                    print("found ", k, " in ", s, " comment id: ", comment.id, comment.author)
                    keyword = k
            if keyword:
                #need to save the comment.id in the DB so we don't keep trying to comment on the same damn thing
                #comment.reply(keyword.title + " is aid.")
                self._save_reply(comment)
    
    def run(self):
        self._get_replied_list()
        self._get_comments()
        self._reply_to_comments(self.comments)
        
VERSION = '0.1'
KEYWORDS_SINGULAR = ['chalk',
                     'pof',
                     'honnold',
                     'gear',
                     'belay',
                     'harness',
                     'spot',
                     'core']

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
    bot = AidBot(VERSION, KEYWORDS_SINGULAR, KEYWORDS_PLURAL)
    bot.run()

if __name__ == '__main__':
    main()
