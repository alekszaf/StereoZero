# RPiStereo (StereoZero)

A Raspberry Pi-based stereo camera system for capturing synchronised left/right image sequences, timelapses, and video, plus a Python/OpenCV pipeline for calibrating the camera pair and generating disparity maps and 3D point clouds. Includes 3D-printable enclosures and rig mounts.

## Repository structure

```
RPiStereo/
├── StereoLapse-master.py   # Timelapse capture triggered by a GPIO timer signal, toggled by a button
├── StereoVid-master.py     # Video recording, toggled by a button, fixed clip length via CLI arg
├── CaptureOnPress.py       # Single-shot capture on button press, used for calibration image sets
├── awb_calibration.py      # Sweeps AWB blue gain to help tune white balance
├── CITATION.cff            # Citation metadata for this software
├── ImageProcessing/
│   ├── stereo_calibration.py  # Chessboard-based single + stereo camera calibration, saves stereoMap.xml
│   ├── stereo_match.py        # Rectifies an image pair and computes a disparity map (StereoBM)
│   ├── stereoMatch_GUI.py     # Interactive trackbar GUI for tuning StereoSGBM/StereoBM parameters
│   ├── point_cloud.py         # Rectifies an image pair, computes disparity, exports a coloured .ply point cloud
│   └── edgeDetection.py       # Sobel / Canny edge detection on a captured image
├── Utils/
│   ├── fileRename.py       # Batch-renames captured images with distance/mode metadata
│   ├── image_cutter.py     # Batch-crops a folder of images to a fixed size
│   ├── newFolders.py       # Creates a sequence of distance-labelled folders
│   ├── sort2Folders.py     # Creates distance folders and sorts files into them by resolution mode
│   └── wait_for_edge.py    # Minimal GPIO rising-edge trigger test used to debug the timer signal
└── CAD/
    ├── Enclosures-STL/         # Pi Zero W + camera enclosure and timer enclosure STL files
    └── StereoCameraRig-STL/    # Stereo camera baseholder STL files (30 mm / 60 mm baseline)
```

## Hardware

- Raspberry Pi (Zero W or similar) with a `picamera`-compatible camera module
- Push button and an external timer signal wired to GPIO for triggering capture (see `channel`/`button` pin numbers in the capture scripts)
- 3D-printed enclosure and stereo rig (STL files in `CAD/`)

## Software requirements

Capture scripts (run on the Raspberry Pi):
- Python 3
- `picamera`
- `RPi.GPIO` and/or `gpiozero`

Image processing scripts (run on a workstation with the captured images):
- Python 3
- `opencv-python`
- `numpy`
- `Pillow`
- `matplotlib`

Note: several scripts (`stereo_calibration.py`, `stereo_match.py`, `point_cloud.py`, `stereoMatch_GUI.py`, `edgeDetection.py`, and the scripts in `Utils/`) currently reference hardcoded local file paths. Update the `imagesLeft`/`imagesRight`/`path`/`parent_dir` variables at the top of each script to point at your own image locations before running.

## Usage

### 1. Capture

Run on the Raspberry Pi:
- `StereoLapse-master.py` — press the button to arm the timelapse, then each rising edge on the timer GPIO captures a still frame to `/home/pi/Timelapse/`.
- `StereoVid-master.py -t <seconds>` — press the button to start/stop recording a video clip of the given length.
- `CaptureOnPress.py` — captures a still at two resolutions each time the button is pressed; used to build calibration image sets.
- `awb_calibration.py` — captures a sequence of stills sweeping the AWB blue gain, to help pick white balance values for the scripts above.

### 2. Calibrate

1. Capture chessboard images with both cameras (e.g. via `CaptureOnPress.py`).
2. Update the image paths and `chessboardSize`/`frameSize` in `ImageProcessing/stereo_calibration.py` to match your setup.
3. Run it to perform single-camera and stereo calibration and stereo rectification; the resulting undistortion/rectification maps are written to `stereoMap.xml`.

### 3. Process stereo pairs

- `ImageProcessing/stereo_match.py` — loads a left/right pair, computes a disparity map with `StereoBM`, and displays it.
- `ImageProcessing/stereoMatch_GUI.py` — same idea, but with trackbars for interactively tuning disparity parameters.
- `ImageProcessing/point_cloud.py` — rectifies a pair using `stereoMap.xml`, computes disparity, and exports a coloured point cloud to `pointCloud.ply`.
- `ImageProcessing/edgeDetection.py` — Sobel and Canny edge detection on a single image.

### 4. Organise captures

The scripts in `Utils/` help manage large batches of captured images: renaming with distance/mode metadata (`fileRename.py`), cropping (`image_cutter.py`), and creating/sorting distance-labelled folders (`newFolders.py`, `sort2Folders.py`).

## CAD

STL files for 3D printing the Pi Zero W camera enclosure, timer enclosure, and stereo camera rig baseholders (30 mm and 60 mm baselines) are in `CAD/`.

## Citation

If you use this software, please cite it — see [`CITATION.cff`](CITATION.cff).
