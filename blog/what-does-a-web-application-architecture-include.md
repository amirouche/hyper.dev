# 2019/01/01 - What does a web application architecture include?

And what are the code patterns?

In this note, I will describe and introduce concepts related to web
developpement from the big picture to code patterns.

This article links to RFCs and man pages, it's a reminder for me to
read them one day.

## Big pictures

At the very beginning you type an Uniform Resource Locator
aka. URL [RFC 1738](https://www.ietf.org/rfc/rfc1738.txt) in the
location bar. Something like `http://hyperdev.fr/`.

The browser will request the Internet Protocol address
aka. IP [RFC 791](https://tools.ietf.org/html/rfc791) of the URL using
a Domain Name Service [RFC 1035](https://www.ietf.org/rfc/rfc1035.txt)
prolly configured
in [`/etc/resolv.conf`](https://linux.die.net/man/5/resolv.conf).

You query the DNS service using the [`dig`](https://linux.die.net/man/1/dig) command:

```
amirouche@ubudec:~$ dig hyperdev.fr

; <<>> DiG 9.10.3-P4-Ubuntu <<>> hyperdev.fr
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2891
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;hyperdev.fr.			IN	A

;; ANSWER SECTION:
hyperdev.fr.		2952	IN	A	92.222.88.65

;; Query time: 0 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Mon Nov 06 20:24:48 CET 2017
;; MSG SIZE  rcvd: 56
```

You decypher this without knowing DNS or whatever. There is only
one IP in the output.

At this point, the browser with the IP and the URL will construct a
HyperText Transfer Protocol
aka. HTTP/1.1 [RFC 2616](https://tools.ietf.org/html/rfc2616). This
HTTP packet is a *request* for the page you want.

You can simulate what the browser does at this point with
the [`nc`](https://linux.die.net/man/1/nc) command. For instance:

```
amirouche@ubudec:~$ nc 92.222.88.65 80
```

Then paste the following in the console:

```
GET / HTTP/1.1
Host: hyperdev.fr

```

Mind the last blank line.

The output will start with something like that:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3
Date: Mon, 06 Nov 2017 19:27:02 GMT
Content-Type: text/html
Content-Length: 3875
Last-Modified: Sat, 19 Aug 2017 13:31:40 GMT
Connection: keep-alive
ETag: "59983dbc-f23"
Accept-Ranges: bytes

<html><head><meta charset="utf-8" /><title>hyperdev.fr</title><link rel="stylesheet" href="/static/css/normalize.css" /><link rel="stylesheet" href="/static/css/app.css" /></head><body><div>
...
```

And even more HTML code. This is the server response.

At his point the browser will parse the response and prolly request
more files from the server and trigger at the same time the rendering
of the page [TODO: link how a browser render a page].

But a question remains, who answered the HTTP request? Well the answer
is: it depends. It depends whether there is cache or some other kind
of proxy between the browser and the server.

Also, nowdays HTTP requests happens most of the time over a secure
layer sometime called SSL but it's more likely using Transport Layer
Security protocol
aka. TLS [RFC 2246](https://www.ietf.org/rfc/rfc2246.txt).

Thanks to [Let's Encrypt](https://letsencrypt.org/) everybody can use
TLS for free.

To keep things simple we will imagine that there is no proxy and you
directly access the application server.
