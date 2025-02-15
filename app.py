import gradio as gr
import numpy as np
import soundfile as sf
import datetime
import os
import re
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

def load_effect_presets():
    """
    Scans the 'pedalboard/' directory for .pdl files and returns a sorted list of filenames.
    """
    return sorted([f for f in os.listdir("pedalboard") if f.endswith(".pdl")])

def process_effect(audio_input, effect):
    """
    Process the uploaded or recorded audio using the selected effect from a .pdl file.
    The function reads the effect chain and output filename from the .pdl file,
    applies the chain to the input audio, saves the processed audio with a timestamp,
    and returns the file path.
    """
    if audio_input is None:
        return None

    sample_rate, audio_data = audio_input
    audio_data = np.array(audio_data, dtype=np.float32)
    if audio_data.ndim == 1:
        audio_data = np.expand_dims(audio_data, axis=1)

    pdl_file_path = os.path.join("pedalboard", effect)
    try:
        with open(pdl_file_path, "r") as f:
            content = f.read()
    except Exception as e:
        raise ValueError(f"Error reading {pdl_file_path}: {e}")

    match = re.search(r'(\[.*?\])\s*,\s*"([^"]+)"', content, re.DOTALL)
    if not match:
        raise ValueError("Invalid .pdl file format. Expected format: [effects], \"output_filename.wav\"")

    effect_chain_str = match.group(1)
    output_filename = match.group(2)

    allowed_effects = {
        "Chorus": Chorus,
        "Compressor": Compressor,
        "Delay": Delay,
        "Distortion": Distortion,
        "HighpassFilter": HighpassFilter,
        "LowpassFilter": LowpassFilter,
        "Phaser": Phaser,
        "Reverb": Reverb,
        "PitchShift": PitchShift,
        "Limiter": Limiter,
        "LadderFilter": LadderFilter,
    }

    try:
        board_list = eval(effect_chain_str, {"__builtins__": None}, allowed_effects)
    except Exception as e:
        raise ValueError(f"Error evaluating effect chain: {e}")

    board = Pedalboard(board_list)
    processed_audio = board(audio_data, sample_rate)

    max_amp = np.max(np.abs(processed_audio))
    if max_amp > 1.0:
        processed_audio = processed_audio / max_amp

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = output_filename.rsplit('.', 1)
    timestamped_filename = f"{name}_{timestamp}.{ext}"
    sf.write(timestamped_filename, processed_audio, sample_rate)

    return timestamped_filename

def build_designer_chain(
    # Chorus Subtle
    chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
    # Chorus Intense
    chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
    # Compressor
    compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
    # Delay Single
    delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
    # Delay Multi
    delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
    delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
    # Distortion Mild
    distortion_mild_enable, distortion_mild_drive_db,
    # Distortion Heavy
    distortion_heavy_enable, distortion_heavy_drive_db,
    # Filters (combined Highpass and Lowpass)
    filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
    # Ladder Filter
    ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
    # Phaser
    phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
    # Reverb Small
    reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
    # Reverb Large
    reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
    # Pitch Shift Up & Down
    pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value
):
    effects_str_list = []
    effects_objs_list = []
    enabled_effect_names = []

    if chorus_subtle_enable:
        s = f"Chorus(rate_hz={chorus_subtle_rate_hz}, depth={chorus_subtle_depth}, mix={chorus_subtle_mix})"
        effects_str_list.append(s)
        effects_objs_list.append(Chorus(rate_hz=chorus_subtle_rate_hz, depth=chorus_subtle_depth, mix=chorus_subtle_mix))
        enabled_effect_names.append("Chorus Subtle")
    if chorus_intense_enable:
        s = f"Chorus(rate_hz={chorus_intense_rate_hz}, depth={chorus_intense_depth}, mix={chorus_intense_mix})"
        effects_str_list.append(s)
        effects_objs_list.append(Chorus(rate_hz=chorus_intense_rate_hz, depth=chorus_intense_depth, mix=chorus_intense_mix))
        enabled_effect_names.append("Chorus Intense")
    if compressor_enable:
        s = f"Compressor(threshold_db={comp_threshold_db}, ratio={comp_ratio}, attack_ms={comp_attack_ms}, release_ms={comp_release_ms})"
        effects_str_list.append(s)
        effects_objs_list.append(Compressor(threshold_db=comp_threshold_db, ratio=comp_ratio, attack_ms=comp_attack_ms, release_ms=comp_release_ms))
        enabled_effect_names.append("Compressor")
    if delay_single_enable:
        s = f"Delay(delay_seconds={delay_single_delay_seconds}, feedback={delay_single_feedback}, mix={delay_single_mix})"
        effects_str_list.append(s)
        effects_objs_list.append(Delay(delay_seconds=delay_single_delay_seconds, feedback=delay_single_feedback, mix=delay_single_mix))
        enabled_effect_names.append("Delay Single")
    if delay_multi_enable:
        s1 = f"Delay(delay_seconds={delay_multi_1_delay_seconds}, feedback={delay_multi_1_feedback}, mix={delay_multi_1_mix})"
        s2 = f"Delay(delay_seconds={delay_multi_2_delay_seconds}, feedback={delay_multi_2_feedback}, mix={delay_multi_2_mix})"
        effects_str_list.append(s1)
        effects_str_list.append(s2)
        effects_objs_list.append(Delay(delay_seconds=delay_multi_1_delay_seconds, feedback=delay_multi_1_feedback, mix=delay_multi_1_mix))
        effects_objs_list.append(Delay(delay_seconds=delay_multi_2_delay_seconds, feedback=delay_multi_2_feedback, mix=delay_multi_2_mix))
        enabled_effect_names.append("Delay Multi")
    if distortion_mild_enable:
        s = f"Distortion(drive_db={distortion_mild_drive_db})"
        effects_str_list.append(s)
        effects_objs_list.append(Distortion(drive_db=distortion_mild_drive_db))
        enabled_effect_names.append("Distortion Mild")
    if distortion_heavy_enable:
        s = f"Distortion(drive_db={distortion_heavy_drive_db})"
        effects_str_list.append(s)
        effects_objs_list.append(Distortion(drive_db=distortion_heavy_drive_db))
        enabled_effect_names.append("Distortion Heavy")
    if filters_enable:
        s1 = f"HighpassFilter(cutoff_frequency_hz={filters_highpass_cutoff})"
        s2 = f"LowpassFilter(cutoff_frequency_hz={filters_lowpass_cutoff})"
        effects_str_list.append(s1)
        effects_str_list.append(s2)
        effects_objs_list.append(HighpassFilter(cutoff_frequency_hz=filters_highpass_cutoff))
        effects_objs_list.append(LowpassFilter(cutoff_frequency_hz=filters_lowpass_cutoff))
        enabled_effect_names.append("Filters")
    if ladder_filter_enable:
        s = f"LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz={ladder_cutoff_hz}, resonance={ladder_resonance}, drive={ladder_drive})"
        effects_str_list.append(s)
        effects_objs_list.append(LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=ladder_cutoff_hz, resonance=ladder_resonance, drive=ladder_drive))
        enabled_effect_names.append("Ladder Filter")
    if phaser_enable:
        s = f"Phaser(rate_hz={phaser_rate_hz}, depth={phaser_depth}, feedback={phaser_feedback}, mix={phaser_mix})"
        effects_str_list.append(s)
        effects_objs_list.append(Phaser(rate_hz=phaser_rate_hz, depth=phaser_depth, feedback=phaser_feedback, mix=phaser_mix))
        enabled_effect_names.append("Phaser")
    if reverb_small_enable:
        s = f"Reverb(room_size={reverb_small_room_size}, damping={reverb_small_damping}, width={reverb_small_width}, wet_level={reverb_small_wet_level})"
        effects_str_list.append(s)
        effects_objs_list.append(Reverb(room_size=reverb_small_room_size, damping=reverb_small_damping, width=reverb_small_width, wet_level=reverb_small_wet_level))
        enabled_effect_names.append("Reverb Small")
    if reverb_large_enable:
        s = f"Reverb(room_size={reverb_large_room_size}, damping={reverb_large_damping}, width={reverb_large_width}, wet_level={reverb_large_wet_level})"
        effects_str_list.append(s)
        effects_objs_list.append(Reverb(room_size=reverb_large_room_size, damping=reverb_large_damping, width=reverb_large_width, wet_level=reverb_large_wet_level))
        enabled_effect_names.append("Reverb Large")
    if pitch_shift_up_enable:
        s = f"PitchShift(semitones={pitch_shift_up_value})"
        effects_str_list.append(s)
        effects_objs_list.append(PitchShift(semitones=pitch_shift_up_value))
        enabled_effect_names.append("Pitch Shift Up")
    if pitch_shift_down_enable:
        s = f"PitchShift(semitones={pitch_shift_down_value})"
        effects_str_list.append(s)
        effects_objs_list.append(PitchShift(semitones=pitch_shift_down_value))
        enabled_effect_names.append("Pitch Shift Down")
        
    chain_str = "[" + ", ".join(effects_str_list) + "],"
    return chain_str, effects_objs_list, enabled_effect_names

def generate_preset_preview(preset_title,
    # Chorus Subtle
    chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
    # Chorus Intense
    chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
    # Compressor
    compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
    # Delay Single
    delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
    # Delay Multi
    delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
    delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
    # Distortion Mild
    distortion_mild_enable, distortion_mild_drive_db,
    # Distortion Heavy
    distortion_heavy_enable, distortion_heavy_drive_db,
    # Filters
    filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
    # Ladder Filter
    ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
    # Phaser
    phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
    # Reverb Small
    reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
    # Reverb Large
    reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
    # Pitch Shifts
    pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value
):
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    chain_str, _, enabled_effect_names = build_designer_chain(
        chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
        chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
        compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
        delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
        delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
        delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
        distortion_mild_enable, distortion_mild_drive_db,
        distortion_heavy_enable, distortion_heavy_drive_db,
        filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
        ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
        phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
        reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
        reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
        pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value
    )
    if preset_title.strip():
        final_title = preset_title.strip()
    else:
        if enabled_effect_names:
            final_title = "_".join(enabled_effect_names) + "_" + now
        else:
            final_title = "Preset_" + now
    preset_content = "\n".join([
        f"# {final_title}",
        f"{chain_str}",
        f"\"{final_title}.wav\""
    ])
    return preset_content

def process_designer(audio_input, preset_title,
    # Chorus Subtle
    chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
    # Chorus Intense
    chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
    # Compressor
    compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
    # Delay Single
    delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
    # Delay Multi
    delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
    delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
    # Distortion Mild
    distortion_mild_enable, distortion_mild_drive_db,
    # Distortion Heavy
    distortion_heavy_enable, distortion_heavy_drive_db,
    # Filters
    filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
    # Ladder Filter
    ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
    # Phaser
    phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
    # Reverb Small
    reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
    # Reverb Large
    reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
    # Pitch Shifts
    pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value
):
    if audio_input is None:
        return None
    sample_rate, audio_data = audio_input
    audio_data = np.array(audio_data, dtype=np.float32)
    if audio_data.ndim == 1:
        audio_data = np.expand_dims(audio_data, axis=1)
    _, effects_objs, _ = build_designer_chain(
        chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
        chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
        compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
        delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
        delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
        delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
        distortion_mild_enable, distortion_mild_drive_db,
        distortion_heavy_enable, distortion_heavy_drive_db,
        filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
        ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
        phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
        reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
        reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
        pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value
    )
    board = Pedalboard(effects_objs)
    processed_audio = board(audio_data, sample_rate)
    max_amp = np.max(np.abs(processed_audio))
    if max_amp > 1.0:
        processed_audio = processed_audio / max_amp

    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if preset_title.strip():
        final_title = preset_title.strip()
    else:
        _, _, enabled_effect_names = build_designer_chain(
            chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
            chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
            compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
            delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
            delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
            delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
            distortion_mild_enable, distortion_mild_drive_db,
            distortion_heavy_enable, distortion_heavy_drive_db,
            filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
            ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
            phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
            reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
            reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
            pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value
        )
        if enabled_effect_names:
            final_title = "_".join(enabled_effect_names) + "_" + now
        else:
            final_title = "Preset_" + now

    output_filename = f"{final_title}_{now}.wav"
    sf.write(output_filename, processed_audio, sample_rate)
    return output_filename

def save_preset(preset_title,
    # Chorus Subtle
    chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
    # Chorus Intense
    chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
    # Compressor
    compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
    # Delay Single
    delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
    # Delay Multi
    delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
    delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
    # Distortion Mild
    distortion_mild_enable, distortion_mild_drive_db,
    # Distortion Heavy
    distortion_heavy_enable, distortion_heavy_drive_db,
    # Filters
    filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
    # Ladder Filter
    ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
    # Phaser
    phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
    # Reverb Small
    reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
    # Reverb Large
    reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
    # Pitch Shifts
    pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value
):
    preview = generate_preset_preview(preset_title,
        chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
        chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
        compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
        delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
        delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
        delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
        distortion_mild_enable, distortion_mild_drive_db,
        distortion_heavy_enable, distortion_heavy_drive_db,
        filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
        ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
        phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
        reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
        reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
        pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value
    )
    final_title = preview.splitlines()[0].lstrip("# ").strip()
    filename = f"{final_title}.pdl"
    try:
        with open(filename, "w") as f:
            f.write(preview)
        return f"Preset saved to {filename}"
    except Exception as e:
        return f"Error saving preset: {e}"

with gr.Blocks() as demo:
    gr.Markdown("## Pedalboard Audio Effects Demo")
    with gr.Tabs():
        with gr.Tab("Effects Demo"):
            with gr.Row():
                audio_input = gr.Audio(type="numpy", label="Input Audio (upload or record)")
                effect_select = gr.Dropdown(choices=load_effect_presets(), label="Select an Effect (.pdl)")
            output_audio = gr.Audio(label="Processed Audio", type="filepath")
            process_button = gr.Button("Process Audio")
            process_button.click(process_effect, inputs=[audio_input, effect_select], outputs=output_audio)
        
        with gr.Tab("Designer"):
            gr.Markdown("## Designer: Create New Presets")
            preset_title = gr.Textbox(label="Preset Title", placeholder="Enter preset title (or leave blank for default)")
            
            gr.Markdown("### Chorus Subtle")
            chorus_subtle_enable = gr.Checkbox(label="Enable Chorus Subtle", value=False)
            chorus_subtle_rate_hz = gr.Slider(0, 5, value=1.0, label="Rate (Hz)")
            chorus_subtle_depth = gr.Slider(0, 1, value=0.25, label="Depth")
            chorus_subtle_mix = gr.Slider(0, 1, value=0.3, label="Mix")
            
            gr.Markdown("### Chorus Intense")
            chorus_intense_enable = gr.Checkbox(label="Enable Chorus Intense", value=False)
            chorus_intense_rate_hz = gr.Slider(0, 5, value=3.0, label="Rate (Hz)")
            chorus_intense_depth = gr.Slider(0, 1, value=0.8, label="Depth")
            chorus_intense_mix = gr.Slider(0, 1, value=0.7, label="Mix")
            
            gr.Markdown("### Compressor")
            compressor_enable = gr.Checkbox(label="Enable Compressor", value=False)
            comp_threshold_db = gr.Slider(-60, 0, value=-20, label="Threshold (dB)")
            comp_ratio = gr.Slider(1, 20, value=4, label="Ratio")
            comp_attack_ms = gr.Slider(1, 50, value=5, label="Attack (ms)")
            comp_release_ms = gr.Slider(50, 500, value=100, label="Release (ms)")
            
            gr.Markdown("### Delay Single")
            delay_single_enable = gr.Checkbox(label="Enable Delay Single", value=False)
            delay_single_delay_seconds = gr.Slider(0, 1, value=0.3, label="Delay (seconds)")
            delay_single_feedback = gr.Slider(0, 1, value=0.4, label="Feedback")
            delay_single_mix = gr.Slider(0, 1, value=0.4, label="Mix")
            
            gr.Markdown("### Delay Multi")
            delay_multi_enable = gr.Checkbox(label="Enable Delay Multi", value=False)
            gr.Markdown("#### First Delay")
            delay_multi_1_delay_seconds = gr.Slider(0, 1, value=0.2, label="Delay (seconds)")
            delay_multi_1_feedback = gr.Slider(0, 1, value=0.3, label="Feedback")
            delay_multi_1_mix = gr.Slider(0, 1, value=0.3, label="Mix")
            gr.Markdown("#### Second Delay")
            delay_multi_2_delay_seconds = gr.Slider(0, 1, value=0.4, label="Delay (seconds)")
            delay_multi_2_feedback = gr.Slider(0, 1, value=0.2, label="Feedback")
            delay_multi_2_mix = gr.Slider(0, 1, value=0.2, label="Mix")
            
            gr.Markdown("### Distortion Mild")
            distortion_mild_enable = gr.Checkbox(label="Enable Distortion Mild", value=False)
            distortion_mild_drive_db = gr.Slider(0, 30, value=10, label="Drive (dB)")
            
            gr.Markdown("### Distortion Heavy")
            distortion_heavy_enable = gr.Checkbox(label="Enable Distortion Heavy", value=False)
            distortion_heavy_drive_db = gr.Slider(0, 30, value=25, label="Drive (dB)")
            
            gr.Markdown("### Filters")
            filters_enable = gr.Checkbox(label="Enable Filters", value=False)
            filters_highpass_cutoff = gr.Slider(20, 2000, value=500, label="Highpass Cutoff (Hz)")
            filters_lowpass_cutoff = gr.Slider(2000, 20000, value=5000, label="Lowpass Cutoff (Hz)")
            
            gr.Markdown("### Ladder Filter")
            ladder_filter_enable = gr.Checkbox(label="Enable Ladder Filter", value=False)
            ladder_cutoff_hz = gr.Slider(20, 20000, value=1000, label="Cutoff (Hz)")
            ladder_resonance = gr.Slider(0, 1, value=0.7, label="Resonance")
            ladder_drive = gr.Slider(0, 3, value=1.5, label="Drive")
            
            gr.Markdown("### Phaser")
            phaser_enable = gr.Checkbox(label="Enable Phaser", value=False)
            phaser_rate_hz = gr.Slider(0, 5, value=1.0, label="Rate (Hz)")
            phaser_depth = gr.Slider(0, 1, value=0.5, label="Depth")
            phaser_feedback = gr.Slider(0, 1, value=0.5, label="Feedback")
            phaser_mix = gr.Slider(0, 1, value=0.5, label="Mix")
            
            gr.Markdown("### Reverb Small")
            reverb_small_enable = gr.Checkbox(label="Enable Reverb Small", value=False)
            reverb_small_room_size = gr.Slider(0, 1, value=0.3, label="Room Size")
            reverb_small_damping = gr.Slider(0, 1, value=0.5, label="Damping")
            reverb_small_width = gr.Slider(0, 1, value=0.7, label="Width")
            reverb_small_wet_level = gr.Slider(0, 1, value=0.4, label="Wet Level")
            
            gr.Markdown("### Reverb Large")
            reverb_large_enable = gr.Checkbox(label="Enable Reverb Large", value=False)
            reverb_large_room_size = gr.Slider(0, 1, value=0.9, label="Room Size")
            reverb_large_damping = gr.Slider(0, 1, value=0.2, label="Damping")
            reverb_large_width = gr.Slider(0, 1, value=1.0, label="Width")
            reverb_large_wet_level = gr.Slider(0, 1, value=0.5, label="Wet Level")
            
            gr.Markdown("### Pitch Shift Up")
            pitch_shift_up_enable = gr.Checkbox(label="Enable Pitch Shift Up", value=False)
            pitch_shift_up_value = gr.Slider(1, 12, value=12, label="Semitones (Up)")
            
            gr.Markdown("### Pitch Shift Down")
            pitch_shift_down_enable = gr.Checkbox(label="Enable Pitch Shift Down", value=False)
            pitch_shift_down_value = gr.Slider(-12, -1, value=-12, label="Semitones (Down)")
            
            preview_button = gr.Button("Preview Preset")
            preset_preview_box = gr.Textbox(label="Preset Preview", lines=4)
            preview_button.click(generate_preset_preview, 
                inputs=[preset_title,
                        chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
                        chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
                        compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
                        delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
                        delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
                        delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
                        distortion_mild_enable, distortion_mild_drive_db,
                        distortion_heavy_enable, distortion_heavy_drive_db,
                        filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
                        ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
                        phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
                        reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
                        reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
                        pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value],
                outputs=preset_preview_box)
            
            designer_audio_input = gr.Audio(type="numpy", label="Input Audio (Designer)")
            designer_output_audio = gr.Audio(label="Processed Audio (Designer)", type="filepath")
            process_designer_button = gr.Button("Process Audio (Designer)")
            process_designer_button.click(process_designer, 
                inputs=[designer_audio_input, preset_title,
                        chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
                        chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
                        compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
                        delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
                        delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
                        delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
                        distortion_mild_enable, distortion_mild_drive_db,
                        distortion_heavy_enable, distortion_heavy_drive_db,
                        filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
                        ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
                        phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
                        reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
                        reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
                        pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value],
                outputs=designer_output_audio)
            
            save_button = gr.Button("Save Preset")
            save_message = gr.Textbox(label="Save Preset Message")
            save_button.click(save_preset, 
                inputs=[preset_title,
                        chorus_subtle_enable, chorus_subtle_rate_hz, chorus_subtle_depth, chorus_subtle_mix,
                        chorus_intense_enable, chorus_intense_rate_hz, chorus_intense_depth, chorus_intense_mix,
                        compressor_enable, comp_threshold_db, comp_ratio, comp_attack_ms, comp_release_ms,
                        delay_single_enable, delay_single_delay_seconds, delay_single_feedback, delay_single_mix,
                        delay_multi_enable, delay_multi_1_delay_seconds, delay_multi_1_feedback, delay_multi_1_mix,
                        delay_multi_2_delay_seconds, delay_multi_2_feedback, delay_multi_2_mix,
                        distortion_mild_enable, distortion_mild_drive_db,
                        distortion_heavy_enable, distortion_heavy_drive_db,
                        filters_enable, filters_highpass_cutoff, filters_lowpass_cutoff,
                        ladder_filter_enable, ladder_cutoff_hz, ladder_resonance, ladder_drive,
                        phaser_enable, phaser_rate_hz, phaser_depth, phaser_feedback, phaser_mix,
                        reverb_small_enable, reverb_small_room_size, reverb_small_damping, reverb_small_width, reverb_small_wet_level,
                        reverb_large_enable, reverb_large_room_size, reverb_large_damping, reverb_large_width, reverb_large_wet_level,
                        pitch_shift_up_enable, pitch_shift_down_enable, pitch_shift_up_value, pitch_shift_down_value],
                outputs=save_message)
                
demo.launch()
