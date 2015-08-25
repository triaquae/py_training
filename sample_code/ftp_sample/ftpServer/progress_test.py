

import sys
import time 
sys.stdout.write("[ ]")
#sys.stdout.flush()
str_mark= ''
for i in range(50):
  str_mark +="="
  sys.stdout.write("%s>\r" % str_mark)
  sys.stdout.flush()
  time.sleep(0.1)


