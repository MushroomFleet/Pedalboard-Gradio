import soundfile as sf
from pedalboard import (
    Pedalboard, 
    Chorus, 
    Compressor, 
    Delay, 
    Distortion,
    Gain,
    HighpassFilter,
    LowpassFilter,
    Phaser,
    Reverb,
    PitchShift,
    Limiter,
    LadderFilter
)
import numpy as np

class PedalboardDemo:
    def __init__(self, input_file):
        """Initialize the demo with an input audio file."""
        self.audio, self.sample_rate = sf.read(input_file)
        
    def save_audio(self, audio_data, filename):
        """Save the processed audio to a file."""
        sf.write(filename, audio_data, self.sample_rate)
        
    def demo_all_effects(self):
        """Run all effect demos."""
        self.demo_chorus()
        self.demo_compressor()
        self.demo_delay()
        self.demo_distortion()
        self.demo_filters()
        self.demo_phaser()
        self.demo_reverb()
        self.demo_pitch_shift()
        self.demo_combined_effects()
        
    def demo_chorus(self):
        """Demonstrate chorus effect with different settings."""
        # Subtle chorus
        subtle_board = Pedalboard([
            Chorus(rate_hz=1.0, depth=0.25, mix=0.3)
        ])
        subtle = subtle_board(self.audio, self.sample_rate)
        self.save_audio(subtle, "chorus_subtle.wav")
        
        # Intense chorus
        intense_board = Pedalboard([
            Chorus(rate_hz=3.0, depth=0.8, mix=0.7)
        ])
        intense = intense_board(self.audio, self.sample_rate)
        self.save_audio(intense, "chorus_intense.wav")
        
    def demo_compressor(self):
        """Demonstrate compressor with different settings."""
        board = Pedalboard([
            Compressor(
                threshold_db=-20,
                ratio=4,
                attack_ms=5,
                release_ms=100
            )
        ])
        processed = board(self.audio, self.sample_rate)
        self.save_audio(processed, "compressed.wav")
        
    def demo_delay(self):
        """Demonstrate delay effect with different settings."""
        # Single delay
        single_board = Pedalboard([
            Delay(delay_seconds=0.3, feedback=0.4, mix=0.4)
        ])
        single = single_board(self.audio, self.sample_rate)
        self.save_audio(single, "delay_single.wav")
        
        # Multiple delays
        multi_board = Pedalboard([
            Delay(delay_seconds=0.2, feedback=0.3, mix=0.3),
            Delay(delay_seconds=0.4, feedback=0.2, mix=0.2)
        ])
        multi = multi_board(self.audio, self.sample_rate)
        self.save_audio(multi, "delay_multi.wav")
        
    def demo_distortion(self):
        """Demonstrate distortion with different drive levels."""
        # Mild overdrive
        mild_board = Pedalboard([
            Distortion(drive_db=10)
        ])
        mild = mild_board(self.audio, self.sample_rate)
        self.save_audio(mild, "distortion_mild.wav")
        
        # Heavy distortion
        heavy_board = Pedalboard([
            Distortion(drive_db=25)
        ])
        heavy = heavy_board(self.audio, self.sample_rate)
        self.save_audio(heavy, "distortion_heavy.wav")
        
    def demo_filters(self):
        """Demonstrate various filter effects."""
        # High-pass and low-pass combination
        filter_board = Pedalboard([
            HighpassFilter(cutoff_frequency_hz=500),
            LowpassFilter(cutoff_frequency_hz=5000)
        ])
        filtered = filter_board(self.audio, self.sample_rate)
        self.save_audio(filtered, "filtered.wav")
        
        # Ladder filter sweep
        ladder_board = Pedalboard([
            LadderFilter(
                mode=LadderFilter.Mode.HPF12,
                cutoff_hz=1000,
                resonance=0.7,
                drive=1.5
            )
        ])
        ladder = ladder_board(self.audio, self.sample_rate)
        self.save_audio(ladder, "ladder_filter.wav")
        
    def demo_phaser(self):
        """Demonstrate phaser effect."""
        board = Pedalboard([
            Phaser(
                rate_hz=1.0,
                depth=0.5,
                feedback=0.5,
                mix=0.5
            )
        ])
        processed = board(self.audio, self.sample_rate)
        self.save_audio(processed, "phaser.wav")
        
    def demo_reverb(self):
        """Demonstrate reverb with different room sizes."""
        # Small room
        small_board = Pedalboard([
            Reverb(room_size=0.3, damping=0.5, width=0.7, wet_level=0.4)
        ])
        small = small_board(self.audio, self.sample_rate)
        self.save_audio(small, "reverb_small.wav")
        
        # Large hall
        large_board = Pedalboard([
            Reverb(room_size=0.9, damping=0.2, width=1.0, wet_level=0.5)
        ])
        large = large_board(self.audio, self.sample_rate)
        self.save_audio(large, "reverb_large.wav")
        
    def demo_pitch_shift(self):
        """Demonstrate pitch shifting."""
        # Shift up one octave
        up_board = Pedalboard([
            PitchShift(semitones=12)
        ])
        up = up_board(self.audio, self.sample_rate)
        self.save_audio(up, "pitch_up.wav")
        
        # Shift down one octave
        down_board = Pedalboard([
            PitchShift(semitones=-12)
        ])
        down = down_board(self.audio, self.sample_rate)
        self.save_audio(down, "pitch_down.wav")
        
    def demo_combined_effects(self):
        """Demonstrate a complex chain of effects."""
        board = Pedalboard([
            Compressor(threshold_db=-20, ratio=3),
            Chorus(rate_hz=1.0, depth=0.25, mix=0.3),
            Delay(delay_seconds=0.25, feedback=0.3),
            Reverb(room_size=0.6, damping=0.4),
            Limiter(threshold_db=-2.0)
        ])
        processed = board(self.audio, self.sample_rate)
        self.save_audio(processed, "combined_effects.wav")

def main():
    """Run the complete demo."""
    # Replace 'input.wav' with your audio file
    demo = PedalboardDemo('input.wav')
    demo.demo_all_effects()
    print("Demo complete! Check the output files in the current directory.")

if __name__ == "__main__":
    main()