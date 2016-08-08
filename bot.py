import sqlite3
import praw
import os
import random
import json

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
            conn.row_factory = lambda cursor, row: row[0]
            cur = conn.cursor()
            result = cur.execute('SELECT id FROM done').fetchall()
        self.replied_to = [str(x) for x in result]
        return self.replied_to
            
    def _get_comments(self):
        """Ignore deleted comments (for some reason it still showed the comment bodies
           of spam posts you deleted from r/tradotto even though the API says
           they should have been set to None)."""
        self.o.refresh()
        sub = self.r.get_subreddit('tradotto')##('climbingcirclejerk')
        self.comments = [x for x in sub.get_comments(limit=100) if x.author is not None]
        
    def _reply_to_comments(self, comments):
        """Look for keywords in comments and reply with '<keyword> is/are aid'.
           Does not reply to itself and saves all comment IDs it replied to so it 
           doesn't reply to the same comment more than once."""
        for comment in self.comments:
            keyword = ''
            if comment.author.name == 'Bots_are_aid' or comment.id in self.replied_to:
                continue
            text = comment.body.lower()
            for word in self.kw_singular:
                if word in text:
                    keyword = word
                    break
            if not keyword:
                for word in self.kw_plural:
                    if word in text:
                        keyword = word
                        break
            if keyword and random.random() > 0.5:
                if keyword in self.kw_singular:
                    comment.reply(keyword + ' is aid.')
                elif keyword in self.kw_plural:
                    comment.reply(keyword + 's are aid.')
                with sqlite3.connect('done.db') as conn:
                    conn.execute('INSERT INTO done VALUES (?)', (comment.id,))
    
    def run(self):
        self._get_comments()
        self._reply_to_comments(self.comments)
        
__version__ = '0.2'

def main():
    with open('keywords.json', 'r') as keywords:
        keywords = json.load(keywords)
    kw_singular = keywords['singular']
    kw_plural = keywords['plural']
    bot = AidBot(__version__, kw_singular, kw_plural)
    bot.run()

if __name__ == '__main__':
    main()
