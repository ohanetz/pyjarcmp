#!/usr/bin/python

import os
import sys
import subprocess
from logger import Logger
from chdir import chdir
from jar_compare import jar_compare


## Defaults ##
DEFAULT_DIFF_APP = "diff"
DEFAULT_REPORTS_DIR = "/".join((os.getcwd(), "reports"))
DEFAULT_WORKING_DIR = "/".join((os.getcwd(), "tmp"))


def print_usage():
    print "Usage: pyjarcmp.py -o OLD_JAR_PATH -n NEW_JAR_PATH [OPTIONS]"
    print "Options:"
    print " -exclude_meta_inf   Don't compare content in /META-INF/ folder"
    print " -exclude [FILES]    List of files to exclude from the comparison" 



def __main__():
    if len(sys.argv) < 5:
        print_usage()
        exit(1)

    if not "-o" in sys.argv or not "-n" in sys.argv:
        print "You must provide both old and new jar paths"
        print_usage()
        exit(1)

    old_jar_path = sys.argv[sys.argv.index("-o") + 1]
    new_jar_path = sys.argv[sys.argv.index("-n") + 1]

    l = Logger("/".join((os.getcwd(), "pyjarcmp.log")))

    diff_app = DEFAULT_DIFF_APP
    reports_dir = DEFAULT_REPORTS_DIR
    working_dir = DEFAULT_WORKING_DIR

    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    with chdir(working_dir):
        l.log("Removing old data")
        if os.path.exists("old_jar"):
            subprocess.call("rm -rf old_jar".split(" "))
        if os.path.exists("new_jar"):
            subprocess.call("rm -rf new_jar".split(" "))

        l.log("Creating working dirs")
        os.mkdir("old_jar")
        os.mkdir("new_jar")


    with chdir("/".join((working_dir, "old_jar"))):
        l.log("Extracting old jar")
        subprocess.call("jar -xf".split(" ") + [old_jar_path])

    with chdir("/".join((working_dir, "new_jar"))):
        l.log("Extracting new jar")
        subprocess.call("jar -xf".split(" ") + [new_jar_path])


    l.log("Getting old jar files list")
    old_jar_files = []
    for subdir, dirs, files in os.walk("/".join((working_dir, "old_jar"))):
        for f in files:
            old_jar_files.append(os.path.join(subdir, f))

    l.log("Getting new jar files list")
    new_jar_files = []
    for subdir, dirs, files in os.walk("/".join((working_dir, "new_jar"))):
        for f in files:
            new_jar_files.append(os.path.join(subdir, f))

    if "-exclude_meta_inf" in sys.argv:
        l.log("Excluding META-INF")
        old_jar_files = [x for x in old_jar_files if x.find("/META-INF/") < 0]
        new_jar_files = [x for x in new_jar_files if x.find("/META-INF/") < 0]

    if "-exclude" in sys.argv:
        excludes = sys.argv[sys.argv.index("-exclude") + 1].split(",")
        for efile in excludes:
            l.log("Excluding " + efile)
            old_jar_files = [x for x in old_jar_files if x.find(efile.strip()) < 0]
            new_jar_files = [x for x in new_jar_files if x.find(efile.strip()) < 0]
            

    exit(jar_compare(old_jar_files, new_jar_files))


__main__()
