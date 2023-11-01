# hard code code correct voice-------------------------------
import librosa
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import cosine
import json


def extract_mfcc(audio_path, target_length=None):
    try:
        # Load the audio clip
        # Adjust the sampling rate if needed
        audio, _ = librosa.load(audio_path, sr=16000)

        if target_length is not None:
            # Pad or truncate the audio to the target length
            if len(audio) > target_length:
                audio = audio[:target_length]
            else:
                audio = np.pad(
                    audio, (0, target_length - len(audio)), 'constant')

        # Extract MFCCs
        mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)
        # Normalize MFCCs
        mfccs -= (np.mean(mfccs, axis=1)[:, np.newaxis] + 1e-8)
        mfccs /= (np.std(mfccs, axis=1)[:, np.newaxis] + 1e-8)
        return mfccs.tolist()  # Convert to a JSON-serializable format
    except Exception as e:
        return str(e)



# Paths to the two voice clips you want to compare
voice_clip1_path = "pythonModels/identify/1.wav"
voice_clip2_path = "pythonModels/identify/2.wav"

# Specify a common target length for MFCCs (adjust as needed)
target_length = 10000  # You can adjust this based on your requirements


# Extract MFCC features for both voice clips with a common target length
mfccs1 = extract_mfcc(voice_clip1_path, target_length=target_length)
mfccs2 = extract_mfcc(voice_clip2_path, target_length=target_length)

# Calculate Dynamic Time Warping (DTW) distance for the original MFCC features
dtw_distance, _ = fastdtw(mfccs1, mfccs2, dist=cosine)

# Set the DTW distance threshold (adjust based on your data and requirements)
dtw_threshold = 100  # Adjust as needed

# Prepare the result as a JSON object with condition output
if dtw_distance <= dtw_threshold:
    comparison_result = "Same user detected."
else:
    comparison_result = "Different user detected."

result = {
    "DTW_distance": dtw_distance,
    "comparison_result": comparison_result,
}

# Convert the result to a JSON string
result_json = json.dumps(result)

# Print the JSON result
print(result_json)












# ------------------base64 correct code for audio.not blob---------------------------------------
# import librosa
# import numpy as np
# from fastdtw import fastdtw
# from scipy.spatial.distance import cosine
# import json
# import base64

# def extract_mfcc(audio_path, target_length=None):
#     try:
#         # Load the audio clip
#         # Adjust the sampling rate if needed
#         audio, _ = librosa.load(audio_path, sr=16000)

#         if target_length is not None:
#             # Pad or truncate the audio to the target length
#             if len(audio) > target_length:
#                 audio = audio[:target_length]
#             else:
#                 audio = np.pad(
#                     audio, (0, target_length - len(audio)), 'constant')

#         # Extract MFCCs
#         mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)
#         # Normalize MFCCs
#         mfccs -= (np.mean(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#         mfccs /= (np.std(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#         return mfccs.tolist()  # Convert to a JSON-serializable format
#     except Exception as e:
#         return str(e)

# def audio_to_base64(audio_path):
#     try:
#         with open(audio_path, "rb") as audio_file:
#             audio_bytes = audio_file.read()
#             base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
#         return base64_audio
#     except Exception as e:
#         return str(e)

# # Paths to the two voice clips you want to compare
# voice_clip1_path = "src/pythonModels/identify/1.wav"
# voice_clip2_path = "src/pythonModels/identify/4.wav"

# # Convert audio clips to base64
# base64_audio1 = audio_to_base64(voice_clip1_path)
# base64_audio2 = audio_to_base64(voice_clip2_path)

# # You can now use base64_audio1 and base64_audio2 as needed in your code.

# # Specify a common target length for MFCCs (adjust as needed)
# target_length = 10000  # You can adjust this based on your requirements

# # Extract MFCC features for both voice clips with a common target length
# mfccs1 = extract_mfcc(voice_clip1_path, target_length=target_length)
# mfccs2 = extract_mfcc(voice_clip2_path, target_length=target_length)

# # Calculate Dynamic Time Warping (DTW) distance for the original MFCC features
# dtw_distance, _ = fastdtw(mfccs1, mfccs2, dist=cosine)

# # Set the DTW distance threshold (adjust based on your data and requirements)
# dtw_threshold = 100  # Adjust as needed

# # Prepare the result as a JSON object with condition output
# if dtw_distance <= dtw_threshold:
#     comparison_result = "Same user detected."
# else:
#     comparison_result = "Different user detected."

# result = {
#     "DTW_distance": dtw_distance,
#     "comparison_result": comparison_result,
#     "base64_audio1": base64_audio1,
#     "base64_audio2": base64_audio2,
# }

# # Convert the result to a JSON string
# result_json = json.dumps(result)

# # Print the JSON result
# print(result_json)









# import librosa
# import numpy as np
# from fastdtw import fastdtw
# from scipy.spatial.distance import cosine

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
# voice_clip1_path = "src/pythonModels/identify/1.wav"
# voice_clip2_path = "src/pythonModels/identify/2.wav"

# # Extract MFCC features for both voice clips
# mfccs1 = extract_mfcc(voice_clip1_path)
# mfccs2 = extract_mfcc(voice_clip2_path)

# # Scale the features
# scaled_mfccs1 = scale_features(mfccs1)
# scaled_mfccs2 = scale_features(mfccs2)

# # Calculate Dynamic Time Warping (DTW) distance for the original MFCC features
# dtw_distance, _ = fastdtw(scaled_mfccs1.T, scaled_mfccs2.T, dist=cosine)

# # Set the DTW distance threshold (adjust based on your data and requirements)
# dtw_threshold = 100  # Adjust as needed

# # Compare the DTW distance to the threshold
# if dtw_distance <= dtw_threshold:
#     print("DTW distance: {:.2f} - Both voice clips are likely from the same user.".format(dtw_distance))
# else:
#     print("DTW distance: {:.2f} - Voice clips are likely from different users.".format(dtw_distance))


# import librosa
# import numpy as np
# from fastdtw import fastdtw
# from scipy.spatial.distance import cosine
# import json

# def extract_mfcc(audio_path):
#     try:
#         # Load the audio clip
#         audio, _ = librosa.load(audio_path, sr=16000)  # Adjust the sampling rate if needed
#         # Extract MFCCs
#         mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)
#         # Normalize MFCCs
#         mfccs -= (np.mean(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#         mfccs /= (np.std(mfccs, axis=1)[:, np.newaxis] + 1e-8)
#         return mfccs.tolist()  # Convert to a JSON-serializable format
#     except Exception as e:
#         return str(e)

# def scale_features(features):
#     # Scale features to have zero mean and unit variance
#     mean = np.mean(features, axis=1)
#     std = np.std(features, axis=1)
#     scaled_features = (features - mean[:, np.newaxis]) / (std[:, np.newaxis] + 1e-8)
#     return scaled_features.tolist()  # Convert to a JSON-serializable format

# # Paths to the two voice clips you want to compare
# voice_clip1_path = "src/pythonModels/identify/2.wav"
# voice_clip2_path = "src/pythonModels/identify/3.wav"

# # Extract MFCC features for both voice clips
# mfccs1 = extract_mfcc(voice_clip1_path)
# mfccs2 = extract_mfcc(voice_clip2_path)

# # Scale the features
# scaled_mfccs1 = scale_features(mfccs1)
# scaled_mfccs2 = scale_features(mfccs2)

# # Calculate Dynamic Time Warping (DTW) distance for the original MFCC features
# dtw_distance, _ = fastdtw(scaled_mfccs1, scaled_mfccs2, dist=cosine)

# # Set the DTW distance threshold (adjust based on your data and requirements)
# dtw_threshold = 10  # Adjust as needed

# # Prepare the result as a JSON object with condition output
# if dtw_distance <= dtw_threshold:
#     comparison_result = "Both voice clips are likely from the same user."
# else:
#     comparison_result = "Voice clips are likely from different users."

# result = {
#     "DTW_distance": dtw_distance,
#     "comparison_result": comparison_result,
# }

# # Convert the result to a JSON string
# result_json = json.dumps(result)

# # Print the JSON result
# print(result_json)
