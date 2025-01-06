---
date: 2024-06-21
---

# Adding a DDNS provider to my router

I self-host a Minecraft server, and keeping up with IP address changes is very annoying.
When someone suggested I use freemyip, I immediately checked it out, and liked the simplicity of it.
I got a subdomain, and I was ready to go.

I logged into my router, checked the list of DDNS providers, and... it wasn't there.
I searched around for how to add a DDNS provider to my router, but no luck.

I then remembered that I had rooted the router before, and tried to log in via SSH.
Unfortunately, I had forgotten the password I set when I rooted it.
I used autoflashgui to reset the password (I put `echo root:root | chpasswd` in the command field, and selected "Ping" as the execution method), and I was in.

I started poking around on the command line:
```
root@dsldevice:~# cd /www
root@dsldevice:/www# ls
cards         docroot       lua           snippets      wizard-cards
root@dsldevice:/www# ls docroot/
ajax                  css                   gateway.lp            intercept.lp          login.lp              parental-block.lp     password.lp
change-access-key.lp  font                  img                   js                    modals                password-reset.lp
root@dsldevice:/www# grep freedns docroot/*
root@dsldevice:/www# grep freedns docroot/*/*
docroot/modals/wanservices-modal.lp:    ddns_supported_services["freedns.afraid.org-basicauth"] = "afraid.org-basicauth"
docroot/modals/wanservices-modal.lp:    ddns_supported_services["freedns.afraid.org-keyauth"] = "afraid.org-keyauth"
root@dsldevice:/www# cd docroot/modals/
root@dsldevice:/www/docroot/modals# vi wanservices-modal.lp
...
-- open the supported services file that come with the ddns package
    local ddns_supported_services , valid_services = {}, {}
    local path = format("/etc/ddns/%s", name)
    local f = io.open(path, "r")
...
root@dsldevice:/www/docroot/modals# ls /etc/ddns/
root@dsldevice:/www/docroot/modals# cat /etc/ddns/*
...
"freedns.afraid.org"	"http://[USERNAME]:[PASSWORD]@freedns.afraid.org/nic/update?hostname=[DOMAIN]&myip=[IP]"
...
```
So, I found the right file; all I needed to do was add an entry, which I proceeded to do.
```
"freemyip.com"		"https://freemyip.com/update?token=[PASSWORD]&domain=[DOMAIN]"
```
I then looked in the router settings; the entry was there, I added the token and domain, and it worked perfectly. (First try!)
