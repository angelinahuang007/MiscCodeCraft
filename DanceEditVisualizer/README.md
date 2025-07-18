# Dance Edit Preferences Visualizer

A Python tool that visualizes edit preferences for dance videos, showing which parts participants want to include (green) or exclude (red) from the final edit.

## Features

- **Dual Preference Support**: Each participant can specify both wanted (`*_want.txt`) and unwanted (`*_nowant.txt`) parts
- **Unique Color Coding**: Each participant gets distinct shades of green for wanted parts and red for unwanted parts
- **Automatic File Detection**: Automatically detects all preference files in the `input/` folder
- **Numbered Outputs**: Generates numbered output files to prevent overwriting previous visualizations
- **Clean Layout**: Legend positioned at bottom to avoid covering visualization content

## File Structure

```
├── input/                    # Preference files folder
│   ├── person1_want.txt     # Person 1's wanted parts
│   ├── person1_nowant.txt   # Person 1's unwanted parts
│   ├── person2_want.txt     # Person 2's wanted parts
│   └── person2_nowant.txt   # Person 2's unwanted parts
├── output/                   # Generated visualizations
├── visualize_edit_preferences.py
└── requirements.txt
```

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

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place preference files in the `input/` folder using the naming convention:
   - `personname_want.txt` for wanted parts
   - `personname_nowant.txt` for unwanted parts

2. Run the visualization:
   ```bash
   python visualize_edit_preferences.py
   ```

3. Check the `output/` folder for generated visualizations (numbered files like `edit_preferences_visualization_01.png`)

## Visualization Features

- **Video Timeline**: Each video (A005, A011, A019) shown on separate rows
- **Time Axis**: X-axis shows time from 0:00 to 3:30 with 30-second intervals
- **Color Coding**: 
  - Green shades = wanted parts (unique per participant)
  - Red shades = unwanted parts (unique per participant)
- **Time Labels**: Each block shows exact time range
- **Bottom Legend**: Clear identification of which color belongs to which participant and preference type

## Requirements

- Python 3.7+
- matplotlib
- numpy 