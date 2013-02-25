#!/usr/bin/env python

import unittest
import mymail
import subprocess
import os

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

Note on last point.  The emphise is on "well-formed" email addresses. Some
email addresses can be very weird, but still valid:
Valid email addresses
=====================
niceandsimple@example.com
very.common@example.com
a.little.lengthy.but.fine@dept.example.com
disposable.style.email.with+symbol@example.com
user@[IPv6:2001:db8:1ff::a0b:dbd0]
"much.more unusual"@example.com
"very.unusual.@.unusual.com"@example.com
"very.(),:;<>[]\".VERY.\"very@\\ \"very\".unusual"@strange.example.com
postbox@com (top-level domains are valid hostnames)
admin@mailserver1 (local domain name with no TLD)
!#$%&'*+-/=?^_`{}|~@example.org
"()<>[]:,;@\\\"!#$%&'*+-/=?^_`{}| ~.a"@example.org
" "@example.org (space between the quotes)
"""

class testEmailFind(unittest.TestCase):
    """Check that the email address routine works properly"""

    goodAddresses = ('aebhughes@gmail.com',
                     'info@custom-soft.co.za',
                     'fred.Bloggs@my-domain.ac.co.uk',
                     'postbox@com',
                     )

    textInput = """This is grabage but aebhughes@gmail.com is included
as well as///info@custom-soft.co.za\\\and fred.Bloggs@my-domain.ac.co.uk
and-a-rather-strange-one postbox@com"""

    def testRightNumber(self):
        """This checks the correct number of emails extracted"""
        t1 = mymail.get_email(self.textInput)
        self.assertEqual(len(self.goodAddresses), len(t1))

    def testGoodContent(self):
        """actual elements match known values"""
        t1 = mymail.get_email(self.textInput)
        if t1:
            for email in t1:
                self.assertIn(email, self.goodAddresses)
        else:
            assert('No emails extracted')


class testParmDetect(unittest.TestCase):

    def testPipedOK(self):
        """Check piped input is detected"""
        cmd = './mymail.py < mymail.testdata.txt'
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()
        self.assertEqual(stderr, '')

    def testOtherPipedOK(self):
        """Check piped input is with | works"""
        cmd = 'cat mymail.testdata.txt | ./mymail.py'
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()
        self.assertEqual(stderr, '')

    def testGetParm(self):
        """Check if module detects parameters"""
        cmd = './mymail.py mymail.testdata.txt'
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()
        self.assertEqual(stderr, '')

    def testGetParmWithFile(self):
        """Check if module detects if create parameter"""
        cmd = './mymail.py -f outfile mymail.testdata.txt'
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()
        self.assertEqual(stderr, '')

    def testFileExists(self):
        self.assertTrue(os.path.exists('outfile'))
        os.remove('outfile')

class testParmManagement(unittest.TestCase):

    path = './my_mail/test/'
    fname = 'myfile.txt'

    def setUp(self):
        """Create test scaffolding"""
        os.makedirs(self.path)
        tmp_file = open(self.path + self.fname, 'w')
        tmp_file.write('my test file')
        tmp_file.close()

    def testFindsFile(self):
        """Does it find the file path?"""
        cmd = './mymail.py tmp/test/myfile.txt'
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()
        self.assertNotEqual(stdout, '')
        self.assertEqual(stderr, '')

    def testURLFind(self):
        """does it recognise a URL and find it?"""
        cmd = './mymail.py www.google.com'
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()
        self.assertNotEqual(stdout, '')
        self.assertEqual(stderr, '')

    def testNoInputFound(self):
        """handels invalid parmameters neatly"""
        cmd = './mymail.py blah'
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()
        self.assertIn('Error:', stdout)

    def tearDown(self):
        """remove test scaffolding"""
        os.remove(self.path + self.fname)
        os.removedirs(self.path)
        

if __name__ == '__main__':
    unittest.main()
