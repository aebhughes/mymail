================================
MYMAIL: email extraction utility
================================

mymail.py:

This was originally constructed as a test for an interveiw. However, it
is quite useful as a utility to extract email addresses from a few different
sources.

The original requirement was to construct a  command-line level script that:
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
---------------------
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

Not all these are catered for.
