
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

    def test_conf_port_tcp(self):
        with TestDir() as t:
            confname = t.dir+'/procServ.d/instance-3.conf'
            with open(confname, 'x') as F:
                F.write("""
[instance-3]
command = /bin/sh -c blah
chdir = /somedir
port = 6666
""")
            generator.run(t.dir+'/run')
            service = t.dir+'/run/procserv-instance-3.service'
            with open(service, 'r') as F:
                content = F.read()
                self.assertEqual(content, """
[Unit]
Description=procServ for instance-3
After=network.target remote-fs.target
ConditionPathIsDirectory=/somedir

[Service]
Type=simple
ExecStart=%s --system instance-3 --port 6666
RuntimeDirectory=procserv-instance-3
StandardOutput=syslog
StandardError=inherit
SyslogIdentifier=procserv-instance-3

[Install]
WantedBy=multi-user.target
""" % generator.which('procServ-launcher'))

    def test_conf_basic_logfile_relpath(self):
        with TestDir() as t:
            logfile = 'log.txt'
            chdir   = '/somedir'
            confname = t.dir+'/procServ.d/instance-5.conf'
            with open(confname, 'x') as F:
                F.write("""
[instance-5]
command = /bin/sh -c blah
chdir = /somedir
logfile = log.txt
""")
            generator.run(t.dir+'/run')
            service = t.dir+'/run/procserv-instance-5.service'
            with open(service, 'r') as F:
                content = F.read()
                self.assertEqual(content, """
[Unit]
Description=procServ for instance-5
After=network.target remote-fs.target
ConditionPathIsDirectory=/somedir

[Service]
Type=simple
ExecStart={0} --system instance-5 --logfile {1}
RuntimeDirectory=procserv-instance-5
StandardOutput=syslog
StandardError=inherit
SyslogIdentifier=procserv-instance-5

[Install]
WantedBy=multi-user.target
""".format(generator.which('procServ-launcher'), logfile))
            
    def test_conf_basic_logfile_abspath(self):
        with TestDir() as t:
            logfile = os.path.expanduser("~") + '/random/dir/log.txt'
            chdir   = '/somedir'
            confname = t.dir+'/procServ.d/instance-6.conf'
            with open(confname, 'x') as F:
                F.write("""
[instance-6]
command = /bin/sh -c blah
chdir = /somedir
logfile = %s
""" % logfile)
            generator.run(t.dir+'/run')
            service = t.dir+'/run/procserv-instance-6.service'
            with open(service, 'r') as F:
                content = F.read()
                self.assertEqual(content, """
[Unit]
Description=procServ for instance-6
After=network.target remote-fs.target
ConditionPathIsDirectory=/somedir

[Service]
Type=simple
ExecStart={0} --system instance-6 --logfile {1}
RuntimeDirectory=procserv-instance-6
StandardOutput=syslog
StandardError=inherit
SyslogIdentifier=procserv-instance-6

[Install]
WantedBy=multi-user.target
""".format(generator.which('procServ-launcher'), logfile ))

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
