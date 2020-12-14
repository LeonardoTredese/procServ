import os
import unittest

from .. import manage
from ..manage import getargs, main
from . import TestDir

manage.systemctl = '/bin/true'

class TestGen(unittest.TestCase):
    def test_add_basic(self):
        with TestDir() as t:
            main(getargs(['add', '-C', '/somedir', 'instance-0', '--', '/bin/sh', '-c', 'blah']), test=True)
            #os.system('find '+t.dir)

            confname = t.dir+'/procServ.d/instance-0.conf'

            self.assertTrue(os.path.isfile(confname))
            with open(confname, 'r') as F:
                content = F.read()

            self.assertEqual(content, """
[instance-0]
command = /bin/sh -c blah
chdir = /somedir
""")
    def test_add_user(self):
        with TestDir() as t:
            main(getargs(['add',
                          '-C', '/somedir',
                          '-U', 'someone',
                          'instance-1', '--', '/bin/sh', '-c', 'blah']), test=True)

            confname = t.dir+'/procServ.d/instance-1.conf'

            self.assertTrue(os.path.isfile(confname))
            with open(confname, 'r') as F:
                content = F.read()

            self.assertEqual(content, """
[instance-1]
command = /bin/sh -c blah
chdir = /somedir
user = someone
""")
    def test_add_group(self):
        with TestDir() as t:
            main(getargs(['add',
                          '-C', '/somedir',
                          '-G', 'somegroup',
                          'instance-2', '--', '/bin/sh', '-c', 'blah']), test=True)

            confname = t.dir+'/procServ.d/instance-2.conf'

            self.assertTrue(os.path.isfile(confname))
            with open(confname, 'r') as F:
                content = F.read()

            self.assertEqual(content, """
[instance-2]
command = /bin/sh -c blah
chdir = /somedir
group = somegroup
""")

    def test_add_port_tcp(self):
        with TestDir() as t:
            main(getargs(['add',
                          '-C', '/somedir',
                          '-P', 'tcp:6666',
                          'instance-3', '--', '/bin/sh', '-c', 'blah']), test=True)

            confname = t.dir+'/procServ.d/instance-3.conf'

            self.assertTrue(os.path.isfile(confname))
            with open(confname, 'r') as F:
                content = F.read()

            self.assertEqual(content, """
[instance-3]
command = /bin/sh -c blah
chdir = /somedir
port = tcp:6666
""")

    def test_add_port_unix(self):
        with TestDir() as t:
            main(getargs(['add',
                          '-C', '/somedir',
                          '-P', 'unix:test-port', 
                          'instance-4', '--', '/bin/sh', '-c', 'blah']), test=True)

            confname = t.dir+'/procServ.d/instance-4.conf'

            self.assertTrue(os.path.isfile(confname))
            with open(confname, 'r') as F:
                content = F.read()

            self.assertEqual(content, """
[instance-4]
command = /bin/sh -c blah
chdir = /somedir
port = unix:test-port
""")

    def test_add_basic_logfile_relpath(self):
        with TestDir() as t:
            logfile = 'log.txt'
            chdir   = '/somedir'
            main(getargs(['add',
                          '-C', chdir,
                          '-L', logfile,
                          'instance-5', '--', '/bin/sh', '-c', 'blah']), test=True)
            confname = t.dir+'/procServ.d/instance-5.conf'
            self.assertTrue(os.path.isfile(confname))
            with open(confname, 'r') as F:
                self.assertEqual(F.read(), """
[instance-5]
command = /bin/sh -c blah
chdir = /somedir
logfile = log.txt
""")
            self.assertTrue(os.path.isfile(chdir + '/' + logfile))
            os.remove(chdir + '/' + logfile)
            os.rmdir(chdir)
            self.assertFalse(os.path.isfile(chdir + '/' + logfile))
            
    def test_add_basic_logfile_abspath(self):
        with TestDir() as t:
            logfile = os.path.expanduser("~") + '/random/dir/log.txt'
            chdir   = '/somedir'
            main(getargs(['add',
                          '-C', chdir,
                          '-L', logfile,
                          'instance-6', '--', '/bin/sh', '-c', 'blah']), test=True)
            confname = t.dir+'/procServ.d/instance-6.conf'
            self.assertTrue(os.path.isfile(confname))
            with open(confname, 'r') as F:
                self.assertEqual(F.read(), """
[instance-6]
command = /bin/sh -c blah
chdir = /somedir
""" + "logfile = " + logfile + "\n")

            self.assertTrue(os.path.isfile(logfile))
            os.remove(logfile)
            os.rmdir(os.path.expanduser("~") + '/random/dir')
            os.rmdir(os.path.expanduser("~") + '/random')
            self.assertFalse(os.path.isfile(logfile))

    def test_remove(self):
        with TestDir() as t:
            # we won't remove this config, so it should not be touched
            with open(t.dir+'/procServ.d/other.conf', 'w') as F:
                F.write("""
[other]
command = /bin/sh -c blah
chdir = /somedir
user = someone
group = controls
""")

            confname = t.dir+'/procServ.d/blah.conf'
            with open(confname, 'w') as F:
                F.write("""
[blah]
command = /bin/sh -c blah
chdir = /somedir
user = someone
group = controls
""")

            main(getargs(['remove', '-f', 'blah']), test=True)

            self.assertFalse(os.path.isfile(confname))
            self.assertTrue(os.path.isfile(t.dir+'/procServ.d/other.conf'))

            confname = t.dir+'/procServ.d/blah.conf'
            with open(confname, 'w') as F:
                F.write("""
[blah]
command = /bin/sh -c blah
chdir = /somedir
user = someone
group = controls

[more]
# not normal, but we shouldn't nuke this file if it contains other instances
""")

            main(getargs(['remove', '-f', 'blah']), test=True)

            self.assertTrue(os.path.isfile(confname))
            self.assertTrue(os.path.isfile(t.dir+'/procServ.d/other.conf'))
