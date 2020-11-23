import sys, os, subprocess
from .conf import getrundir
tail  = '/usr/bin/tail'
less  = '/usr/bin/less'
reset = '/usr/bin/reset'

def logs(conf, args):
    name = args.name
    logfile_path = log_file_path(name, conf)
    if args.tail:
        print(args.tail)
        subprocess.run([tail, "-n", args.tail, logfile_path], stdout=sys.stdout)
    else:
        try:
            subprocess.run([less, logfile_path], stdin=sys.stdin, stdout=sys.stdout)
        except KeyboardInterrupt:
            # reset terminal on reckless close
            subprocess.run(reset)

def log_file_path(name, conf):
    if not conf.has_section(name):    
        sys.stderr.write("Instance '%s' not found"%name)
        sys.exit(1)
    if not conf.has_option(name, 'logfile') or conf.get(name, 'logfile') == '-':
        sys.stderr.write("Logfile was not set for '%s'"%name)
        sys.exit(1)
    logfile_path = conf.get(name, 'logfile') if os.path.isabs(conf.get(name, 'logfile')) else '/'.join([conf.get(name,'chdir'),conf.get(name, 'logfile')])
    if not os.path.isfile(logfile_path):
        sys.stderr.write("Logfile '%s' does not exist"%logfile_path)
        sys.exit(1)
    return logfile_path

