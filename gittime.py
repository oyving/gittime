
import sys
import subprocess
import StringIO
import datetime
import re
import stat

# how to split Date: Fri ... from each other
field_split = re.compile(r":\s*")


def verify_installation(request):
    "Should check if the file is under git control"
    return 1


def cb_filestat(args):
    """Looks up the creation time of a file in git, and uses that for the publishing time
    in pyblosxom."""
    
    filename = args['filename']

    git = subprocess.Popen(["git", "log", "--date=raw", "--", filename], stdout=subprocess.PIPE)
    content = git.stdout.readlines()
    dates = []

    for line in filter(lambda x: x.startswith("Date:"), content):
        line = line.strip()
        line = field_split.split(line, 1)
        dates.append(int(line[1][:-6]))
	
	dates.sort()
	mtime = list(args['mtime'])
	mtime[stat.ST_MTIME] = dates[0]
	args['mtime'] = tuple(mtime)
	
	return args
	
	
	