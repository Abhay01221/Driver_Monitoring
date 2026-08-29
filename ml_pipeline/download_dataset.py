"""
Download UTA-RLDD (UTA Real-Life Drowsiness Dataset) using kagglehub
"""
import kagglehub
import shutil
from pathlib import Path
import config

def download_dataset():
    """
    Download the UTA-RLDD Dataset from Kaggle
    
    This dataset contains 3 classes:
    - Alert (label 0): Completely conscious
    - Low Vigilant (label 5): Some signs of sleepiness  
    - Drowsy (label 10): Actively trying not to fall asleep
    
    Returns:
        Path to dataset directory
    """
    print("\n" + "="*60)
    print("Downloading UTA-RLDD (Real-Life Drowsiness Dataset)")
    print("="*60 + "\n")
    
    # Download dataset using kagglehub
    print("📥 Downloading from Kaggle...")
    dataset_path = kagglehub.dataset_download("minhngt02/uta-rldd")
    
    print(f"✓ Dataset downloaded to: {dataset_path}")
    
    # Check what's in the downloaded path
    dataset_dir = Path(dataset_path)
    print(f"\n📁 Contents of {dataset_dir}:")
    for item in dataset_dir.iterdir():
        if item.is_dir():
            count = len(list(item.glob("*")))
            print(f"  📂 {item.name}/ ({count} files)")
        else:
            print(f"  📄 {item.name}")
    
    # Check if data needs to be copied to ml_pipeline/data/
    expected_structure = config.DATA_DIR
    
    print(f"\n🔄 Checking data directory: {expected_structure}")
    
    if not expected_structure.exists():
        print(f"Creating {expected_structure}...")
        expected_structure.mkdir(parents=True, exist_ok=True)
    
    # Check for Alert, Low Vigilant, and Drowsy folders
    alert_source = dataset_dir / "Alert"
    low_vigilant_source = dataset_dir / "Low_Vigilant"
    drowsy_source = dataset_dir / "Drowsy"
    
    # Also check alternative naming conventions
    if not alert_source.exists():
        # Try to find them in subdirectories or with different names
        alert_candidates = list(dataset_dir.rglob("*alert*")) + list(dataset_dir.rglob("*Alert*"))
        low_vigilant_candidates = list(dataset_dir.rglob("*low*vigilant*")) + list(dataset_dir.rglob("*Low*Vigilant*"))
        drowsy_candidates = list(dataset_dir.rglob("*drowsy*")) + list(dataset_dir.rglob("*Drowsy*"))
        
        if alert_candidates:
            alert_source = [d for d in alert_candidates if d.is_dir()][0]
        if low_vigilant_candidates:
            low_vigilant_source = [d for d in low_vigilant_candidates if d.is_dir()][0]
        if drowsy_candidates:
            drowsy_source = [d for d in drowsy_candidates if d.is_dir()][0]
            print(f"Found dataset in subdirectory: {drowsy_source.parent}")
    
    # Copy or create symlinks to ml_pipeline/data/
    alert_dest = config.ALERT_DIR
    low_vigilant_dest = config.LOW_VIGILANT_DIR
    drowsy_dest = config.DROWSY_DIR
    
    if alert_source.exists() and low_vigilant_source.exists() and drowsy_source.exists():
        print(f"\n📋 Dataset structure found:")
        print(f"  • Alert: {len(list(alert_source.glob('*')))} images")
        print(f"  • Low Vigilant: {len(list(low_vigilant_source.glob('*')))} images")
        print(f"  • Drowsy: {len(list(drowsy_source.glob('*')))} images")
        
        # Option 1: Create symbolic links (faster, no duplication)
        print(f"\n🔗 Creating symbolic links in {config.DATA_DIR}...")
        
        if alert_dest.exists():
            alert_dest.unlink() if alert_dest.is_symlink() else shutil.rmtree(alert_dest)
        if low_vigilant_dest.exists():
            low_vigilant_dest.unlink() if low_vigilant_dest.is_symlink() else shutil.rmtree(low_vigilant_dest)
        if drowsy_dest.exists():
            drowsy_dest.unlink() if drowsy_dest.is_symlink() else shutil.rmtree(drowsy_dest)
        
        try:
            alert_dest.symlink_to(alert_source.resolve(), target_is_directory=True)
            low_vigilant_dest.symlink_to(low_vigilant_source.resolve(), target_is_directory=True)
            drowsy_dest.symlink_to(drowsy_source.resolve(), target_is_directory=True)
            print("✓ Symbolic links created successfully")
        except OSError:
            # If symlinks fail (Windows without admin), copy instead
            print("⚠ Symbolic links failed, copying files instead...")
            print("  (This may take a few minutes)")
            
            if alert_dest.exists():
                shutil.rmtree(alert_dest)
            if low_vigilant_dest.exists():
                shutil.rmtree(low_vigilant_dest)
            if drowsy_dest.exists():
                shutil.rmtree(drowsy_dest)
            
            shutil.copytree(alert_source, alert_dest)
            shutil.copytree(low_vigilant_source, low_vigilant_dest)
            shutil.copytree(drowsy_source, drowsy_dest)
            print("✓ Files copied successfully")
    else:
        print(f"\n⚠ Warning: Expected folder structure not found")
        print(f"  Expected: Alert/, Low_Vigilant/, and Drowsy/ folders")
        print(f"  You may need to manually organize the dataset")
        print(f"\n  Dataset location: {dataset_path}")
        return dataset_path
    
    print(f"\n" + "="*60)
    print("✓ Dataset ready!")
    print("="*60)
    print(f"\nDataset location: {config.DATA_DIR}")
    print(f"  • {config.ALERT_DIR}")
    print(f"  • {config.LOW_VIGILANT_DIR}")
    print(f"  • {config.DROWSY_DIR}")
    print(f"\nYou can now run training:")
    print(f"  python train.py --model yolo --epochs 50")
    print()
    
    return dataset_path


if __name__ == "__main__":
    try:
        dataset_path = download_dataset()
    except Exception as e:
        print(f"\n❌ Error downloading dataset: {e}")
        print("\nTroubleshooting:")
        print("  1. Install kagglehub: pip install kagglehub")
        print("  2. Authenticate with Kaggle (first-time only):")
        print("     - Visit https://www.kaggle.com/settings/account")
        print("     - Click 'Create New API Token'")
        print("     - Follow the authentication prompts")
        print("  3. Try again: python download_dataset.py")
