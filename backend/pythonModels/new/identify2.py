import sys
import librosa
import numpy as np
from fastdtw import fastdtw

def extract_mfcc(audio_path):
    # Adjust the sampling rate if needed
    audio, _ = librosa.load(audio_path, sr=16000)
    mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)
    mfccs -= (np.mean(mfccs, axis=1)[:, np.newaxis] + 1e-8)
    mfccs /= (np.std(mfccs, axis=1)[:, np.newaxis] + 1e-8)
    return mfccs

def scale_features(features):
    mean = np.mean(features, axis=1)
    std = np.std(features, axis=1)
    scaled_features = (
        features - mean[:, np.newaxis]) / (std[:, np.newaxis] + 1e-8)
    return scaled_features

if __name__ == "__main":
    if len(sys.argv) != 2:
        print("Usage: python identify.py <audio_file_path>")
        sys.exit(1)

    audio_path = sys.argv[1]
    print("Audio file path:", audio_path)  # Print the audio file path

    # Replace these paths with the actual paths to your reference voice clips
    voice_clip1_path = "1.wav"
    voice_clip2_path = "2.wav"

    # Extract MFCC features for both voice clips
    mfccs1 = extract_mfcc(voice_clip1_path)
    mfccs2 = extract_mfcc(voice_clip2_path)

    # Scale the features
    scaled_mfccs1 = scale_features(mfccs1)
    scaled_mfccs2 = scale_features(mfccs2)

    # Flatten the scaled MFCC features
    flattened_mfccs1 = scaled_mfccs1.flatten()
    flattened_mfccs2 = scaled_mfccs2.flatten()

    # Calculate Dynamic Time Warping (DTW) distance for the original MFCC features
    dtw_distance, _ = fastdtw(scaled_mfccs1.T, scaled_mfccs2.T)

    # Set the DTW distance threshold (adjust based on your data and requirements)
    dtw_threshold = 1000

    # Create a dictionary to hold the result
    result = {
        "dtw_distance": dtw_distance,
        "is_same_user": dtw_distance <= dtw_threshold
    }
    print(result)
