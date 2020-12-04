import sys, os, subprocess
from .conf import getrundir
tail  = '/usr/bin/tail'
less  = '/usr/bin/less'
reset = '/usr/bin/reset'
instance_not_found = "Instance '%s' not found"
loggin_not_configured = "Logging is not configured for '%s', check configuration file\n"
log_file_does_not_exist = "Logfile '%s' does not exist yet, do you want to create it?"
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
    if not conf.has_section(name): print_err_and_exit(instance_not_found % name, 1)
    if not conf.has_option(name, 'logfile') or conf.get(name, 'logfile') == '-': print_err_and_exit(loggin_not_configured % name, 1)
    logfile_path = conf.get(name, 'logfile') if os.path.isabs(conf.get(name, 'logfile')) else '/'.join([conf.get(name,'chdir'),conf.get(name, 'logfile')])
    if not os.path.isfile(logfile_path):
        if yes_or_no(log_file_does_not_exist % logfile_path):
            os.makedirs(os.path.split(logfile_path)[0], exist_ok=True)
            open(logfile_path, 'w').close()
        else:
            print_err_and_exit("then there will be no logs\n",1)
    return logfile_path

def print_err_and_exit(errormsg, exitcode):
    sys.stderr.write(errormsg)
    sys.exit(exitcode)

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
       return True
    elif reply[0] == 'n':
       return False
    else:
       return yes_or_no("Uh? please retry")
