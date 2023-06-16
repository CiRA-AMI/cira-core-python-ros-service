import sys
import os

home_path = os.path.expanduser('~')
print("home_path : ", home_path)

if os.name == 'nt':
	sys.path.append('C:\\CiRA-CORE\\install\\lib\\site-packages')
	sys.path.append('C:\\opt\\ros\\melodic\\x64\\lib\\site-packages')
else :
	sys.path.append(home_path + '/.cira_core_install/cira_libs_ws/install/lib/python3/dist-packages')

import cv2
import rospy
from cira_msgs.srv import CiraFlowService2, CiraFlowService2Response
from sensor_msgs.msg import Image
from std_msgs.msg import String
import ros_numpy
import numpy as np
import json

service_name = ""  #enter service name
if service_name == "" :
	print("Please enter your service_name")
	quit()

rospy.init_node('cira_rosservice_server', anonymous=True)

def handle_service(req):
	payload = json.loads(req.flow_in.jsonstr)
	#print(payload)

	img = {}
	img['data'] = []
	if len(req.flow_in.img.data) > 0 :
		img = ros_numpy.numpify(req.flow_in.img)

	#implement your process here

	res = CiraFlowService2Response()
	payload_out = {}
	payload_out['ok'] = True
	res.flow_out.jsonstr = json.dumps(payload_out)
	if len(req.flow_in.img.data) > 0 :
		res.flow_out.img = ros_numpy.msgify(Image, img, encoding='bgr8')

	return res

p = rospy.Publisher(f'/{service_name}/cira_service', String, queue_size=10)
s = rospy.Service(f'/{service_name}/cira_service', CiraFlowService2, handle_service)

print("cira_rosservice ", service_name, " started")

rospy.spin()
