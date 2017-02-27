import time
import webbrowser

i = 0
total = 6
print 'running start' + time.ctime()
while i < total:
	time.sleep(3)
	webbrowser.open('http://www.baidu.com')
	i = i + 1
	print str(i) + time.ctime()
	
