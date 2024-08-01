#!/usr/bin/python3
import requests
import threading
import argparse
import queue
import colorama
from time import time
import os
import lib.logo as logo

def prepare_arg():
    parser = argparse.ArgumentParser(description="A Python Based SubDomain Finder :-", usage="./%(prog)s google.com", epilog="./%(prog)s google.com -w wordlist.txt -t 100 google.com -v")
    parser.add_argument("-d", "--domain",metavar="\b", dest="domain", help="Target Domain")
    parser.add_argument("-w", "--wordlist", metavar="\b", dest="wordlist", help="Custom Wordlist/Default:default.txt")
    parser.add_argument("-t", "--thread", metavar="\b",dest="thread", help="Number of Threads Default: 200")
    parser.add_argument("-v", "--verbose", dest="verbose",action="store_true", help="Verbose Output")
    parser.add_argument("-V", "--version", action="version",version="%(prog)s 1.0.0")
    argument = parser.parse_args()
    if not argument.domain:
        parser.error("[+] Target Domain Need....")
    return argument


arg = prepare_arg()
domain = arg.domain
wordlist = arg.wordlist
threads = arg.thread
verbose = arg.verbose

queues = queue.Queue()
subdomains = []
start_time = time()
logo.logo()


def find_domain(subdomain):
    hostname = subdomain+"."+domain
    header = {"User-Agent": "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"}
    try:
        r = requests.get(f"https://{hostname}",timeout=5)
        if r.status_code == 200:
            subdomains.append(hostname)
            if not verbose:
                pass
            else:
                print("https://"+hostname)

    except:
        pass

def get_queue(words):

    for single in words:
        queues.put(single)

def worker():
    while not queues.empty():
        subdomain = queues.get()
        find_domain(subdomain)
        if queues.empty():
            break

if wordlist == None:
    word = open('default.txt', 'r')
    words = word.read().splitlines()
    word.close()
else:
    word = open(arg.wordlist, 'r')
    words = word.read().splitlines()
    word.close()

get_queue(words)

list_thread = []

if not threads:
    for t in range(200):
        thread = threading.Thread(target=worker)
        list_thread.append(thread)
else:
    if threads:
        for t in range(int(threads)):
            thread = threading.Thread(target=worker)
            list_thread.append(thread)

if wordlist:
    print(f"WordList :- {wordlist}\n")
else:
    print("")

if verbose:
    print("Verbose Mode: True \n")
else:
    print("Verbose Mode: False \n")

for thread in list_thread:
    thread.start()
for thread in list_thread:
    thread.join()

if arg.verbose:
    pass 
else:
    for i in subdomains:
        print(f"https://"+i)

end_time = time()

print(f"Time Taken : {round(end_time-start_time, 2)}")