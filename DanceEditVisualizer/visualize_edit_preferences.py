#!/usr/bin/env python3
"""
Dance Edit Preferences Visualizer

This script visualizes the edit preferences for three dance videos (A005, A011, A019)
showing which parts each person wants to exclude from the final edit.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for WSL compatibility
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime, timedelta
import os
import glob

def parse_time_range(time_str):
    """Parse time range string like '00:49-00:53' into start and end seconds."""
    start_str, end_str = time_str.split('-')
    
    def time_to_seconds(time_str):
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    
    return time_to_seconds(start_str), time_to_seconds(end_str)

def parse_preference_file(filename):
    """Parse a preference file and return a dictionary of video preferences."""
    preferences = {}
    
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found")
        return preferences
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 2:
                continue
            
            video_id = parts[0]
            time_ranges = parts[1:]
            
            if video_id not in preferences:
                preferences[video_id] = []
            
            for time_range in time_ranges:
                try:
                    start_sec, end_sec = parse_time_range(time_range)
                    preferences[video_id].append((start_sec, end_sec))
                except ValueError as e:
                    print(f"Warning: Could not parse time range '{time_range}' in {filename}: {e}")
    
    return preferences

def get_next_output_number(output_dir):
    """Get the next available output number for the output file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        return 1
    
    existing_files = glob.glob(os.path.join(output_dir, 'edit_preferences_visualization_*.png'))
    if not existing_files:
        return 1
    
    # Extract numbers from existing files
    numbers = []
    for file in existing_files:
        try:
            # Extract number from filename like "edit_preferences_visualization_01.png"
            filename = os.path.basename(file)
            number_str = filename.split('_')[-1].replace('.png', '')
            numbers.append(int(number_str))
        except (ValueError, IndexError):
            continue
    
    return max(numbers) + 1 if numbers else 1

def get_preference_files(input_dir):
    """Get all preference files from the input directory."""
    if not os.path.exists(input_dir):
        print(f"Warning: Input directory '{input_dir}' not found")
        return []
    
    # Get all .txt files in the input directory
    txt_files = glob.glob(os.path.join(input_dir, '*.txt'))
    
    # Define colors for different people (cycling if more than available colors)
    colors = ['#4062BB', '#59C3C3', '#95F2D9', '#1CFEBA', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    preference_files = []
    for i, file_path in enumerate(sorted(txt_files)):
        filename = os.path.basename(file_path)
        person_name = filename.replace('.txt', '')
        color = colors[i % len(colors)]
        preference_files.append((person_name, file_path, color))
    
    return preference_files

def visualize_preferences():
    """Create a visualization of all edit preferences."""
    # Video information
    videos = ['A019', 'A011', 'A005']  # A005 (top), A011 (middle), A019 (bottom)
    video_duration = 3 * 60 + 30  # 3:30 minutes in seconds
    row_height = 1.0
    bar_height = 0.7
    label = ['3', '2', '1']
    
    # Get preference files from input directory
    input_dir = 'input'
    people = get_preference_files(input_dir)
    
    if not people:
        print("No preference files found in the input directory!")
        return
    
    print(f"Found {len(people)} preference files:")
    for person_name, file_path, color in people:
        print(f"  - {person_name}: {file_path}")
    
    # Parse all preference files
    all_preferences = {}
    for person_name, file_path, color in people:
        preferences = parse_preference_file(file_path)
        all_preferences[person_name] = preferences
    
    # Create the visualization
    fig, ax = plt.subplots(figsize=(15, 6))
    
    # Set up the plot
    ax.set_xlim(0, video_duration)
    ax.set_ylim(-0.5, len(videos) - 0.5)
    
    # Add video labels on y-axis
    ax.set_yticks(range(len(videos)))
    ax.set_yticklabels(label)
    #ax.set_yticklabels(videos)
    #ax.set_ylabel('Videos')
    
    # Add time labels on x-axis (every 30 seconds)
    time_ticks = list(range(0, video_duration + 1, 30))
    time_labels = [f"{t//60}:{t%60:02d}" for t in time_ticks]
    ax.set_xticks(time_ticks)
    ax.set_xticklabels(time_labels)
    ax.set_xlabel('Time (MM:SS)')
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Draw video timeline bars (all same height)
    for i, video in enumerate(videos):
        # Draw the full video timeline
        rect = patches.Rectangle((0, i - row_height/2), video_duration, row_height, 
                               linewidth=1, edgecolor='black', 
                               facecolor='lightgray', alpha=0.5)
        ax.add_patch(rect)
        
        # Add video label
        ax.text(-10, i, video, ha='right', va='center', fontweight='bold')
    
    # Draw excluded time ranges for each person
    legend_elements = []
    for person_name, file_path, color in people:
        preferences = all_preferences[person_name]
        
        for video in videos:
            if video in preferences:
                for start_sec, end_sec in preferences[video]:
                    video_index = videos.index(video)
                    
                    # Draw the excluded time range
                    rect = patches.Rectangle((start_sec, video_index - bar_height/2), 
                                           end_sec - start_sec, bar_height,
                                           linewidth=1, edgecolor='black',
                                           facecolor=color, alpha=0.7)
                    ax.add_patch(rect)
                    
                    # Add time label at the bottom of the block
                    center_x = (start_sec + end_sec) / 2
                    bottom_y = video_index - bar_height/2 - 0.05
                    time_label = f"{start_sec//60}:{start_sec%60:02d}-{end_sec//60}:{end_sec%60:02d}"
                    ax.text(center_x, bottom_y, time_label, 
                           ha='center', va='top', fontsize=8, fontweight='bold',
                           color='black', backgroundcolor='white', alpha=0.8)
        
        # Add to legend
        legend_elements.append(patches.Patch(color=color, label=person_name))
    
    # Add legend
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))
    
    # Add title
    plt.title('Dance Video Edit Preferences\n(Blocks = parts to exclude)', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Adjust layout
    plt.tight_layout()
    
    # Generate output filename with number
    output_dir = 'output'
    output_number = get_next_output_number(output_dir)
    output_filename = f'edit_preferences_visualization_{output_number:02d}.png'
    output_path = os.path.join(output_dir, output_filename)
    
    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved as '{output_path}'")
    
    # Show the plot (will not display in WSL, but left for completeness)
    plt.show()

def print_summary():
    """Print a summary of all preferences."""
    print("\n=== EDIT PREFERENCES SUMMARY ===\n")
    
    input_dir = 'input'
    people = get_preference_files(input_dir)
    
    for person_name, file_path, color in people:
        print(f"{person_name}'s preferences:")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    for line in content.split('\n'):
                        print(f"  {line}")
                else:
                    print("  No preferences specified")
        else:
            print(f"  File {file_path} not found")
        print()

if __name__ == "__main__":
    print("Dance Edit Preferences Visualizer")
    print("=" * 40)
    
    # Print summary first
    print_summary()
    
    # Create visualization
    print("Creating visualization...")
    visualize_preferences()
    
    print("\nDone! Check the 'output' folder for the visualization.") 