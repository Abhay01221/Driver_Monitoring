"""
Download Driver Drowsiness Dataset using kagglehub
"""
import kagglehub
import shutil
from pathlib import Path
import config

def download_dataset():
    """
    Download the Driver Drowsiness Dataset (DDD) from Kaggle
    
    Returns:
        Path to dataset directory
    """
    print("\n" + "="*60)
    print("Downloading Driver Drowsiness Dataset (DDD)")
    print("="*60 + "\n")
    
    # Download dataset using kagglehub
    print("📥 Downloading from Kaggle...")
    dataset_path = kagglehub.dataset_download("ismailnasri20/driver-drowsiness-dataset-ddd")
    
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
    
    # Check for Drowsy and Non Drowsy folders
    drowsy_source = dataset_dir / "Drowsy"
    non_drowsy_source = dataset_dir / "Non Drowsy"
    
    # Also check if they're in a subdirectory
    if not drowsy_source.exists():
        # Try to find them in subdirectories
        subdirs = [d for d in dataset_dir.rglob("Drowsy") if d.is_dir()]
        if subdirs:
            drowsy_source = subdirs[0]
            non_drowsy_source = drowsy_source.parent / "Non Drowsy"
            print(f"Found dataset in subdirectory: {drowsy_source.parent}")
    
    # Copy or create symlinks to ml_pipeline/data/
    drowsy_dest = config.DROWSY_DIR
    non_drowsy_dest = config.NON_DROWSY_DIR
    
    if drowsy_source.exists() and non_drowsy_source.exists():
        print(f"\n📋 Dataset structure found:")
        print(f"  • Drowsy: {len(list(drowsy_source.glob('*')))} images")
        print(f"  • Non Drowsy: {len(list(non_drowsy_source.glob('*')))} images")
        
        # Option 1: Create symbolic links (faster, no duplication)
        print(f"\n🔗 Creating symbolic links in {config.DATA_DIR}...")
        
        if drowsy_dest.exists():
            drowsy_dest.unlink() if drowsy_dest.is_symlink() else shutil.rmtree(drowsy_dest)
        if non_drowsy_dest.exists():
            non_drowsy_dest.unlink() if non_drowsy_dest.is_symlink() else shutil.rmtree(non_drowsy_dest)
        
        try:
            drowsy_dest.symlink_to(drowsy_source.resolve(), target_is_directory=True)
            non_drowsy_dest.symlink_to(non_drowsy_source.resolve(), target_is_directory=True)
            print("✓ Symbolic links created successfully")
        except OSError:
            # If symlinks fail (Windows without admin), copy instead
            print("⚠ Symbolic links failed, copying files instead...")
            print("  (This may take a few minutes)")
            
            if drowsy_dest.exists():
                shutil.rmtree(drowsy_dest)
            if non_drowsy_dest.exists():
                shutil.rmtree(non_drowsy_dest)
            
            shutil.copytree(drowsy_source, drowsy_dest)
            shutil.copytree(non_drowsy_source, non_drowsy_dest)
            print("✓ Files copied successfully")
    else:
        print(f"\n⚠ Warning: Expected folder structure not found")
        print(f"  Expected: Drowsy/ and Non Drowsy/ folders")
        print(f"  You may need to manually organize the dataset")
        print(f"\n  Dataset location: {dataset_path}")
        return dataset_path
    
    print(f"\n" + "="*60)
    print("✓ Dataset ready!")
    print("="*60)
    print(f"\nDataset location: {config.DATA_DIR}")
    print(f"  • {config.DROWSY_DIR}")
    print(f"  • {config.NON_DROWSY_DIR}")
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
