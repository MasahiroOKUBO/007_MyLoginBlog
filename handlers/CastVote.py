from models import Vote, posts_key, votes_key
from handlers import BaseHandler
from google.appengine.ext import ndb


class CastVote(BaseHandler):
    """User can vote on blog posts."""
    def post(self, post_id):
        if not self.user:
            self.redirect('/login')
            return
        post_key = ndb.Key('Post', int(post_id), parent=posts_key())
        post = post_key.get()
        voter_key = self.user.key

        if post.author_key == voter_key:
            message = "Can not veto yourself!"
            self.redirect('/blog')
            return

        old_vote = Vote.query() \
            .filter(Vote.voter_key == voter_key) \
            .filter(Vote.post_key == post.key) \
            .get()

        if old_vote:
            message = "already voted!"
            self.redirect('/blog')
            return

        if voter_key and post.key:
            vote = Vote(parent=votes_key(), voter_key=voter_key, post_key=post.key)
            vote.put()
            message = "Vote Succeeded!"
            self.redirect('/blog')
            return

