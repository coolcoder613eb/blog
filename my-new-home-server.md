---
date: 2024-08-21
---
# My new home server
Yesterday I got my new home server, a Panasonic Toughbook CF-19 Mk4 with 8GB of RAM, an Intel i5 U 540, and a 320GB SSD.

I installed headless Debian 12, overwriting the Windows 7 install already there, and stopped for the night.
Today I started on moving my servers from my Raspberry Pi to my new server.
First, I adressed the issue that prompted me to get this laptop in the first place, that is, the server occasionally getting unplugged, by using ChatGPT to help me write a script that would notify me on my Mac when the laptop gets unplugged,
which took most of the time. I then moved over my Quassel Core config (using [this](https://clover.moe/2013/11/17/how-to-move-quassel-core/) guide), and I copied over my minecraft server, using the Adoptium repo to install Java.
