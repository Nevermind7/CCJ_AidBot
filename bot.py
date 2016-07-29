import OAuth2Util
import sqlite3
import praw

class AidBot:
    
    def __init__(self, ver, kw_singular, kw_plural):
        self.user_agent = 'CCJ_AidThingy.{} by /u/individual_throwaway'.format(ver)
	self.user_agent.encode('utf-8')
        self.r = praw.Reddit(self.user_agent)
        self.o = OAuth2Util.OAuth2Util(self.r)
        self.kw_singular = kw_singular
        self.kw_plural = kw_plural
        self.found_kw = {}
        self.comments = None
        self.replied_to = self._get_replied_list()
    """Need to check the db to see if it exists. and then build the table structor if it doesn't""" 
    def _get_replied_list(self):
        """Makes sure we don't reply to the same comment twice."""
        with sqlite3.connect('done.db') as conn:
            cur = conn.cursor()
            result = cur.execute('SELECT id FROM done').fetchall()
        return [str(x) for x in result]

    def _save_reply(self, comment):
	"""saves the comment we reply to in the done table by id"""
	with sqlite3.connect('done.db') as conn:
		cur = conn.cursor()
		result = cur.execute("insert into done.id values({c_id})".format(c_id = comment.id))
		conn.commit()
		con.close()
        
    def _get_comments(self):
        self.o.refresh()
        ccj = self.r.get_subreddit('tradotto')##('climbingcirclejerk')
        self.comments = [x for x in ccj.get_comments(limit=100)]
#        for comment in self.comments:
           # print(comment.body)
        
    def _parse_comments(self, comments):
 	keyword = ''	
	for comment in self.comments:
		s = comment.body
		for k in KEYWORDS_SINGULAR:
			if k in s:
				print("found ", k, " in ", s, " comment id: ", comment.id)
				keyword = k
				break
			else:
				reply = False
		#want to comment here
		if keyword:
			##need to save the comment.id in the DB so we don't keep trying to comment on the same damn thing
			##self._save_reply(comment)
			
			comment.reply(keyword.title + " is aid.")
	pass
    
    def _reply(self, submission, found):
        pass
    
    def run(self):
        self._get_comments()
	self._parse_comments(self.comments)
       # print(len(self.comments))
        
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
    aid = AidBot(VERSION, KEYWORDS_SINGULAR, KEYWORDS_PLURAL)
    aid.run()

if __name__ == '__main__':
    main()
