#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import uuid
import string

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class UserManager(object):

    def find_user(self, username):
        loginflag = False
        user = dict()
        user["username"] = username
        userfile = open("user.db", "r")
        try:
            userstrs = userfile.readlines()
            for cur in userstrs :
                userstr = cur.strip().split(",")
                if user["username"] == userstr[1] :
                    user["userid"] = userstr[0]
                    user["userchname"] = userstr[3]
                    user["usersum"] = userstr[4]
                    user["usertype"] = userstr[5]
                    loginflag = True
                    break
        except IOError, e:
            print "open user.db error: ",e 
        except Exception, e:
            print "unable error: ",e 
        finally:
            userfile.close()
        if False == loginflag:
            return None
        return user

    
    def login_check(username, password):
        loginflag = False
        user = dict()
        user["username"] = username
        user["password"] = password
        userfile = open("user.db", "r")
        try:
            userstrs = userfile.readlines()
            for cur in userstrs :
                userstr = cur.strip().split(",")
                if (user["username"] == userstr[1]) & (user["password"] == userstr[2]) :
                    user["userid"] = userstr[0]
                    user["userchname"] = userstr[3]
                    user["usersum"] = userstr[4]
                    user["usertype"] = userstr[5]
                    loginflag = True
                    break
        except IOError, e:
            print "open user.db error: ",e 
        except Exception, e:
            print "unable error: ",e 
        finally:
            userfile.close()
        if False == loginflag:
            return None
        return user

    def add_user():
        pass

    def del_user():
        pass

    def modify_user():
        pass

class MenuManager(object):
    def __init__(self):
        pass
    
    def find_menu(self, menuid):
        menu = dict()
        menufile = open("menu.db", "r")
        try:
            menustrs = menufile.readlines()
            for cur in menustrs :
                menustr = cur.strip().split(",")
                if menuid == menustr[0] :
                    menu["menuid"] = menustr[0]
                    menu["menuname"] = menustr[1]
                    menu["menuprice"] = menustr[2]
                    break
        except IOError, e:
            print "open menu.db error: ",e 
        except Exception, e:
            print "unable error: ",e 
        finally:
            menufile.close()
        return menu 

    def travel_menu(self):
        menus = []
        menufile = open("menu.db", "r")
        try:
            menustrs = menufile.readlines()
            for cur in menustrs :
                menustr = cur.strip().split(",")
                menu = dict()
                menu["menuid"] = menustr[0]
                menu["menuname"] = menustr[1]
                menu["menuprice"] = menustr[2]
                menus.append(menu)
        except IOError, e:
            print "open menu.db error: ",e 
        except Exception, e:
            print "unable error: ",e 
        finally:
            menufile.close()
        return menus

    def add_menu(self):
        pass

    def del_menu(self):
        pass

    def modify_menu(self):
        pass

    def set_menudisplay(self, menuid, display):
        mls = MenuMixin
        for i in xrange(len(mls.cache)):
            index = len(mls.cache) - i - 1
            if (menuid == mls.cache[index]["id"]):
                mls.cache[index]["display"] = display

    def get_personmenusum(self, cname):
        personmenusum = 0
        mls = MenuMixin
        for i in xrange(len(mls.cache)):
            index = len(mls.cache) - i - 1
            #print "gpms:mu:%s" % (mls.cache[index]["from"])
            if ("show" == mls.cache[index]["display"]):
                if cname == mls.cache[index]["fromuserid"]:
                    personmenusum += string.atoi(mls.cache[index]["menuprice"])
        return personmenusum

    def get_menusum(self):
        menusum = 0
        mls = MenuMixin
        for i in xrange(len(mls.cache)):
            index = len(mls.cache) - i - 1
            if ("show" == mls.cache[index]["display"]):
                menusum += string.atoi(mls.cache[index]["menuprice"])
        return menusum

class MealManager():
    def __init__():
        pass
    
    def find_meal():
        pass

    def add_meal():
        pass

    def del_meal():
        pass

    def modify_meal():
        pass

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/a/message/new", MessageNewHandler),
            (r"/a/message/updates", MessageUpdatesHandler),
            (r"/a/menu/new", MenuNewHandler),
            (r"/a/menu/updates", MenuUpdatesHandler),
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape="xhtml_escape",
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        #print "user_json: %s" % (user_json)
        if not user_json: return None
        return user_json
        #return tornado.escape.json_decode(user_json)

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cusername = tornado.escape.xhtml_escape(self.current_user)
        #if self.get_argument("next", None):
        #    self.redirect(self.get_argument("next"))
        #else:
        #    self.write(menu)
        #self.new_menus([menu])
        userdict = dict()
        userManager = UserManager() 
        userdict = userManager.find_user(cusername)
        userdict["menunum"] = len(MenuMixin.cache) #error num

        menuManager = MenuManager() 
        userdict["menusum"] = menuManager.get_menusum()
        userdict["personmenusum"] = menuManager.get_personmenusum(cusername)
        #print "personmenusum:%s" % (userdict["personmenusum"])
        
        menus = []
        menuManager = MenuManager() 
        menus = menuManager.travel_menu()
        self.render("index.html", mlists=MenuMixin.cache, messages=MessageMixin.cache, menus=menus, user=userdict)
        #self.redirect("/auth/login")
        #self.render("login.html")

class MessageMixin(object):
    waiters = set()
    cache = []
    cache_size = 30

    def wait_for_messages(self, callback, cursor=None):
        cls = MessageMixin
        if cursor:
            index = 0
            for i in xrange(len(cls.cache)):
                index = len(cls.cache) - i - 1
                if cls.cache[index]["id"] == cursor: break
            recent = cls.cache[index + 1:]
            if recent:
                callback(recent)
                return
        cls.waiters.add(callback)

    def cancel_wait(self, callback):
        cls = MessageMixin
        cls.waiters.remove(callback)

    def new_messages(self, messages):
        cls = MessageMixin
        logging.info("Sending new message to %r listeners", len(cls.waiters))
        for callback in cls.waiters:
            try:
                callback(messages)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        cls.waiters = set()
        cls.cache.extend(messages)
        if len(cls.cache) > self.cache_size:
            cls.cache = cls.cache[-self.cache_size:]

class MessageNewHandler(BaseHandler, MessageMixin):
    @tornado.web.authenticated
    def post(self):
        #print "from:%s" % (self.get_argument("username"))
        message = {
            "id": str(uuid.uuid4()),
            #"from": self.get_current_user(),
            "from": self.get_argument("username"),
            "body": self.get_argument("body"),
        }
        message["html"] = self.render_string("message.html", message=message)
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        self.new_messages([message])


class MessageUpdatesHandler(BaseHandler, MessageMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        cursor = self.get_argument("cursor", None)
        self.wait_for_messages(self.on_new_messages,
                               cursor=cursor)

    def on_new_messages(self, messages):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        self.finish(dict(messages=messages))

    def on_connection_close(self):
        self.cancel_wait(self.on_new_messages)

class MenuMixin(object):
    waiters = set()
    cache = []
    cache_size = 200

    def wait_for_menus(self, callback, cursor=None):
        cls = MenuMixin
        if cursor:
            index = 0
            for i in xrange(len(cls.cache)):
                index = len(cls.cache) - i - 1
                if cls.cache[index]["id"] == cursor: break
            recent = cls.cache[index + 1:]
            if recent:
                callback(recent)
                return
        cls.waiters.add(callback)

    def cancel_wait(self, callback):
        cls = MenuMixin
        cls.waiters.remove(callback)

    def new_menus(self, menus):
        cls = MenuMixin
        logging.info("Sending new menu to %r listeners", len(cls.waiters))
        for callback in cls.waiters:
            try:
                callback(menus)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        cls.waiters = set()
        cls.cache.extend(menus)
        if len(cls.cache) > self.cache_size:
            cls.cache = cls.cache[-self.cache_size:]



class MenuNewHandler(BaseHandler, MenuMixin):
    @tornado.web.authenticated
    def post(self):
        menu = dict()
        menuManager = MenuManager()
        command = self.get_argument("command")
        if ( "order" == command ):
            menuid = self.get_argument("menuid")
            menu = menuManager.find_menu(menuid)
            menu["from"] = self.get_argument("username")
            menu["fromuserid"] = self.get_argument("userid")
            menu["id"] = str(uuid.uuid4())
            menu["display"] = "show"
        elif ( "delmenu" == command ):
            menuid = self.get_argument("deletemenuid")
            menu = menuManager.find_menu(menuid)
            menu["display"] = "hidden"
            menu["fromuserid"] = self.get_argument("fromuserid")
            menu["id"] = self.get_argument("menuid")
            menuManager.set_menudisplay(menu["id"], menu["display"])

        else :
            print "unknown command: %s" % (command)

        menu["html"] = self.render_string("mlist.html", menu=menu)
        #print "MN menu:%s" % (menu)
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(menu)
        self.new_menus([menu])

    def get(self):
        print "call this MenuNewHandler get"


class MenuUpdatesHandler(BaseHandler, MenuMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        cursor = self.get_argument("cursor", None)
        #print "MUH: cursor:%s" % (cursor)
        self.wait_for_menus(self.on_new_menus,
                               cursor=cursor)

    def on_new_menus(self, menus):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        self.finish(dict(menus=menus))

    def on_connection_close(self):
        self.cancel_wait(self.on_new_menus)


class AuthLoginHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        #if self.get_argument("openid.mode", None):
        #    self.get_authenticated_user(self.async_callback(self._on_auth))
        #    return
        #self.authenticate_redirect(ax_attrs=["name"])
        #self.write("Hello, %r" % (self.get_argument("username")))
        #self.render("index.html", messages=MessageMixin.cache)
        self.render("login.html", mesg="")

    def post(self):
        loginflag = False
        user = dict()
        user["username"] = self.get_argument("username")
        user["password"] = self.get_argument("password")
        userfile = open("user.db", "r")
        try:
            userstrs = userfile.readlines()
            for cur in userstrs :
                userstr = cur.strip().split(",")
                if (user["username"] == userstr[1]) & (user["password"] == userstr[2]) :
                    user["userid"] = userstr[0]
                    user["userchname"] = userstr[3]
                    user["usersum"] = userstr[4]
                    user["usertype"] = userstr[5]
                    loginflag = True
                    break
        except IOError, e:
            print "open user.db error: ",e 
        except Exception, e:
            print "unable error: ",e 
        finally:
            userfile.close()
        if False == loginflag:
            return self.render("login.html", mesg="login error!" )

        #self.write("Hello, %s" % (self.get_argument("username")))

        #menu = {
        #    "id": 2001,
        #    "menuname": "gbjd",
        #    "menuprice": 14,
        #}

        #menus = []
        #menuManager = MenuManager() 
        #menus = menuManager.travel_menu()
        #menu["html"] = self.render_string("menu.html", menu=menu)
        #self.render("index.html", mlists=MenuMixin.cache, messages=MessageMixin.cache, menus=menus, user=user)
        self.set_secure_cookie("user", user["username"])
        self.redirect("/")

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect("/")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.write("You are now logged out")


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
