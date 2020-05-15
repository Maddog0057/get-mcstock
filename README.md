# get-mcstock

Original code from here: https://forum.level1techs.com/t/automated-microcenter-stock-checking-updated/117256
Modifications only made to data parsing (for updated Micro Center Website) and replacing email notif with discord

HOW TO USE:

Replace the urls in the "URLS" list with what you're looking to buy
Replace storeSelected='121' with the number of your store (can be found by viewing source on the MC website, 121 is Cambridge, MA FYI)
Replace webhook_url = 'DISCORDWEBHOOKURLHERE' with your discord webhook, theres pretty good documentation on how to get this if you have a discord server

Personally (at the recommendation of the original author) I run this as a cron job on a centos server using the following setting:

*/5 * * * * /bin/python3 /opt/mc-stock/get-mcstock.py 2>&1 | /usr/bin/logger -t mcstock

This runs the script every 5 minutes and directs all output (stderr/stdout) to /var/log/messages with the tag "mcstock"

NOTE: If you run this as a cron job you need to explicitly set the location of the "items_in_stock" datafile or else it will never update the stock of the item locally for the next run

REQUIREMENTS:

Python3 (not 2.7)

Most of the imports are standard and should be already included with your installation of python3, requests and pickle might need to be installed using pip
