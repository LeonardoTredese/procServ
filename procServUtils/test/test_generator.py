import os
import unittest

from .. import generator
from . import TestDir

class TestGen(unittest.TestCase):
    def test_conf_basic(self):
        with TestDir() as t:
            confname = t.dir+'/procServ.d/instance-0.conf'
            with open(confname, 'x') as F:
                F.write("""
[instance-0]
command = /bin/sh -c blah
chdir = /somedir
""")
            generator.run(t.dir+'/run')
            service = t.dir+'/run/procserv-instance-0.service'
            with open(service, 'r') as F:
                content = F.read()
                self.assertEqual(content, """
[Unit]
Description=procServ for instance-0
After=network.target remote-fs.target
ConditionPathIsDirectory=/somedir

[Service]
Type=simple
ExecStart=%s --system instance-0
RuntimeDirectory=procserv-instance-0
StandardOutput=syslog
StandardError=inherit
SyslogIdentifier=procserv-instance-0


[Install]
WantedBy=multi-user.target
""" % generator.which('procServ-launcher'))
    def test_conf_user(self):
        with TestDir() as t:
            confname = t.dir+'/procServ.d/instance-1.conf'
            with open(confname, 'x') as F:
                F.write("""
[instance-1]
command = /bin/sh -c blah
chdir = /somedir
user = someone
""")
            generator.run(t.dir+'/run')
            service = t.dir+'/run/procserv-instance-1.service'
            with open(service, 'r') as F:
                content = F.read()
                self.assertEqual(content, """
[Unit]
Description=procServ for instance-1
After=network.target remote-fs.target
ConditionPathIsDirectory=/somedir

[Service]
Type=simple
ExecStart=%s --system instance-1
RuntimeDirectory=procserv-instance-1
StandardOutput=syslog
StandardError=inherit
SyslogIdentifier=procserv-instance-1

User=someone

[Install]
WantedBy=multi-user.target
""" % generator.which('procServ-launcher'))
    def test_conf_group(self):
        with TestDir() as t:
            confname = t.dir+'/procServ.d/instance-2.conf'
            with open(confname, 'x') as F:
                F.write("""
[instance-2]
command = /bin/sh -c blah
chdir = /somedir
group = somegroup
""")
            generator.run(t.dir+'/run')
            service = t.dir+'/run/procserv-instance-2.service'
            with open(service, 'r') as F:
                content = F.read()
                self.assertEqual(content, """
[Unit]
Description=procServ for instance-2
After=network.target remote-fs.target
ConditionPathIsDirectory=/somedir

[Service]
Type=simple
ExecStart=%s --system instance-2
RuntimeDirectory=procserv-instance-2
StandardOutput=syslog
StandardError=inherit
SyslogIdentifier=procserv-instance-2

Group=somegroup

[Install]
WantedBy=multi-user.target
""" % generator.which('procServ-launcher'))

    def test_system(self):
        with TestDir() as t:
            confname = t.dir+'/procServ.d/blah.conf'
            with open(confname, 'w') as F:
                F.write("""
[blah]
command = /bin/sh -c proprot
chdir = /somedir
user = someone
group = controls
""")

            generator.run(t.dir+'/run')
            service = t.dir+'/run/procserv-blah.service'
            with open(service, 'r') as F:
                content = F.read()
                self.assertEqual(content, """
[Unit]
Description=procServ for blah
After=network.target remote-fs.target
ConditionPathIsDirectory=/somedir

[Service]
Type=simple
ExecStart=%s --system blah
RuntimeDirectory=procserv-blah
StandardOutput=syslog
StandardError=inherit
SyslogIdentifier=procserv-blah

User=someone
Group=controls

[Install]
WantedBy=multi-user.target
""" % generator.which('procServ-launcher'))
