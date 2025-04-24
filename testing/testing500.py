import os
import torch
import torchvision
import torch.nn as nn
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights
from torchvision.models.feature_extraction import create_feature_extractor
import cv2
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, "../../ultralytics")
from ultralytics import YOLO
import ultralytics
print("Ultralytics YOLO loaded from:", ultralytics.__file__)


def main():
    data_file = "data.yaml"

    with open(data_file, "w") as f:
        f.write("""train: ../../seaDronesSee_yolo_testing/images/test
val: ../../seaDronesSee_yolo_testing/images/test
test: ../../seaDronesSee_yolo_testing/images/test
nc: 1
names: ["human"]""")

    name = "yolo11_shufflenet_1_0_ca"
    model = YOLO(f"../models500/pt/{name}.pt")
    model.export(format="ncnn", half=True)
    model = YOLO(f"../models500/pt/{name}_ncnn_model")

    metrics = model.val(
        data=data_file,
        split="test",
        batch=1,
        save=False,
    )


if __name__ == "__main__":
    main()
