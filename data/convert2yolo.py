import os
import json
import shutil
import random


def create_folders():
    os.makedirs("seaDronesSee_yolo/images/train")
    os.makedirs("seaDronesSee_yolo/images/val")
    os.makedirs("seaDronesSee_yolo/images/test")
    os.makedirs("seaDronesSee_yolo/images/temp")

    os.makedirs("seaDronesSee_yolo/labels/train")
    os.makedirs("seaDronesSee_yolo/labels/val")
    os.makedirs("seaDronesSee_yolo/labels/test")
    os.makedirs("seaDronesSee_yolo/labels/temp")


def merge():
    # copy val
    shutil.copytree(
        "seaDronesSee/images/val",
        "seaDronesSee_yolo/images/temp",
        dirs_exist_ok=True,
    )

    # copy train
    shutil.copytree(
        "seaDronesSee/images/train",
        "seaDronesSee_yolo/images/temp",
        dirs_exist_ok=True,
    )

    # copy boxes coordinates
    for src in ["val", "train"]:
        src = f"seaDronesSee/annotations/instances_{src}.json"

        images = {}
        with open(src) as f:
            d = json.load(f)
            for item in d["images"]:
                images[item["file_name"]] = item

        boxes = {}
        with open(src) as f:
            d = json.load(f)
            for item in d["annotations"]:
                file_name = f"{item['image_id']}.jpg"
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
                    + f"{item['category_id']} {center_x:.6f} {center_y:.6f} {norm_w:.6f} {norm_h:.6f}\n"
                )

            # create files
            for box in boxes:
                txt = box.replace(".jpg", ".txt")
                with open(f"seaDronesSee_yolo/labels/temp/{txt}", "w") as f:
                    f.write(boxes[box].rstrip())


def clean_label_files():
    labels_dir = os.path.join("seaDronesSee_yolo", "labels", "temp")
    images_dir = os.path.join("seaDronesSee_yolo", "images", "temp")

    total_files_deleted = 0
    total_lines_removed = 0

    for filename in os.listdir(labels_dir):
        if not filename.endswith(".txt"):
            continue

        label_path = os.path.join(labels_dir, filename)
        image_filename = os.path.splitext(filename)[0] + ".jpg"
        image_path = os.path.join(images_dir, image_filename)

        with open(label_path, "r") as f:
            lines = f.readlines()

        # Filter for lines starting with class "1"
        human_lines = [line for line in lines if line.strip().startswith("1")]
        lines_removed = len(lines) - len(human_lines)

        if human_lines:
            # Change class "1" to class "0"
            updated_lines = ["0" + line[1:] for line in human_lines]
            with open(label_path, "w") as f:
                f.writelines(updated_lines)
            total_lines_removed += lines_removed
        else:
            # Delete label and image if no human lines remain
            os.remove(label_path)
            if os.path.exists(image_path):
                os.remove(image_path)
            total_files_deleted += 1
            total_lines_removed += len(lines)

    print(f"\nTotal label files deleted: {total_files_deleted}")
    print(f"Total lines removed: {total_lines_removed}")


def split():
    base_dir = "seaDronesSee_yolo"
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
    val_split = int(num_images * 0.9)  # 80% train, 10% val, 10% test

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


def remove_temp_folders():
    shutil.rmtree("seaDronesSee_yolo/images/temp")
    shutil.rmtree("seaDronesSee_yolo/labels/temp")


if __name__ == "__main__":
    create_folders()
    merge()
    clean_label_files()
    split()
    remove_temp_folders()


# Total label files deleted: 2293
# Total lines removed: 24088
