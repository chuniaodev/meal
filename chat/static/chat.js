// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#messageform").live("submit", function() {
        newMessage($(this));
        return false;
    });
    $("#messageform").live("keypress", function(e) {
        if (e.keyCode == 13) {
            newMessage($(this));
            return false;
        }
    });
    $("#message").select();

    // add new menu lichuntao
    $("#menuform").live("submit", function() {
        newMenu($(this));
        return false;
    });
    $("#menuform").live("keypress", function(e) {
        if (e.keyCode == 13) {
            newMenu($(this));
            return false;
        }
    });
    //$("#menuid").select();
    updater.poll();
});

function newMenu(form) {
    var menu = form.formToDict();
    var disabled = form.find("input[type=submit]");
    //disabled.disable();
    var menuReqFlag = document.getElementById("menuReqFlagID");
    menuReqFlag.value = "ON"
    var menuReqFlag = document.getElementById("mesgReqFlagID");
    menuReqFlag.value = "OFF"
    $.postJSON("/a/menu/new", menu, function(response) {
        updater.showMenu(response);
        if (menu.id) {
            form.parent().remove();
        } else {
            form.find("input[type=text]").val("").select();
            disabled.enable();
        }
    });
}

function newMessage(form) {
    var message = form.formToDict();
    var disabled = form.find("input[type=submit]");
    //disabled.disable();
    var menuReqFlag = document.getElementById("menuReqFlagID");
    menuReqFlag.value = "OFF"
    var menuReqFlag = document.getElementById("mesgReqFlagID");
    menuReqFlag.value = "ON"
    $.postJSON("/a/message/new", message, function(response) {
        updater.showMessage(response);
        if (message.id) {
            form.parent().remove();
        } else {
            form.find("input[type=text]").val("").select();
            disabled.enable();
        }
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
            success: function(response) {
        if (callback) callback(eval("(" + response + ")"));
    }, error: function(response) {
        console.log("ERROR:", response)
    }});
};

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

jQuery.fn.disable = function() {
    this.enable(false);
    return this;
};

jQuery.fn.enable = function(opt_enable) {
    if (arguments.length && !opt_enable) {
        this.attr("disabled", "disabled");
    } else {
        this.removeAttr("disabled");
    }
    return this;
};

var updater = {
    errorSleepTime: 500,
    cursor: null,
    menucursor: null,

    poll: function() {
        var args = {"_xsrf": getCookie("_xsrf")};
        //console.log("url:", $.query.get('') ); 
        var menuFlag = document.getElementById("menuReqFlagID");
        var mesgFlag = document.getElementById("mesgReqFlagID");
        //console.log("menuReq:", menuFlag.value ); //request.getHeader("Referer")  window.location.href 
        //console.log("mesgReq:", mesgFlag.value ); 
        if ("ON".indexOf(mesgFlag.value)==0) {
            if (updater.cursor) args.cursor = updater.cursor;
            $.ajax({url: "/a/message/updates", type: "POST", dataType: "text",
                data: $.param(args), success: updater.onSuccess,
                error: updater.onError});
        }

        if ("ON".indexOf(menuFlag.value)==0) {
            if (updater.menucursor) args.menucursor = updater.menucursor;
            $.ajax({url: "/a/menu/updates", type: "POST", dataType: "text",
                data: $.param(args), success: updater.onMenuSuccess,
                error: updater.onError});
        }
    },

    onSuccess: function(response) {
        try {
            updater.newMessages(eval("(" + response + ")"));
            //updater.newMenus(eval("(" + response + ")"));
        } catch (e) {
            updater.onError();
            return;
        }
        updater.errorSleepTime = 500;
        window.setTimeout(updater.poll, 0);
    },

    onMenuSuccess: function(response) {
        try {
            updater.newMenus(eval("(" + response + ")"));
        } catch (e) {
            updater.onError();
            return;
        }
        updater.errorSleepTime = 500;
        window.setTimeout(updater.poll, 0);
    },

    onError: function(response) {
        updater.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", updater.errorSleepTime, "ms");
        window.setTimeout(updater.poll, updater.errorSleepTime);
    },

    newMessages: function(response) {
        if (!response.messages) return;
        updater.cursor = response.cursor;
        var messages = response.messages;
        updater.cursor = messages[messages.length - 1].id;
        console.log(messages.length, "new messages, cursor:", updater.cursor);
        for (var i = 0; i < messages.length; i++) {
            updater.showMessage(messages[i]);
        }

    },

    newMenus: function(response) {
        if (!response.menus) return;
        updater.menucursor = response.menucursor;
        var menus = response.menus;
        updater.menucursor = menus[menus.length - 1].id;
        console.log(menus.length, "new menus, menucursor:", updater.menucursor);
        var sum = 0;
        for (var i = 0; i < menus.length; i++) {
            updater.showMenu(menus[i]);
            //sum += menus[i].price;
        }
        document.getElementById("sumid").innerHTML = sum;
    },

    showMenu: function(menu) {
        var existing = $("#menu" + menu.id);
        if (existing.length > 0) return;
        var node = $(menu.html);
        node.hide();
        $("#inmenubox").append(node);
        node.slideDown();
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    }

};


