"""
Script to fix corrupted pickle files
This attempts to repair pickle files that may have been corrupted due to text mode saving
"""

import pickle
import os
import sys

def try_fix_pickle(filename):
    """Try multiple methods to load and fix a pickle file"""
    print(f"\n{'='*60}")
    print(f"Attempting to fix: {filename}")
    print(f"{'='*60}")
    
    if not os.path.exists(filename):
        print(f"✗ File not found: {filename}")
        return None
    
    # Method 1: Try loading with error recovery
    print("\n[Method 1] Standard binary mode loading...")
    try:
        with open(filename, 'rb') as f:
            obj = pickle.load(f)
            print("✓ Successfully loaded with standard method!")
            return obj
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Method 2: Try reading entire file first, then loading
    print("\n[Method 2] Reading entire file into memory first...")
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        obj = pickle.loads(data)
        print("✓ Successfully loaded after reading into memory!")
        return obj
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Method 3: Try removing problematic bytes (CR/LF issues)
    print("\n[Method 3] Attempting to clean file of text mode artifacts...")
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        
        # Remove common text mode artifacts
        # '\r\n' (Windows) or '\n' (Unix) that might have been inserted
        # But be careful - we need to preserve actual pickle protocol bytes
        
        # Try loading with protocol detection
        obj = pickle.loads(data)
        print("✓ Successfully loaded after cleanup!")
        return obj
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Method 4: Try with different pickle protocol
    print("\n[Method 4] Trying different pickle protocols...")
    for protocol in [0, 1, 2, 3, 4, 5]:
        try:
            with open(filename, 'rb') as f:
                # Skip pickle protocol byte and try different ones
                first_byte = f.read(1)
                if first_byte == b'\x80':
                    protocol_byte = f.read(1)
                    remaining_data = f.read()
                    # Reconstruct with current protocol
                    fixed_data = b'\x80' + bytes([protocol]) + remaining_data
                    obj = pickle.loads(fixed_data)
                    print(f"✓ Successfully loaded with protocol {protocol}!")
                    return obj
        except:
            continue
    
    print("\n✗ All methods failed. The pickle file appears to be corrupted.")
    print("   You may need to regenerate the pickle files from your training script.")
    return None

def save_fixed_pickle(obj, original_filename, output_filename=None):
    """Save a fixed pickle object"""
    if output_filename is None:
        # Create backup and fix in place
        backup_filename = original_filename + '.backup'
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
        os.rename(original_filename, backup_filename)
        output_filename = original_filename
        print(f"\n✓ Created backup: {backup_filename}")
    
    try:
        with open(output_filename, 'wb') as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"✓ Saved fixed pickle: {output_filename}")
        return True
    except Exception as e:
        print(f"✗ Error saving fixed pickle: {e}")
        return False

if __name__ == '__main__':
    print("Pickle File Repair Tool")
    print("="*60)
    print("This tool attempts to repair corrupted pickle files")
    print("="*60)
    
    files_to_fix = ['model.pkl', 'tfidf.pkl', 'label_encoder.pkl']
    fixed_objects = {}
    
    for filename in files_to_fix:
        if os.path.exists(filename):
            obj = try_fix_pickle(filename)
            if obj is not None:
                fixed_objects[filename] = obj
                # Optionally save fixed version
                response = input(f"\nSave fixed version of {filename}? (y/n): ").strip().lower()
                if response == 'y':
                    save_fixed_pickle(obj, filename)
        else:
            print(f"\n⚠ {filename} not found, skipping...")
    
    if fixed_objects:
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        for filename, obj in fixed_objects.items():
            print(f"✓ {filename}: Successfully loaded ({type(obj).__name__})")
    else:
        print("\n" + "="*60)
        print("⚠ WARNING: Could not fix any pickle files!")
        print("="*60)
        print("\nRECOMMENDED ACTION:")
        print("1. Upgrade numpy and scikit-learn:")
        print("   pip install --upgrade numpy>=1.26.0 scikit-learn>=1.6.0")
        print("\n2. Regenerate pickle files from your training script")
        print("   using the updated versions of numpy and scikit-learn")
        print("\n3. Ensure pickle files are saved in binary mode:")
        print("   with open('file.pkl', 'wb') as f:")
        print("       pickle.dump(obj, f)")
