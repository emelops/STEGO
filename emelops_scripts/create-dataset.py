from datetime import datetime
from glob import glob
from hashlib import sha256
from os import link, makedirs
from pathlib import Path
from random import Random
from shutil import rmtree

dataset_name = 'true_color'
dataset_size = 30000
train_percent = 50
val_percent = 25
test_percent = 25

date_seed = datetime(2022, 12, 18, 18)
rng = Random(date_seed.timestamp())

dataset_path_pattern = Path(f'/datadrive/{dataset_name}/imgs/*.png')
dataset_files = sorted(glob(str(dataset_path_pattern)))
rng.shuffle(dataset_files)

subset_path = Path(date_seed.strftime(f'/datadrive/{dataset_name}-{dataset_size}-{train_percent}-{val_percent}-{test_percent}-%Y-%m-%d-%H/imgs'))
train_path = subset_path / 'train'
val_path = subset_path / 'val'
test_path = subset_path / 'test'

if subset_path.exists():
    rmtree(str(subset_path))

makedirs(str(train_path))
makedirs(str(val_path))
makedirs(str(test_path))

train_start = 0
train_end = int(train_percent / 100 * dataset_size)

val_start = train_end
val_end = int(val_percent / 100 * dataset_size + val_start)

test_start = val_end 
test_end = int(test_percent / 100 * dataset_size + test_start)

train_files = dataset_files[train_start:train_end]
val_files = dataset_files[val_start:val_end]
test_files = dataset_files[test_start:test_end]

for train_file in train_files:
    train_hash = sha256(Path(train_file).stem.encode('utf-8')).hexdigest()
    train_file_name = f'{train_hash}-{Path(train_file).name}'
    train_link_path = train_path / train_file_name
    link(train_file, train_link_path)

for val_file in val_files:
    val_hash = sha256(Path(val_file).stem.encode('utf-8')).hexdigest()
    val_file_name = f'{val_hash}-{Path(val_file).name}'
    val_link_path = val_path / val_file_name
    link(val_file, val_link_path)

for test_file in test_files:
    test_hash = sha256(Path(test_file).stem.encode('utf-8')).hexdigest()
    test_file_name = f'{test_hash}-{Path(test_file).name}'
    test_link_path = test_path / test_file_name
    link(test_file, test_link_path)


