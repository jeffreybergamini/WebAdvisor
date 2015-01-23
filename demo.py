# On a headless machine, you should probably run: xvfb-run python demo.py
from webadvisor import WebAdvisor
wave = WebAdvisor('username', 'passphrase', 's15')
print wave.get_rosters()
del wave
