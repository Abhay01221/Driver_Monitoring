# UTA-RLDD Dataset Information

## Dataset Successfully Configured! ✓

The **UTA-RLDD (UTA Real-Life Drowsiness Dataset)** from Kaggle has been successfully downloaded and integrated into the project.

### Dataset Details

- **Source**: https://www.kaggle.com/datasets/minhngt02/uta-rldd
- **Size**: 2.77 GB
- **Total Images**: 9,054 images
- **Classes**: 2 (Binary Classification)
  - **Active** (Alert): 5,862 images
  - **Fatigue** (Drowsy): 3,192 images

### Dataset Location

The dataset is cached at:
```
C:\Users\abhay\.cache\kagglehub\datasets\minhngt02\uta-rldd\versions\2
```

The config.py automatically detects and uses this location.

### Dataset Structure

```
uta-rldd/
├── train/
│   ├── active/     # Alert/awake drivers
│   └── fatigue/    # Drowsy/fatigued drivers
├── val/
│   ├── active/
│   └── fatigue/
└── test/
    ├── active/
    └── fatigue/
```

### Data Split (Auto-generated for training)

- **Train**: 6,337 images (70%)
- **Val**: 1,358 images (15%)
- **Test**: 1,359 images (15%)

### Class Balance

The dataset is imbalanced:
- Alert: ~65% of images
- Drowsy: ~35% of images

**Class weights** are automatically computed to handle this imbalance during training:
- Alert class weight: 0.77
- Drowsy class weight: 1.42

### About the Original UTA-RLDD

The original UTA-RLDD dataset contains:
- 30 hours of RGB videos
- 60 healthy participants
- 3 drowsiness states: **alert**, **low vigilance**, and **drowsy**
- Real-life conditions with various backgrounds and angles
- Multiple ethnicities, ages, and genders

The Kaggle version used here is a preprocessed binary classification version (active vs fatigue) with extracted frames from the videos.

### Using the Dataset

The dataset is already configured and ready to use:

#### 1. Verify Dataset
```bash
cd ml_pipeline
python data_prep.py
```

#### 2. Train a Model
```bash
# Train with YOLOv8
python train.py --model yolo --epochs 50

# Or use the quickstart script
python quickstart_training.py
```

#### 3. Evaluate Model
```bash
python evaluate.py --model-path models/best_model.pt
```

### Citation

If you use this dataset, please cite:

```bibtex
@inproceedings{ghoddoosian2019realistic,
  title={A Realistic Dataset and Baseline Temporal Model for Early Drowsiness Detection},
  author={Ghoddoosian, Reza and Galib, Marnim and Athitsos, Vassilis},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshops},
  year={2019}
}
```

### Next Steps

1. ✅ Dataset downloaded and configured
2. ⏳ Train your model: `cd ml_pipeline && python train.py --model yolo --epochs 50`
3. ⏳ Test with the web interface once training is complete

### Notes

- The old Drowsy/Non Drowsy dataset has been replaced
- Config automatically detects the Kaggle cache location
- Class names are mapped: `active` → `Alert`, `fatigue` → `Drowsy`
- The system supports both the frontend and backend with this new dataset
