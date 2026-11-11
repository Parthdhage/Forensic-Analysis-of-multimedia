# Multimedia Forensic Analyzer

A Streamlit interface for reviewing uploaded audio and video files. The current analyzer extracts container and stream metadata, computes file hashes, checks file structure with ffprobe, and can show a video frame preview.

## Requirements

- Python
- FFmpeg, including ffprobe, available on your system PATH
- Python packages: Streamlit, Pillow, and ffmpeg-python

This repository does not currently include a dependency manifest.

## Run locally

Install the Python packages:

    python -m pip install streamlit Pillow ffmpeg-python

Start the Streamlit application:

    streamlit run src/forensic_media_analyzer.py

Streamlit prints a local URL to open in your browser.

## Repository layout

    src/forensic_media_analyzer.py    Streamlit application

## Scope

The application is kept under src/ with its runtime dependencies listed in requirements.txt. Keep original media files and any case evidence in a controlled local workspace; this project is a file-analysis interface, not a case-management or evidence-preservation system.
