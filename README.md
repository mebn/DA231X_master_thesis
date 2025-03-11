# DA231X_master_thesis

Master Thesis at KTH and Remote.aero.

## Venv

```sh
# Start
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# End
deactivate
```

## Server

```sh
cd server
python main.py
```

## Data

After downloading the [SeaDronesSee](https://www.kaggle.com/datasets/ubiratanfilho/sds-dataset) dataset.

```sh
cd data

# Convert to YOLO format
python converter.py
```
