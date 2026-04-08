# """
# Data Audit Module.
# Verifies data integrity and provenance using metadata and SHA-256 hashing.
# """

import hashlib
import json
from pathlib import Path

def generate_file_hash(file_path):
    """
    Generates a unique SHA-256 signature for the file by reading it in chunks.
    """
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError as e:
        print(f"❌ ERROR: Fallo al leer el archivo para auditar: {e}")
        return None

def audit_data():
    """
    Finds the CSV in data/raw, generates its hash, and saves/verifies metadata.json.
    Returns True if audit passes, False otherwise.
    """
    try:
        raw_dir = Path("data/raw")
        csv_files = list(raw_dir.glob("*.csv"))
        
        if not csv_files:
            print("❌ ERROR: No .csv file found in data/raw/")
            return False

        target_file = csv_files[0]
        metadata_path = raw_dir / "metadata.json"
        
        print(f"🔍 Auditing file: {target_file.name}")
        calculated_hash = generate_file_hash(target_file)
        
        if not calculated_hash:
            return False

        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                saved_metadata = json.load(f)
                
            if saved_metadata.get("hash_sha256") == calculated_hash:
                print("✅ SUCCESS: Data integrity verified. File has not been altered.")
                return True
            else:
                print("🚨 CRITICAL ERROR: Hash mismatch. The dataset has been modified or corrupted.")
                return False
                
        else:
            new_metadata = {"file": target_file.name, "hash_sha256": calculated_hash}
            with open(metadata_path, "w") as f:
                json.dump(new_metadata, f, indent=4)
            print("📝 Initial metadata created successfully. Push this file to GitHub.")
            return True
            
    except json.JSONDecodeError:
        print("❌ ERROR: El archivo metadata.json está corrupto y no se puede leer.")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR during audit: {e}")
        return False
