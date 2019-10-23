# A pythonic way of automating and visualizing tcpdump on a raspberry pi.

1. Current issue that I'm running into is that the reload button of the browser is the same as pressing the start or stop tcpdump button.  I need a way of testing if tcpdump is running before loading the page.  I'm trying to use before\_request to do this.  I've added a before\_request decorator function.
