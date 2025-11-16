"""
Diagnostic script to test pickle file loading
Run this to identify issues with model.pkl and tfidf.pkl files
"""

import pickle
import os
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def test_pickle_file(filename):
    """Test if a pickle file can be loaded"""
    print(f"\n{'='*50}")
    print(f"Testing {filename}")
    print(f"{'='*50}")
    
    if not os.path.exists(filename):
        print(f"X File not found: {filename}")
        return False
    
    # Check file size
    file_size = os.path.getsize(filename)
    print(f"File size: {file_size} bytes")
    
    if file_size == 0:
        print(f"X File is empty!")
        return False
    
    # Try to read first few bytes
    try:
        with open(filename, 'rb') as f:
            first_bytes = f.read(20)
            print(f"First 20 bytes (hex): {first_bytes.hex()}")
            print(f"First 20 bytes (repr): {repr(first_bytes)}")
    except Exception as e:
        print(f"X Error reading file: {e}")
        return False
    
    # Try to load pickle
    try:
        with open(filename, 'rb') as f:
            obj = pickle.load(f)
            print(f"✓ Successfully loaded pickle file")
            print(f"Type: {type(obj)}")
            
            # Print some info about the loaded object
            if hasattr(obj, '__class__'):
                print(f"Class: {obj.__class__.__name__}")
            
            # For model, check if it has classes_ attribute
            if hasattr(obj, 'classes_'):
                print(f"Number of classes: {len(obj.classes_)}")
                print(f"First 5 classes: {list(obj.classes_[:5])}")
            
            # For tfidf, check vocabulary
            if hasattr(obj, 'vocabulary_'):
                vocab_size = len(obj.vocabulary_)
                print(f"Vocabulary size: {vocab_size}")
                if vocab_size > 0:
                    sample_words = list(obj.vocabulary_.keys())[:5]
                    print(f"Sample vocabulary words: {sample_words}")
            
            return True
            
    except Exception as e:
        print(f"X Error loading pickle: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("Pickle File Diagnostic Tool")
    print("="*50)
    
    test_pickle_file('model.pkl')
    test_pickle_file('tfidf.pkl')
    
    if os.path.exists('label_encoder.pkl'):
        test_pickle_file('label_encoder.pkl')
    
    print("\n" + "="*50)
    print("Diagnostic complete")
    print("="*50)
