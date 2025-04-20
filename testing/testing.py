import os
import torch
import torchvision
import torch.nn as nn
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights
from torchvision.models.feature_extraction import create_feature_extractor
import cv2
import matplotlib.pyplot as plt

import sys
sys.path.append("../../ultralytics")
from ultralytics import YOLO


data_file = "data.yaml"

with open(data_file, "w") as f:
    f.write("""train: ../../seaDronesSee_yolo_testing/images/test
val: ../../seaDronesSee_yolo_testing/images/test
test: ../../seaDronesSee_yolo_testing/images/test
nc: 1
names: ["human"]""")

model = YOLO("../models500/pt/yolo11_baseline.pt")

for i in range(1):
    metrics = model.val(
        data=data_file,
        split="test",
        batch=1,
        save=False,
    )

    print("Round:", i)
    print(metrics)
