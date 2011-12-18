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

//var menunum = document.getElementById("menunumid").innerHTML;
var menunum = $("#menunumid").text();
//var menusum = document.getElementById("menusumid").innerHTML;
var menusum = $("#menusumid").text();
//var userid = document.getElementById("userid").value;
var userid = $("#userid").val();

//var personmenusum = document.getElementById("personmenusumid").innerHTML;
var personmenusum = $("#personmenusumid").text();

//main page menu display set
//$("#inmenubox").append(node);


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
    disabled.disable();
    $("#menuReqFlagID").val("ON");
    $("#mesgReqFlagID").val("OFF");
    $.postJSON("/a/menu/new", menu, function(response) {
        updater.showMenu(response);
        if (menu.id) {
            form.parent().remove();
        } else {
            //form.find("input[type=text]").val("").select();
            disabled.enable();
        }
    });
}

function newMessage(form) {
    var message = form.formToDict();
    var disabled = form.find("input[type=submit]");
    disabled.disable();
    $("#menuReqFlagID").val("OFF");
    $("#mesgReqFlagID").val("ON");
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
        if ("ON".indexOf($("#mesgReqFlagID").val()) == 0) {
            if (updater.cursor) args.cursor = updater.cursor;
            $.ajax({url: "/a/message/updates", type: "POST", dataType: "text",
                data: $.param(args), success: updater.onSuccess,
                error: updater.onError});
        }

        if ("ON".indexOf($("#menuReqFlagID").val()) == 0) {
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

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    },

    newMenus: function(response) {
        if (!response.menus) return;
        updater.menucursor = response.menucursor;
        var menus = response.menus;
        updater.menucursor = menus[menus.length - 1].id;
        console.log(menus.length, "new menus, menucursor:", updater.menucursor);
        for (var i = 0; i < menus.length; i++) {
            //alert(menus[i] + "----" + menus[i].menuprice);
			if ( "hidden" == menus[i].display ) {
				$("#menu" + menus[i].id).hide();
				continue;
			}
            updater.showMenu(menus[i]);
            menunum = parseInt(menunum) + 1;
            menusum = parseInt(menusum) + parseInt(menus[i].menuprice);
            if ( userid == menus[i].fromuserid) {
                personmenusum = parseInt(personmenusum) + parseInt(menus[i].menuprice);
            }
			if ( menus[i].fromuserid != $("#userid").val() ) {
				$("#menudelbutton" + menus[i].id).hide();
				//alert("#menudelbutton" + menus[i].id + ":" + $("#menudelbutton" + menus[i].id).val());
			}
        }
        $("#menusumid").text(menusum);
        $("#personmenusumid").text(personmenusum);
        $("#menunumid").text(menunum);
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


