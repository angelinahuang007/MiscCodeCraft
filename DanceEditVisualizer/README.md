# Dance Edit Preferences Visualizer

This project visualizes edit preferences for three dance videos (A005, A011, A019) showing which parts each person wants to exclude from the final edit.

## Files

- `tiffany.txt` - Tiffany's edit preferences
- `chuangege.txt` - Chuangege's edit preferences  
- `angelina.txt` - Angelina's edit preferences
- `visualize_edit_preferences.py` - Main visualization script
- `requirements.txt` - Python dependencies
- `setup.py` - Setup script for virtual environment

## Data Format

Each preference file contains lines in the format:
```
VIDEO_ID TIME_RANGE1 TIME_RANGE2 ...
```

Example:
```
A005 00:49-00:53 02:12-02:19 02:59-03:10
A011 00:54-00:58 01:14-01:20
```

Where:
- `VIDEO_ID` is one of: A005, A011, A019
- `TIME_RANGE` is in format MM:SS-MM:SS (start-end time)

## Setup Instructions

### Option 1: Automatic Setup (Recommended)
```bash
python setup.py
```

### Option 2: Manual Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Linux/macOS: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment (if not already activated)
2. Run the visualization script:
   ```bash
   python visualize_edit_preferences.py
   ```

The script will:
- Display a summary of all preferences in the terminal
- Create a visualization showing:
  - Each video on a separate row
  - Time axis from 0:00 to 3:30
  - Colored blocks for excluded time ranges
  - Different colors for each person's preferences
- Save the visualization as `edit_preferences_visualization.png`

## Visualization Features

- **Video Timeline**: Each video (A005, A011, A019) is shown on a separate row
- **Time Axis**: X-axis shows time from 0:00 to 3:30 with 30-second intervals
- **Color Coding**: Each person's excluded parts are shown in different colors:
  - Tiffany: Red (#FF6B6B)
  - Chuangege: Teal (#4ECDC4)
  - Angelina: Blue (#45B7D1)
- **Time Labels**: Each excluded block shows the exact time range
- **Legend**: Color legend identifies which person each color represents

## Requirements

- Python 3.7 or higher
- matplotlib
- numpy

## Output

The script generates:
1. Console output showing a summary of all preferences
2. A PNG file (`edit_preferences_visualization.png`) with the visualization
3. An interactive matplotlib window (if run in an environment that supports it) 