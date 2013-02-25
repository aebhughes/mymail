#!/usr/bin/env python

import sys
import re
import os
import urllib2

""" Objective of mymail.py: To read a text file that has email addresses
peppered throughout, extract those email addresses and output the list of
extracted addresses.  

Requirements:
-   command-line level script that:
    +  accepts stdin text input (piped)
    +  accepts URL that is used as input (wget)
    +  accepts path to input text file 
    +  outputs to stdout
    +  outputs to file/path
    +  handles infinate input file sizes
    +  only outputs well formed email addresses
"""

def get_email(intext):
    """function to extract all email addresses from a block of text
       Note that the understanding is for *well formed* email
       addresses.  The more obscure (though valid) forms may be
       excluded"""
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', intext)
    return emails

def get_parms(argv = sys.argv):
    """detects if piped or parmed input and returns parameters found
    as a list """

    if sys.stdin.isatty():  # cmd line?
        return argv[1:]
    elif os.isatty(True):   # piped?
        ret_list = ['piped']
        for arg in argv[1:]:
            ret_list.append(arg)
        return ret_list
    return []

def output_method(p_list):
    """determine if output type is stdout or a file"""
    if '-h' in p_list:
        print """
        Usage: ./mymail.py [-f <outfile>] <in-file>
        or:    ./mymail.py [-f <outfile>] < <in-file> i.e. piped
               
        """
        sys.exit(0)
    if '-f' in p_list:
        p_list.pop(p_list.index('-f'))
        fname = p_list.pop(0)
        out_method = open(fname, 'w')
    else:
        out_method = sys.stdout
    return out_method, p_list
        

def main():
    """main process: Determine between piped input, file input or URL
       and read input searching for valid email addresses.
       Note that input size is immaterial"""
    parms = get_parms()
    outfile, parms = output_method(parms)
    if not parms:
        print 'Error: no valid input found: run ./mymail.py -h for options'
        sys.exit(1)
    if parms[0] == 'piped':
        for inline in sys.stdin.readlines():
            for email in get_email(inline):
                print >>outtype, email
    else:
        try:
            url = urllib2.urlopen(parms[0])
            for inline in url:
                for email in get_email(inline):
                    print >>outtype, email
        except ValueError, urllib2.URLError:
            try:
                fname = open(parms[0], 'r')
                for inline in fname:
                    for email in get_email(inline):
                        print >>outtype, email
            except IOError as e:
                print 'Error: input file not found'
                print './mymail.py -h for usage'
                outfile.close()
                sys.exit(1)
    outfile.close()
 
if __name__ == "__main__":
    main()
