import gradio as gr
import numpy as np
import soundfile as sf
import datetime
from pedalboard import (
    Pedalboard,
    Chorus,
    Compressor,
    Delay,
    Distortion,
    HighpassFilter,
    LowpassFilter,
    Phaser,
    Reverb,
    PitchShift,
    Limiter,
    LadderFilter
)

# Mapping of available effects to their corresponding pedalboard chain and output filename
effects_options = {
    "Chorus Subtle": (
        [Chorus(rate_hz=1.0, depth=0.25, mix=0.3)],
        "chorus_subtle.wav"
    ),
    "Chorus Intense": (
        [Chorus(rate_hz=3.0, depth=0.8, mix=0.7)],
        "chorus_intense.wav"
    ),
    "Compressor": (
        [Compressor(threshold_db=-20, ratio=4, attack_ms=5, release_ms=100)],
        "compressed.wav"
    ),
    "Delay Single": (
        [Delay(delay_seconds=0.3, feedback=0.4, mix=0.4)],
        "delay_single.wav"
    ),
    "Delay Multi": (
        [Delay(delay_seconds=0.2, feedback=0.3, mix=0.3),
         Delay(delay_seconds=0.4, feedback=0.2, mix=0.2)],
        "delay_multi.wav"
    ),
    "Distortion Mild": (
        [Distortion(drive_db=10)],
        "distortion_mild.wav"
    ),
    "Distortion Heavy": (
        [Distortion(drive_db=25)],
        "distortion_heavy.wav"
    ),
    "Filters": (
        [HighpassFilter(cutoff_frequency_hz=500),
         LowpassFilter(cutoff_frequency_hz=5000)],
        "filtered.wav"
    ),
    "Ladder Filter": (
        [LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=1000, resonance=0.7, drive=1.5)],
        "ladder_filter.wav"
    ),
    "Phaser": (
        [Phaser(rate_hz=1.0, depth=0.5, feedback=0.5, mix=0.5)],
        "phaser.wav"
    ),
    "Reverb Small": (
        [Reverb(room_size=0.3, damping=0.5, width=0.7, wet_level=0.4)],
        "reverb_small.wav"
    ),
    "Reverb Large": (
        [Reverb(room_size=0.9, damping=0.2, width=1.0, wet_level=0.5)],
        "reverb_large.wav"
    ),
    "Pitch Shift Up": (
        [PitchShift(semitones=12)],
        "pitch_up.wav"
    ),
    "Pitch Shift Down": (
        [PitchShift(semitones=-12)],
        "pitch_down.wav"
    ),
    "Combined Effects": (
        [Compressor(threshold_db=-20, ratio=3),
         Chorus(rate_hz=1.0, depth=0.25, mix=0.3),
         Delay(delay_seconds=0.25, feedback=0.3),
         Reverb(room_size=0.6, damping=0.4),
         Limiter(threshold_db=-2.0)],
        "combined_effects.wav"
    )
}

def process_effect(audio_input, effect):
    """
    Process the uploaded or recorded audio using the selected effect.
    The function applies the corresponding pedalboard chain to the input audio,
    saves the processed audio to a file, and returns the file path.
    """
    if audio_input is None:
        return None

    # Gradio audio input returns a tuple: (sample_rate, audio_data)
    sample_rate, audio_data = audio_input
    # Ensure audio_data is a numpy array of type float32 and has shape (samples, channels)
    audio_data = np.array(audio_data, dtype=np.float32)
    if audio_data.ndim == 1:
        audio_data = np.expand_dims(audio_data, axis=1)

    # Retrieve the pedalboard chain and output filename for the selected effect.
    normalized_effect = effect.strip().lower()
    board_list = None
    output_filename = None
    for key, value in effects_options.items():
        if key.strip().lower() == normalized_effect:
            board_list, output_filename = value
            break
    if board_list is None:
        raise ValueError("Selected effect is not available.")

    board = Pedalboard(board_list)
    processed_audio = board(audio_data, sample_rate)

    # Normalize processed audio to ensure amplitude is not excessive.
    max_amp = np.max(np.abs(processed_audio))
    if max_amp > 1.0:
        processed_audio = processed_audio / max_amp

    # Save the processed audio to disk with a timestamp appended to the filename to prevent overwrites.
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = output_filename.rsplit('.', 1)
    timestamped_filename = f"{name}_{timestamp}.{ext}"
    sf.write(timestamped_filename, processed_audio, sample_rate)

    return timestamped_filename

# Build the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Pedalboard Audio Effects Demo")
    
    with gr.Row():
        audio_input = gr.Audio(type="numpy", label="Input Audio (upload or record)")
        effect_select = gr.Dropdown(choices=list(effects_options.keys()), label="Select an Effect")
        
    output_audio = gr.Audio(label="Processed Audio", type="filepath")
    
    process_button = gr.Button("Process Audio")
    process_button.click(process_effect, inputs=[audio_input, effect_select], outputs=output_audio)

demo.launch()
