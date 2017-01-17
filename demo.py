# On a headless machine, you should probably run: xvfb-run python demo.py
import sys
import json
import getpass
import formatters 

from webadvisor import WebAdvisor

if len(sys.argv) == 1 :     
    print "Enter your WebAdvisor username:"
    username = sys.stdin.readline().strip()
    print "Enter your WebAdvisor password:"
    pw = getpass.getpass().strip()
    wave = WebAdvisor(username, pw, 's17')
    rosters = wave.get_rosters()
    print "Writing rosters.json"
    f = open('rosters.json', 'w')
    f.write(json.dumps(rosters))
    f.close()
    del wave
elif len(sys.argv) == 2:
    f = open(sys.argv[1], 'r')
    rosters = json.loads(f.read())
    f.close()

else:
    print 'usage:\n\t' + sys.argv[0] + ' [<json-input>]'
    exit -1

# process rosters
formatters.gen_maillist(rosters)
formatters.gen_unix(rosters)
formatters.gen_vlab(rosters)
formatters.gen_netlab(rosters)
formatters.gen_netacad(rosters)
formatters.gen_csv(rosters)
formatters.gen_sql(rosters)

