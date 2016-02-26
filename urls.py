from tornado.web import url

from users.handlers import RegisterHandler


url_patterns = [
    # test
    # url(r"/", BaseHandler, name="home"),
    url(r"/users/", RegisterHandler),
]
