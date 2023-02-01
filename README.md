# Python console (WIP)
A simple python program that emulates console and allows user to perform basic operations on files, open apps and search for websites or videos on browser.

## Goal
For a second final assigment for my neautral language processing course, I choosed to create console project, that is supposed to perfroms some basic actions,
like playing videos, searching browser or opening files and apps, all that using commends parsed by pythons PLY library. My additional action is moving around directories.

## How it works
The core of the program is standard lex-yacc tokenizer and parser. In a loop that emulates the way console works it reads user's input, tokenizes it and parses. The returned result will later be used in a function that checks what kind of action will be performed and what sort of argument (could be name or path) was received from user.

To avoid errors, the name of a song, website or whatever we want to open (except for directory path) has to be given in between " " signs, as I didn't come up with better regex yet.

In order to play youtube videos and search internet I made use of webbrowser, googlesearch and youtubesearchpython libraries.
As for opening apps, I used AppOpener (it's killing me how straightforward those libs name are) in it's 1.5 version.

## Future improvments
Currently program is at it's final "basic" form, I'd still like to add some more functions, improve parser and make it run as an .exe file
