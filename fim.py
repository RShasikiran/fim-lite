import argparse
import hashlib
import json
import os
from pathlib import Path


def get_hash(filepath):
  """Turns a file into a unique SHA-256 code."""
  sha256 = hashlib.sha256()
  with open(filepath, "rb") as f:
    while chunk := f.read(65536):
      sha256.update(chunk)
  return sha256.hexdigest()


def create_baseline(folder, baseline_file):
  """Takes a snapshot of all files and saves to JSON."""
  data = {}
  for root, _, files in os.walk(folder):
    for file in files:
      path = Path(root) / file
      if path.name == baseline_file:
        continue
      data[str(path.relative_to(folder))] = get_hash(path)

  with open(baseline_file, "w") as f:
    json.dump(data, f, indent=4)
  print(f"[+] Baseline saved with {len(data)} files!")


def verify(folder, baseline_file):
  """Compares current files against the saved baseline."""
  with open(baseline_file, "r") as f:
    old_data = json.load(f)

  current_data = {}
  for root, _, files in os.walk(folder):
    for file in files:
      path = Path(root) / file
      if path.name == baseline_file:
        continue
      current_data[str(path.relative_to(folder))] = get_hash(path)

  # Check for changes
  print("\n--- SECURITY CHECK REPORT ---")
  for path, old_hash in old_data.items():
    if path not in current_data:
      print(f"[-] DELETED: {path}")
    elif current_data[path] != old_hash:
      print(f"[!] MODIFIED: {path}")

  for path in current_data:
    if path not in old_data:
      print(f"[+] ADDED: {path}")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--dir", required=True, help="Folder to watch")
  parser.add_argument("--init", action="store_true", help="Create baseline")
  args = parser.parse_args()

  if args.init:
    create_baseline(args.dir, "baseline.json")
  else:
    verify(args.dir, "baseline.json")