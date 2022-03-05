# VerySimpleFaceRecognizeWithWeb

## Installation

```python
pip install -r requirement.txt
```

## Run the application
- All-in-one startup script
   - Windows > win_runboth.bat
   - Linux > linux_runboth.sh
Which can start both Face Recongnization and Web Lookup System

## Content
- web.py -> Using Flask as main framework
  - Routes
    - / (GET)
    - /operations (GET,POST)
    - /entryLogs (GET)
- cam.py -> Using OpenCV as main framework
  - Recongnzie Faces
  - Mark face section on opencv
  - Store captured image in directory (/imgs)
