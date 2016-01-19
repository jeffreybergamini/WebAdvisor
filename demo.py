# On a headless machine, you should probably run: xvfb-run python demo.py
import sys
import json
import getpass
import formatters 

from webadvisor import WebAdvisor

print "Enter your WebAdvisor username:"
username = sys.stdin.readline().strip()
print "Enter your WebAdvisor password:"
pw = getpass.getpass().strip()
wave = WebAdvisor(username, pw, 's16')
rosters = wave.get_rosters()

# print rosters
print "Writing rosters.json"
f = open('rosters.json', 'w')
f.write(json.dumps(rosters))
f.close()

# process rosters
formatters.gen_maillist(rosters)
formatters.gen_unix(rosters)
formatters.gen_vlab(rosters)
formatters.gen_netlab(rosters)

del wave
