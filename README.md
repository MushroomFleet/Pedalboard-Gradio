# Pedalboard Audio Effects Demo
![demo-ui](https://raw.githubusercontent.com/MushroomFleet/Pedalboard-Gradio/refs/heads/main/images/demo-uiiii.png)

This project is a demonstration of real-time audio processing using Python. It leverages the [Gradio](https://gradio.app/) library to provide an interactive web interface and the [Pedalboard](https://github.com/spotify/pedalboard) library to apply a wide variety of audio effects to uploaded or recorded audio.

With recent updates, all audio effect configurations are now externalized into separate **.pdl** files stored in the `pedalboard/` directory. Additionally, the Gradio interface features a new **Designer** tab that allows you to interactively create, preview, and save custom effect presets in the `.pdl` format.

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
- The Gradio web interface will launch in your default browser.

### Using the Effects Demo
- **Input Audio:** Upload or record an audio file using the provided audio input.
- **Select an Effect:** Choose an effect preset from the dropdown list. These presets are defined in `.pdl` files located in the `pedalboard/` directory.
- **Process Audio:** Click the **Process Audio** button to apply the selected effect chain. The processed audio is normalized and saved as a timestamped `.wav` file (e.g., `chorus_subtle_20250215_094114.wav`), which can then be played back directly.

### Using the Designer Tab
- **Create New Presets:** Navigate to the **Designer** tab to design custom audio effect presets.
- **Preset Title:** Enter a title for your new preset (or leave it blank for a default title based on the enabled effects).
- **Configure Effects:** Adjust various effect parameters (e.g., Chorus, Compressor, Delay, Distortion, Filters, etc.) using interactive sliders and checkboxes.
- **Preview Preset:** Click **Preview Preset** to generate a text preview of the new preset, which shows the effect chain in `.pdl` format.
- **Save Preset:** Once satisfied with the preview, click **Save Preset** to store your new preset as a `.pdl` file in the project directory.

## What app.py Does

- **Externalized Presets:** Reads audio effect definitions from `.pdl` files found in the `pedalboard/` directory.
- **Audio Processing:** Converts the uploaded audio into a NumPy array, applies the selected effect chain via the Pedalboard library, normalizes the signal, and saves the processed audio with a timestamp.
- **Interactive Interface:** Provides two primary tabs in the Gradio interface:
  - **Effects Demo:** For applying pre-defined effect chains.
  - **Designer:** For interactively creating, previewing, and saving new effect presets in the `.pdl` format.

## Output

- **Processed Audio:** The output audio files are saved with unique, timestamped filenames to prevent overwrites.
- **New Presets:** Presets created via the Designer tab are stored as `.pdl` files that include:
  - A header with the preset title.
  - An effect chain definition enclosed in square brackets.
  - An output filename specification in quotes.

## Additional Information

- For manual editing or creation of presets, refer to the guidelines in the [pedalboard.md](pedalboard/pedalboard.md) file located in the `pedalboard/` directory.
- Ensure that your input audio is in a supported format and maintains an adequate quality for optimal processing.
