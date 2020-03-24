import sys
print(sys.path)
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
    print('!!!!')
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
print(sys.path)
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
    print('@@@@@')

