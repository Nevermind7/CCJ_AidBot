import sqlite3
import praw
import random
import json

import OAuth2Util

class AidBot:
    
    def __init__(self, ver, keywords, responses):
        self.user_agent = 'CCJ_AidThingy.{} by /u/individual_throwaway and u/tradotto'.format(ver)
        self.user_agent.encode('utf-8')
        self.r = praw.Reddit(self.user_agent)
        self.o = OAuth2Util.OAuth2Util(self.r)
        self.target = 'climbingcirclejerk'
        self.responses = responses
        self.keywords = keywords
        self.comments = None
        self.submissions = None
        self.replied_to = []
        if os.path.exists(os.path.join(os.getcwd(), 'done.db')):
            self.replied_to = self._get_replied_list()
        else:
            with sqlite3.connect('done.db') as conn:
                conn.execute('CREATE TABLE done (id text)')

    def _get_replied_list(self):
        """Make sure we don't reply to the same comment/submission twice."""
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
        sub = self.r.get_subreddit(self.target)
        self.comments = [x for x in sub.get_comments(limit=100) if x.author is not None]
        
    def _get_submissions(self):
        """Ignore submissions by deleted users (assuming this suffers from the same
           bug as the comments, better safe than sorry."""
        self.o.refresh()
        sub = self.r.get_subreddit(self.target)
        self.submissions = [x for x in sub.get_new(limit=100) if x.author is not None]
        
    def _reply_to_content(self, submissions, comments):
        """Look for keywords in content and reply with '<keyword> is/are aid'.
           Does not reply to itself and saves all content IDs it replied to so it 
           doesn't reply to the same content more than once."""
        for comment in self.comments:
            keyword = ''
            if comment.author.name == 'Bots_are_aid' or comment.id in self.replied_to:
                continue
            text = comment.body.lower()
            for word in self.keywords:
                if word in text:
                    keyword = word
                    break
            if keyword:
                try:
                    comment.reply(keyword.capitalize() + self.responses[self.keywords[keyword]])
                except:
                    continue
                with sqlite3.connect('done.db') as conn:
                    conn.execute('INSERT INTO done VALUES (?)', (comment.id,))

        for submission in submissions:
            keyword = ''
            if submission.author.name == 'Bots_are_aid' or submission.id in self.replied_to:
                continue
            title = submission.title.lower()
            text = submission.selftext.lower()
            for word in self.keywords:
                if word in title or word in text:
                    keyword = word
                    break
            if keyword:
                try:
                    submission.add_comment(keyword.capitalize() +\
                                           self.responses[self.keywords[keyword]])
                except:
                    continue
                with sqlite3.connect('done.db') as conn:
                    conn.execute('INSERT INTO done VALUES (?)', (submission.id,))    
    
    def run(self):
        self._get_submissions()
        self._get_comments()
        self._reply_to_content(self.submissions, self.comments)
        
__version__ = '0.3'

def main():

    with open('keywords.json', 'r') as keywords:
        keyword_data = json.load(keywords)
    keywords = keyword_data['keywords']
    responses = keyword_data['responses']
    
    bot = AidBot(__version__, keywords, responses)
    bot.run()

if __name__ == '__main__':
    main()
