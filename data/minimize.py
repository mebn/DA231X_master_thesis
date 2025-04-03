import os
import random

# Define base directory
base_dir = "seaDronesSee_yolo"

# How much to keep (between 0 and 1)
keep = 0.31

# Define dataset splits
splits = ["train", "val", "test"]

# Reduce images in each split
for split in splits:
    img_dir = os.path.join(base_dir, f"images/{split}")
    label_dir = os.path.join(base_dir, f"labels/{split}")

    images = sorted([f for f in os.listdir(img_dir) if f.endswith(".jpg")])

    num_to_keep = max(1, int(len(images) * keep))
    images_to_keep = set(random.sample(images, num_to_keep))

    for img in images:
        if img not in images_to_keep:
            os.remove(os.path.join(img_dir, img))
            label_path = os.path.join(label_dir, img.replace(".jpg", ".txt"))
            if os.path.exists(label_path):
                os.remove(label_path)

    print(f"Reduced {split} set to {num_to_keep} images and labels.")


# keep = 0.15
# Reduced train set to 982 images and labels.
# Reduced val set to 122 images and labels.
# Reduced test set to 122 images and labels.

# keep = 0.31
# Reduced train set to 2029 images and labels.
# Reduced val set to 253 images and labels.
# Reduced test set to 253 images and labels.

# keep = 0.35
# Reduced train set to 2291 images and labels.
# Reduced val set to 286 images and labels.
# Reduced test set to 286 images and labels.

# keep = 0.40
# Reduced train set to 2618 images and labels.
# Reduced val set to 327 images and labels.
# Reduced test set to 327 images and labels.
