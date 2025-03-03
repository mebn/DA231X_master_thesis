import os
import json
import shutil
import random


def create_folders():
    os.makedirs("../seaDronesSee_yolo/images/train")
    os.makedirs("../seaDronesSee_yolo/images/val")
    os.makedirs("../seaDronesSee_yolo/images/test")

    os.makedirs("../seaDronesSee_yolo/labels/train")
    os.makedirs("../seaDronesSee_yolo/labels/val")
    os.makedirs("../seaDronesSee_yolo/labels/test")


def create_data_yaml():
    with open("../seaDronesSee_yolo/data.yaml", "w") as f:
        f.write(
            """train: images/train
val: images/train/val
test: images/train/test
nc: 6
names: ["ignored", "swimmer", "boat", "jetski", "life_saving_appliances", "buoy"]"""
        )


def merge():
    # copy images
    os.makedirs("../seaDronesSee_yolo/images/temp")

    # copy val
    shutil.copytree(
        "../seaDronesSee/images/val",
        "../seaDronesSee_yolo/images/temp",
        dirs_exist_ok=True,
    )

    # copy train
    shutil.copytree(
        "../seaDronesSee/images/train",
        "../seaDronesSee_yolo/images/temp",
        dirs_exist_ok=True,
    )

    # copy boxes coordinates
    dst = "../seaDronesSee_yolo/labels/temp"
    os.makedirs(dst)
    for src in ["val", "train"]:
        src = f"../seaDronesSee/annotations/instances_{src}.json"

        images = {}
        with open(src) as f:
            d = json.load(f)
            for item in d["images"]:
                images[item["file_name"]] = item

        boxes = {}
        with open(src) as f:
            d = json.load(f)
            for item in d["annotations"]:
                file_name = f"{item["image_id"]}.jpg"
                x, y, w, h = item["bbox"]
                image_width = images[file_name]["width"]
                image_height = images[file_name]["height"]

                # Convert to YOLO format
                center_x = (x + w / 2) / image_width
                center_y = (y + h / 2) / image_height
                norm_w = w / image_width
                norm_h = h / image_height

                boxes[file_name] = (
                    boxes.get(file_name, "")
                    + f"{item["category_id"]} {center_x:.6f} {center_y:.6f} {norm_w:.6f} {norm_h:.6f}\n"
                )

            # create files
            for box in boxes:
                txt = box.replace(".jpg", ".txt")
                with open(f"../seaDronesSee_yolo/labels/temp/{txt}", "w") as f:
                    f.write(boxes[box].rstrip())


def split():
    base_dir = "../seaDronesSee_yolo"
    temp_images = os.path.join(base_dir, "images/temp")
    temp_labels = os.path.join(base_dir, "labels/temp")

    # Target directories
    split_dirs = {
        "train": {
            "images": os.path.join(base_dir, "images/train"),
            "labels": os.path.join(base_dir, "labels/train"),
        },
        "val": {
            "images": os.path.join(base_dir, "images/val"),
            "labels": os.path.join(base_dir, "labels/val"),
        },
        "test": {
            "images": os.path.join(base_dir, "images/test"),
            "labels": os.path.join(base_dir, "labels/test"),
        },
    }

    # List all images (assuming all images are .jpg)
    image_files = sorted([f for f in os.listdir(temp_images) if f.endswith(".jpg")])
    random.shuffle(image_files)  # Shuffle for randomness

    # Compute split sizes
    num_images = len(image_files)
    train_split = int(num_images * 0.8)
    val_split = int(num_images * 0.9)  # 80% train, 10% val, rest test

    # Split into train, val, test
    splits = {
        "train": image_files[:train_split],
        "val": image_files[train_split:val_split],
        "test": image_files[val_split:],
    }

    # Move files
    for split, files in splits.items():
        for img_file in files:
            img_path = os.path.join(temp_images, img_file)
            label_file = img_file.replace(".jpg", ".txt")
            label_path = os.path.join(temp_labels, label_file)

            # Move image and label
            shutil.move(img_path, split_dirs[split]["images"])
            shutil.move(label_path, split_dirs[split]["labels"])


def remove_folders():
    shutil.rmtree("../seaDronesSee_yolo/images/temp")
    shutil.rmtree("../seaDronesSee_yolo/labels/temp")


if __name__ == "__main__":
    create_folders()
    create_data_yaml()
    merge()
    split()
    remove_folders()
