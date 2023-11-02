import librosa
import numpy as np
from tensorflow import keras
from IPython.display import Audio
import os  # Import the os module
import json

# Set TensorFlow log level to only display errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load the trained model
model_path = 'pythonModels/intensity/audio_classification_model2.h5'
model = keras.models.load_model(model_path)


def preprocess_voice_clip(audio_clip_path):
    audio, sample_rate = librosa.load(audio_clip_path, duration=10, sr=None)
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13)
    target_length = 260
    if mfccs.shape[1] < target_length:
        mfccs = np.pad(
            mfccs, ((0, 0), (0, target_length - mfccs.shape[1])), mode='constant')
    else:
        mfccs = mfccs[:, :target_length]

    mfccs = mfccs[np.newaxis, ..., np.newaxis]
    return mfccs


def predict_intensity(audio_clip_path):
    processed_clip = preprocess_voice_clip(audio_clip_path)

    # Suppress the progress output line
    predictions = model.predict(processed_clip, verbose=0)
    return predictions


# Example voice clip path on your local machine
voice_clip_path = 'pythonModels/intensity/Normal.mp3'
predictions = predict_intensity(voice_clip_path)

# Convert the predicted class index to intensity level
intensity_levels = ['Voice intensity is high', 'Voice intensity is normal', 'Voice intensity is low']
predicted_intensity = intensity_levels[np.argmax(predictions)]

# print(f"Predicted Intensity: {predicted_intensity}")

result = {
    "predicted_intensity": predicted_intensity,
}

# Convert the result to a JSON string
result_json = json.dumps(result)

# Print the JSON result
print(result_json)




# import librosa
# import numpy as np
# from tensorflow import keras
# from IPython.display import Audio
# import os  # Import the os module

# # Set TensorFlow log level to only display errors
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# # Load the trained model
# model_path = 'audio_classification_model2.h5'
# model = keras.models.load_model(model_path)

# def preprocess_voice_clip(audio_clip_path):
#     audio, sample_rate = librosa.load(audio_clip_path, duration=10, sr=None)
#     mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13)
#     target_length = 260
#     if mfccs.shape[1] < target_length:
#         mfccs = np.pad(mfccs, ((0, 0), (0, target_length - mfccs.shape[1])), mode='constant')
#     else:
#         mfccs = mfccs[:, :target_length]

#     mfccs = mfccs[np.newaxis, ..., np.newaxis]
#     return mfccs

# def predict_intensity(audio_clip_path):
#     processed_clip = preprocess_voice_clip(audio_clip_path)
#     predictions = model.predict(processed_clip)
#     return predictions

# # Example voice clip path on your local machine
# voice_clip_path = '11clip2.mp3'
# predictions = predict_intensity(voice_clip_path)

# # Convert the predicted class index to intensity level
# intensity_levels = ['High', 'Normal', 'Low']
# predicted_intensity = intensity_levels[np.argmax(predictions)]

# print(f"Predicted Intensity: {predicted_intensity}")


# import librosa
# import numpy as np
# from tensorflow import keras
# from IPython.display import Audio  # Note: IPython is typically used in Jupyter or Colab, you might need to use a different approach to play audio in a local environment

# # Load the trained model
# model_path = 'audio_classification_model2.h5'
# model = keras.models.load_model(model_path)

# def preprocess_voice_clip(audio_clip_path):
#     audio, sample_rate = librosa.load(audio_clip_path, duration=10, sr=None)
#     mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13)
#     target_length = 260
#     if mfccs.shape[1] < target_length:
#         mfccs = np.pad(mfccs, ((0, 0), (0, target_length - mfccs.shape[1])), mode='constant')
#     else:
#         mfccs = mfccs[:, :target_length]

#     mfccs = mfccs[np.newaxis, ..., np.newaxis]
#     return mfccs

# def predict_intensity(audio_clip_path):
#     processed_clip = preprocess_voice_clip(audio_clip_path)
#     predictions = model.predict(processed_clip)
#     return predictions

# # Example voice clip path on your local machine
# voice_clip_path = '11clip2.mp3'
# predictions = predict_intensity(voice_clip_path)

# # Convert the predicted class index to intensity level
# intensity_levels = ['High', 'Normal', 'Low']
# predicted_intensity = intensity_levels[np.argmax(predictions)]


# print(f"Predicted Intensity: {predicted_intensity}")
