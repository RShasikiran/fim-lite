# FIM-Lite (File Integrity Monitor)

A lightweight, production-ready File Integrity Monitoring (FIM) utility built in Python. Designed for host-based security monitoring, it establishes a cryptographic baseline of critical files and detects unauthorized additions, deletions, or modifications in real-time.

---

## 🚀 Overview
Host-based Intrusion Detection Systems (HIDS) rely on monitoring critical files for tampering or unauthorized changes. **FIM-Lite** automates this by taking a cryptographic snapshot (baseline) of a target directory and comparing future scans against it to flag any alterations.

---

## 🛠️ How It Works

FIM-Lite operates in two distinct phases:

1. **Baseline Generation (`--init`):**
   - Recursively walks through the target directory using `os.walk`.
   - Reads files in 64KB chunks to optimize memory usage.
   - Calculates a unique **SHA-256 cryptographic hash** for each file.
   - Saves relative paths and their corresponding checksums into a structured `baseline.json` file.

2. **Integrity Verification (Default Scan):**
   - Re-scans the directory and generates fresh hashes for current files.
   - Compares the current state against the saved `baseline.json`.
   - Accurately categorizes file differences into three distinct states:
     - **Modified:** The file exists, but its hash has changed (contents altered).
     - **Added:** A new file appeared that wasn't in the original baseline.
     - **Deleted:** A file from the baseline is missing during the current scan.

---

## ✨ Features
- **Cryptographic Security:** Utilizes SHA-256 hashing to detect even a single-byte change in file contents.
- **Memory Efficient:** Reads large files in blocks rather than loading them entirely into RAM.
- **Robust Exception Handling:** Gracefully handles permission errors on locked files without crashing the script.
- **Self-Excluding Logic:** Automatically ignores the baseline JSON file during hashing to prevent false positives.
- **CLI Interface:** Configurable via command-line arguments using `argparse`.

---

## 💻 Tech Stack
- **Language:** Python 3
- **Standard Libraries:** `hashlib`, `json`, `os`, `argparse`, `pathlib`

---

## 📦 Usage

### 1. Initialize the Baseline
Scan your target directory and generate the initial cryptographic snapshot:
```bash
python fim.py -d ./target_folder --init
```
###2. Run an Integrity Check
Compare the current state of the directory against your saved baseline:

```Bash
python fim.py -d ./target_folder
```
##⚙️ Command-Line Arguments

-d, --dir: Path to the directory you want to monitor (Required).

--init: Flag to create or overwrite the baseline snapshot.
