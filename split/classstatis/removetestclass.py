import sys

'''
if we should filter test class when understand analysis. then we can ignore this python file.
'''
'''
filter out testclass and inner classes from classlist in xwiki-platform108
filter string: .test.     or   Test    or (
'''
infilename = sys.argv[1]
outfilename = sys.argv[2]

fin = open(infilename, "r")
fout = open(outfilename, "w")
for line in fin:
    if (".test."  not in line) and ("Test" not in line) and ("(" not in line) and ("test" not in line):
        fout.write(line)
fin.close()
fout.close()
