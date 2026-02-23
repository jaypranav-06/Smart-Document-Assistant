#!/usr/bin/env python3
"""Clear the ChromaDB database to start fresh."""
import shutil
from pathlib import Path

def clear_database():
    """Remove the ChromaDB database directory."""
    chroma_path = Path("./chroma_db")
    uploads_path = Path("./uploads")

    if chroma_path.exists():
        print(f"Removing ChromaDB database at {chroma_path}")
        shutil.rmtree(chroma_path)
        print("✓ ChromaDB cleared")
    else:
        print("ChromaDB directory not found")

    if uploads_path.exists():
        print(f"\nRemoving uploaded files at {uploads_path}")
        shutil.rmtree(uploads_path)
        uploads_path.mkdir()
        print("✓ Uploads cleared")
    else:
        print("Uploads directory not found")

    print("\n✅ Database cleared successfully!")
    print("Restart the backend server to create a fresh database.")

if __name__ == "__main__":
    response = input("This will delete all documents and uploaded files. Continue? (yes/no): ")
    if response.lower() == "yes":
        clear_database()
    else:
        print("Cancelled")
