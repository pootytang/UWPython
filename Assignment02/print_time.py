import time
import datetime

html_head = """
<html>
<head><title>Assignment 2</title></head>
"""

html_body1 = """
<body>
<font color=\"red\">Here is the time:</font>
"""
html_body1 = html_body1 + str(time.time()) + "<br />"

html_body2 = """
<font color=\"green\">and again:</font>
"""
html_body2 = html_body2 + " " + str(datetime.datetime.now()) + "<br />"

html_body = html_body1 + html_body2

html_end = """
</body>
</html>
"""


print html_head
print html_body
print html_end

