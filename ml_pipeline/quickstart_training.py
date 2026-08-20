"""
Quick Start Script for Training
Automatically downloads dataset and starts training
"""
import sys
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("Driver Drowsiness Detection - Quick Start Training")
    print("="*70 + "\n")
    
    # Step 1: Check if dataset exists
    import config
    from data_prep import load_image_paths_and_labels
    
    print("Step 1: Checking for dataset...")
    image_paths, labels = load_image_paths_and_labels(config.DATA_DIR)
    
    if len(image_paths) == 0:
        print("\n📥 Dataset not found. Downloading from Kaggle...")
        print("(This is a one-time download, ~100MB)")
        
        try:
            from download_dataset import download_dataset
            dataset_path = download_dataset()
            
            # Try loading again
            print("\nRechecking dataset...")
            image_paths, labels = load_image_paths_and_labels(config.DATA_DIR)
            
            if len(image_paths) == 0:
                print(f"\n⚠ Dataset downloaded but not in expected format")
                print(f"Downloaded to: {dataset_path}")
                print(f"Expected at: {config.DATA_DIR}")
                print(f"\nPlease manually organize the dataset:")
                print(f"  1. Find 'Drowsy' and 'Non Drowsy' folders in {dataset_path}")
                print(f"  2. Copy or move them to {config.DATA_DIR}")
                print(f"  3. Run this script again")
                return
        except Exception as e:
            print(f"\n❌ Failed to download dataset: {e}")
            print("\nPlease download manually:")
            print("  1. Visit: https://www.kaggle.com/datasets/ismailnasri20/driver-drowsiness-dataset-ddd")
            print("  2. Download and extract to ml_pipeline/data/")
            print("  3. Run this script again")
            return
    
    print(f"\n✓ Dataset ready: {len(image_paths)} images")
    
    # Step 2: Training parameters
    print("\n" + "="*70)
    print("Step 2: Training Configuration (YOLO Model)")
    print("="*70)
    
    epochs_input = input("\nNumber of epochs [default: 50]: ").strip()
    epochs = int(epochs_input) if epochs_input else 50
    
    batch_input = input("Batch size [default: 32]: ").strip()
    batch_size = int(batch_input) if batch_input else 32
    
    img_input = input("Image size [default: 224]: ").strip()
    img_size = int(img_input) if img_input else 224
    
    # Step 3: Start training
    print("\n" + "="*70)
    print("Step 3: Starting Training")
    print("="*70)
    print(f"\nModel: YOLO (YOLOv8n-cls)")
    print(f"Epochs: {epochs}")
    print(f"Batch size: {batch_size}")
    print(f"Image size: {img_size}")
    print(f"Dataset: {len(image_paths)} images")
    
    confirm = input("\nStart training? (y/n) [default: y]: ").strip().lower() or "y"
    
    if confirm != "y":
        print("\nTraining cancelled.")
        return
    
    # Import and run training
    print("\n🚀 Starting training...\n")
    
    import subprocess
    cmd = [
        sys.executable, "train.py",
        "--model", "yolo",
        "--epochs", str(epochs),
        "--batch-size", str(batch_size),
        "--img-size", str(img_size)
    ]
    
    subprocess.run(cmd)
    
    # Step 4: Copy weights
    print("\n" + "="*70)
    print("Step 4: Deploying Model")
    print("="*70)
    
    # Check if training produced weights
    weights_file = config.MODELS_DIR / "yolo_best.pt"
    
    if weights_file.exists():
        print(f"\n✓ Training complete!")
        print(f"Model saved to: {weights_file}")
        
        # Copy to backend
        backend_weights = Path("../backend/weights/best.pt")
        import shutil
        shutil.copy2(weights_file, backend_weights)
        print(f"✓ Copied to backend: {backend_weights}")
        
        print("\n" + "="*70)
        print("✅ All Done!")
        print("="*70)
        print("\nYou can now start the backend:")
        print("  cd ../backend")
        print("  python -m uvicorn app.main:app --reload")
        print("\nAnd in another terminal, start the frontend:")
        print("  cd ../frontend")
        print("  npm run dev")
        print("\nThen open: http://localhost:3000")
    else:
        print(f"\n⚠ Model weights not found at: {weights_file}")
        print("Training may have failed. Check the logs above.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Training interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
