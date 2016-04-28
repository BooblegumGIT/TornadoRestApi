from tornado.web import url

from accounts.handlers import RegisterHandler
from test.handlers import TestHandler


url_patterns = [
    # test
    # url(r"/", BaseHandler, name="home"),
    url(r"/accounts/", RegisterHandler),
]

test_patterns = [
    url(r"/test/([0-9]+)", TestHandler, dict(db="db"), name="test"),
]
# dict(db="db") - передается в Handler.initialize()
# name="test" - пока не выяснил назначение
url_patterns += test_patterns