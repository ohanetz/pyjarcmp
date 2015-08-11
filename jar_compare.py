import subprocess

def jar_compare(old_jar_files, new_jar_files):
    if not len(old_jar_files) == len(new_jar_files):
        print "Number of files differ: " + str(len(old_jar_files)) + " against " + str(len(new_jar_files))
        return 1

    for old_file in old_jar_files:
        new_file = old_file.replace("old_jar", "new_jar")

        if not subprocess.call(["diff", old_file, new_file]) == 0:
            print "Difference in file: " + new_file
            return 1

    print "Files are identical"
    return 0
