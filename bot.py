import praw
import OAuth2Util

class Bot:
    
    def __init__(self, ver):
        self.user_agent = 'CCJ_AidBot v.{} by /u/individual_throwaway'.format(ver)
        self.r = praw.Reddit(self.user_agent)
        self.o = OAuth2Util.OAuth2Util(self.r)
        
VERSION = '0.1'

def main():
    aid = Bot(VERSION)

if __name__ == '__main__':
    main()