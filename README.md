# Hachi NIO protocol lib for Python

Hachi Protocol is a lightwight network I/O socket communication format to transfer data between applications based on my old project [irineu/eight-protocol](https://github.com/irineu/eight-protocol) initialy designed for NodeJS only.

<img src="http://irineuantunes.com/hachi-protocol.svg" height="100" valign="middle"> for <img src="https://upload.wikimedia.org/wikipedia/commons/f/f8/Python_logo_and_wordmark.svg" height="80" valign="bottom">

## Objective
When you test a simple socket communication, in the more of times everything works fine, but when your project grow up, after publish and test with remote and bad connections, you will get some problems with truncated messages or messages with extra data (part of the next message). It is normal. You'll need create a protocol to handle this situation, maybe implement a header or a terminator (bad ideia), maybe you are already frustated with that notice.

The Hachi Protocol is an implementation plug-and-play of a transparent protocol for handle those situations for you, and the most important: it does not change your code too much. The protocol itself is encapsulated in this library and you can do your business stuff without take care about the bits (like the HTTP protocol).

The message transfered is distributed in two sections:
##### Header
A Key/Value object to identify the message (parameter: transaction, id, token, type, etc...), you can set any object.
##### Body
Binary Data, you can pass anything here

## Quick Start

TODO
