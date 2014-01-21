===================================
os-collect-config on oslo.messaging
===================================

If you don't know what it is, see the description in the original repo:
https://github.com/openstack/os-collect-config

What does it do?
================

It does the same as the original os-collect-config except it works over
oslo.messaging instead of metadata service. Naturally it now works in
RPC manner.

Usage
=====

Comparing with the original os-collect-config there are two changes:

  * You need to use client on the server side to reach out
    the os-collect-config deployed on an instance
  * You need to supply proper parameters for oslo.messaging in config

The client is here: os-collect-config/collect_client.py

Note that currently requirements.txt list the requirements needed to 
work with Rabbit MQ. If you want to use different implementation, replace 
Kombu with the propoper package.

To play with it, install and start Rabbit MQ with the default
settings and specify a couple additional parameter in both client and
os-collect-config configs:
 * rabbit_host - Rabbit MQ IP address
 * server_id - just an ID which needs to be the same both on client
   and os-collect-config. Used to distinguish different intances.

