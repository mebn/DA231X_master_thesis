# DA231X_master_thesis

Master Thesis at KTH and Remote.aero.

## How to run

### Venv

First activate a python virtual environment at the root of the repo:

```sh
# Start
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# End
deactivate
```
### Data

Download the SeaDronesSee dataset [here](https://www.kaggle.com/datasets/ubiratanfilho/sds-dataset) and place it in the `data/` directory. Then convert to YOLO format and reduce the number of elements in the dataset:

```sh
cd data

# Convert to YOLO format
python convert2yolo.py

# Reduce number of elements
python minimize.py
```

### Testing

Run the testing script to evaluate the performace of the various models:

```sh
# Testing models trained on dataset with 2000 images in train set
python testing2000.py

# Testing models trained on dataset with 500 images in train set
python testing500.py
```
