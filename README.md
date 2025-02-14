# Pedalboard Audio Effects Demo

This project is a demonstration of real-time audio processing using Python. It leverages the [Gradio](https://gradio.app/) library to provide an interactive web interface and the [Pedalboard](https://github.com/spotify/pedalboard) library to apply a wide variety of audio effects to uploaded or recorded audio.

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Steps
1. Clone or download the repository.
2. Open a command prompt in the project directory.
3. Install the required dependencies using one of the following options:
   - **Option 1:** Run the provided batch file:
     ```
     install.bat
     ```
   - **Option 2:** Manually install dependencies:
     ```
     pip install -r requirements.txt
     ```

## Usage

### Launching the Application
- To start the Gradio interface, execute:
  ```
  start-gui.bat
  ```
  or
  ```
  python app.py
  ```
- The Gradio web interface will open in your default browser.

### Using the Interface
- **Input Audio:** Upload or record an audio file using the audio input section.
- **Select an Effect:** Choose an audio effect from the dropdown list. Available effects include:
  - Chorus Subtle
  - Chorus Intense
  - Compressor
  - Delay Single
  - Delay Multi
  - Distortion Mild
  - Distortion Heavy
  - Filters (Highpass and Lowpass Filters)
  - Ladder Filter
  - Phaser
  - Reverb Small
  - Reverb Large
  - Pitch Shift Up
  - Pitch Shift Down
  - Combined Effects
- **Process Audio:** Click the **Process Audio** button to apply the selected effect. The processed audio file, saved with a timestamp, will then be provided for playback.

### Output
- The processed audio is saved with a timestamp appended to its filename (e.g., `chorus_subtle_20250214_213015.wav`) to prevent overwrites.
- The output file can be played back directly from the interface.

## What app.py Does

- **Effect Mapping:** The script defines a mapping between human-friendly effect names and their corresponding pedalboard chains along with associated output filenames.
- **Audio Processing:** Through the `process_effect` function, it:
  - Converts the uploaded or recorded audio into a NumPy array.
  - Applies the selected effect chain using the Pedalboard library.
  - Normalizes the audio output to manage amplitude.
  - Saves the processed audio to a `.wav` file with a timestamp to avoid filename conflicts.
- **Interactive Interface:** The Gradio interface is set up using `gr.Blocks`, which enables users to upload/record audio, select an effect, process the sound, and listen to the output.

## Additional Information

- The application supports a diverse set of audio effects that offer both subtle and intense modifications.
- For best results, ensure that the input audio file is in a compatible format and of suitable quality.
