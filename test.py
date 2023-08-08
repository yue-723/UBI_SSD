import os
from datetime import datetime, timedelta
# from click import UsageError

from vision.ssd.vgg_ssd import create_vgg_ssd, create_vgg_ssd_predictor
from vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
from vision.ssd.mobilenetv1_ssd_lite import create_mobilenetv1_ssd_lite, create_mobilenetv1_ssd_lite_predictor
from vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor
from vision.utils.misc import Timer
import matplotlib.pyplot as plt
import cv2
import sys
import numpy as np
import pathlib
import torch

if __name__ == "__main__":
	
	# if len(sys.argv) != 4:
	# 	raise UsageError("Usage: python ssd_test_img.py <img_name> <model_path> <net_type>")

	img_path, model_path, net_type = sys.argv[1], sys.argv[2], sys.argv[3]
	timer = Timer()
	label_path = "models/ubi-model-labels.txt"

	img_name = img_path.split("/")[-1]

	# --------------- #
 
	class_names = [name.strip() for name in open(label_path).readlines()]
	if net_type == 'vgg16-ssd':
		net = create_vgg_ssd(len(class_names), is_test=True)
	elif net_type == 'mb1-ssd':
		net = create_mobilenetv1_ssd(len(class_names), is_test=True)
	elif net_type == 'mb1-ssd-lite':
		net = create_mobilenetv1_ssd_lite(len(class_names), is_test=True)
	elif net_type == 'mb2-ssd-lite':
		net = create_mobilenetv2_ssd_lite(len(class_names), is_test=True, device='cpu')
	else:
		print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
		sys.exit(1)
		
	net.load(model_path)

	if net_type == 'vgg16-ssd':
		predictor = create_vgg_ssd_predictor(net, candidate_size=200)
	elif net_type == 'mb1-ssd':
		predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)
	elif net_type == 'mb1-ssd-lite':
		predictor = create_mobilenetv1_ssd_lite_predictor(net, candidate_size=200)
	elif net_type == 'mb2-ssd-lite':
		predictor = create_mobilenetv2_ssd_lite_predictor(net, candidate_size=200)
	else:
		print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
		sys.exit(1)

	print("Loading Trained Model is Done!\n")
	print("Starting Detection...\n")


	orig_image = cv2.imread(img_path)
	image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
	color = np.random.uniform(0, 255, size = (10, 3))

	timer.start()
	boxes, labels, probs = predictor.predict(image, 20, 0.4)
	interval = timer.end()
	print('Time: {:.2f}s, Detect Objects: {:d}.'.format(interval, labels.size(0)))

	fps = 1/interval

	for i in range(boxes.size(0)):
		box = boxes[i, :]
		label = f"{class_names[labels[i]]}: {probs[i]:.2f}"

		i_color = int(labels[i])
		box = [round(b.item()) for b in box]

		cv2.rectangle(orig_image, (box[0], box[1]), (box[2], box[3]), color[i_color], 2)

		cv2.putText(orig_image, label,
					(box[0] - 10, box[1] - 10),
					cv2.FONT_HERSHEY_SIMPLEX,
					1,  # font scale
					color[i_color],
					2)  # line type

	print(orig_image.shape)
	dt = datetime.now() + timedelta(hours=8)
	save_path = f'./outputs/img/{dt.date()}'
	pathlib.Path(save_path).mkdir(parents=True, exist_ok=True) 
	cv2.imwrite(f'{save_path}/{img_name}', orig_image)
	print("Check the result!")
