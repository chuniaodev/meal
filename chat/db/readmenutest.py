#!/usr/bin/env python
''' 
    test read menudb
'''

print "read menudb"

menus = []
#menu = dict()
menufile = open("menu.db", "r")

try:
    menustrs = menufile.readlines()
    #print "file:\n%s" % (menustrs)
    for cur in menustrs :
        menustr = cur.strip().split(",")
        #print "line:%s" % (menustr)
        menu = dict()
        menu["menuid"] = menustr[0]
        menu["menuname"] = menustr[1]
        menu["menupirce"] = menustr[2]
        #print "menu:\n%s" % (menu)
        menus.append(menu)
    print "menus:\n%s" % (menus)
except IOError, e:
    print "open menu.db error: ",e 

except Exception, e:
    print "unable error: ",e 

finally:
    menufile.close()

if menus != None :
    #print "the menu is: %s, type:%s" % (menu, type(menu))
    for cur in menus :
        print "menuid: %s, " % (cur["menuid"]),
        print "menuname: %s, " % (cur["menuname"]),
        print "menupirce: %s, " % (cur["menupirce"])



