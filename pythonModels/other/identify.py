import librosa
import numpy as np
from fastdtw import fastdtw

def extract_mfcc(audio_path):
    audio, _ = librosa.load(audio_path, sr=16000)  # Adjust the sampling rate if needed
    mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)
    mfccs -= (np.mean(mfccs, axis=1)[:, np.newaxis] + 1e-8)
    mfccs /= (np.std(mfccs, axis=1)[:, np.newaxis] + 1e-8)
    return mfccs

def scale_features(features):
    mean = np.mean(features, axis=1)
    std = np.std(features, axis=1)
    scaled_features = (features - mean[:, np.newaxis]) / (std[:, np.newaxis] + 1e-8)
    return scaled_features

# Ensure a command-line argument is provided for the audio file path
import sys
if len(sys.argv) != 2:
    print("Usage: python identify.py <audio_file_path>")
    sys.exit(1)

audio_path_ = sys.argv[1]
print("Audio file path:", audio_path_)  # Print the audio file path
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

# Compare the DTW distance to the threshold
if dtw_distance <= dtw_threshold:
    print("DTW distance: {:.2f} - Both voice clips are likely from the same user.".format(dtw_distance))
else:
    print("DTW distance: {:.2f} - Voice clips are likely from different users.".format(dtw_distance))





# import os
# import librosa
# import numpy as np
# from fastdtw import fastdtw
# from scipy.spatial.distance import cosine

# def extract_mfcc(audio_path):
#     audio, _ = librosa.load(audio_path, sr=16000)  # Adjust the sampling rate if needed
#     mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)
#     mfccs -= (np.mean(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#     mfccs /= (np.std(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#     return mfccs

# def scale_features(features):
#     mean = np.mean(features, axis=1)
#     std = np.std(features, axis=1)
#     scaled_features = (features - mean[:, np.newaxis]) / (std[:, np.newaxis] + 1e-8)
#     return scaled_features

# if len(os.sys.argv) != 2:
#     print("Usage: python identify.py <audio_file_path>")
#     os.sys.exit(1)

# audio_path = os.sys.argv[1]

# # Paths to the reference voice clips
# voice_clip1_path = "15.wav"  # Replace with your local file path
# voice_clip2_path = "2.wav"  # Replace with your local file path

# # Extract MFCC features for the reference voice clips
# mfccs1 = extract_mfcc(voice_clip1_path)
# mfccs2 = extract_mfcc(voice_clip2_path)

# # Scale the features
# scaled_mfccs1 = scale_features(mfccs1)
# scaled_mfccs2 = scale_features(mfccs2)

# # Extract and scale features for the uploaded audio
# uploaded_mfccs = extract_mfcc(audio_path)
# scaled_uploaded_mfccs = scale_features(uploaded_mfccs)

# # Calculate Dynamic Time Warping (DTW) distance for the original MFCC features
# dtw_distance, _ = fastdtw(scaled_mfccs1.T, scaled_mfccs2.T, dist=cosine)

# # Set the DTW distance threshold (adjust based on your data and requirements)
# dtw_threshold = 100  # Adjust as needed

# # Compare the DTW distance to the threshold
# if dtw_distance <= dtw_threshold:
#     print("DTW distance: {:.2f} - Both voice clips are likely from the same user.")
# else:
#     print("DTW distance: {:.2f} - Voice clips are likely from different users.")




# import librosa
# import numpy as np
# from fastdtw import fastdtw
# import sys

# def extract_mfcc(audio_path):
#     # Load the audio clip
#     audio, _ = librosa.load(audio_path, sr=16000)  # Adjust the sampling rate if needed
#     # Extract MFCCs
#     mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)
#     # Normalize MFCCs
#     mfccs -= (np.mean(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#     mfccs /= (np.std(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#     return mfccs

# def scale_features(features):
#     # Scale features to have zero mean and unit variance
#     mean = np.mean(features, axis=1)
#     std = np.std(features, axis=1)
#     scaled_features = (features - mean[:, np.newaxis]) / (std[:, np.newaxis] + 1e-8)
#     return scaled_features

# def calculate_dtw_distance(voice_clip1_path, voice_clip2_path, dtw_threshold):
#     # Extract MFCC features for both voice clips
#     mfccs1 = extract_mfcc(voice_clip1_path)
#     mfccs2 = extract_mfcc(voice_clip2_path)

#     # Scale the features
#     scaled_mfccs1 = scale_features(mfccs1)
#     scaled_mfccs2 = scale_features(mfccs2)

#     # Flatten the scaled MFCC features
#     flattened_mfccs1 = scaled_mfccs1.flatten()
#     flattened_mfccs2 = scaled_mfccs2.flatten()

#     # Calculate Dynamic Time Warping (DTW) distance
#     dtw_distance, _ = fastdtw(flattened_mfccs1, flattened_mfccs2)

#     # Set a DTW distance threshold (adjust as needed)
#     dtw_threshold = 1000  # Adjust based on your data and requirements

#     # Compare DTW distance to the threshold
#     if dtw_distance <= dtw_threshold:
#         return "DTW distance: {:.2f} - Both voice clips are likely from the same user.".format(dtw_distance)
#     else:
#         return "DTW distance: {:.2f} - Voice clips are likely from different users.".format(dtw_distance)

# if __name__ == '__main__':
#     if len(sys.argv) != 4:
#         print("Usage: python your_python_script.py voice_clip1_path voice_clip2_path dtw_threshold")
#         sys.exit(1)

#     voice_clip1_path = sys.argv[1]
#     voice_clip2_path = sys.argv[2]
#     dtw_threshold = float(sys.argv[3])

#     result = calculate_dtw_distance(voice_clip1_path, voice_clip2_path, dtw_threshold)
#     print(result)






# import sys
# import librosa
# import numpy as np
# from fastdtw import fastdtw

# def extract_mfcc(audio_path):
#     # Load the audio clip
#     audio, _ = librosa.load(audio_path, sr=16000)  # Adjust the sampling rate if needed
#     # Extract MFCCs
#     mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)
#     # Normalize MFCCs
#     mfccs -= (np.mean(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#     mfccs /= (np.std(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#     return mfccs

# def scale_features(features):
#     # Scale features to have zero mean and unit variance
#     mean = np.mean(features, axis=1)
#     std = np.std(features, axis=1)
#     scaled_features = (features - mean[:, np.newaxis]) / (std[:, np.newaxis] + 1e-8)
#     return scaled_features

# # Check if the correct number of command-line arguments is provided
# if len(sys.argv) != 3:
#     print("Usage: python your_script.py <audio_file_path1> <audio_file_path2>")
#     sys.exit(1)

# # Get the audio file paths from the command-line arguments
# audio_path1 = sys.argv[1]
# audio_path2 = sys.argv[2]

# # Extract MFCC features for both audio files
# mfccs1 = extract_mfcc(audio_path1)
# mfccs2 = extract_mfcc(audio_path2)

# # Scale the features
# scaled_mfccs1 = scale_features(mfccs1)
# scaled_mfccs2 = scale_features(mfccs2)

# # Flatten the scaled MFCC features
# flattened_mfccs1 = scaled_mfccs1.flatten()
# flattened_mfccs2 = scaled_mfccs2.flatten()

# # Calculate Dynamic Time Warping (DTW) distance
# dtw_distance, _ = fastdtw(flattened_mfccs1, flattened_mfccs2)

# # Set a DTW distance threshold (adjust as needed)
# dtw_threshold = 1000  # Adjust based on your data and requirements

# # Compare DTW distance to the threshold
# if dtw_distance <= dtw_threshold:
#     print("DTW distance: {:.2f} - Both voice clips are likely from the same user.".format(dtw_distance))
# else:
#     print("DTW distance: {:.2f} - Voice clips are likely from different users.".format(dtw_distance))





# import librosa
# import numpy as np
# from fastdtw import fastdtw

# def extract_mfcc(audio_path):
#     # Load the audio clip
#     audio, _ = librosa.load(audio_path, sr=16000)  # Adjust the sampling rate if needed
#     # Extract MFCCs
#     mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)
#     # Normalize MFCCs
#     mfccs -= (np.mean(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#     mfccs /= (np.std(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#     return mfccs

# def scale_features(features):
#     # Scale features to have zero mean and unit variance
#     mean = np.mean(features, axis=1)
#     std = np.std(features, axis=1)
#     scaled_features = (features - mean[:, np.newaxis]) / (std[:, np.newaxis] + 1e-8)
#     return scaled_features

# # Paths to the two voice clips you want to compare
# voice_clip1_path = "1.wav"  # Replace with your local file path
# voice_clip2_path = "2.wav"  # Replace with your local file path

# # Extract MFCC features for both voice clips
# mfccs1 = extract_mfcc(voice_clip1_path)
# mfccs2 = extract_mfcc(voice_clip2_path)

# # Scale the features
# scaled_mfccs1 = scale_features(mfccs1)
# scaled_mfccs2 = scale_features(mfccs2)

# # Flatten the scaled MFCC features
# flattened_mfccs1 = scaled_mfccs1.flatten()
# flattened_mfccs2 = scaled_mfccs2.flatten()

# # Calculate Dynamic Time Warping (DTW) distance
# dtw_distance, _ = fastdtw(flattened_mfccs1, flattened_mfccs2)

# # Set a DTW distance threshold (adjust as needed)
# dtw_threshold = 1000  # Adjust based on your data and requirements

# # Compare DTW distance to the threshold
# if dtw_distance <= dtw_threshold:
#     print("DTW distance: {:.2f} - Both voice clips are likely from the same user.".format(dtw_distance))
# else:
#     print("DTW distance: {:.2f} - Voice clips are likely from different users.".format(dtw_distance))
