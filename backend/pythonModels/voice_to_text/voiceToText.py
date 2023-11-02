import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Function to preprocess the voice clip


def preprocess_voice_clip(file_path):
    frame_length = 256
    frame_step = 160
    fft_length = 384

    audio_binary = tf.io.read_file(file_path)
    audio, _ = tf.audio.decode_wav(audio_binary)
    audio = tf.squeeze(audio, axis=-1)
    audio = tf.cast(audio, tf.float32)

    spectrogram = tf.signal.stft(
        audio, frame_length=frame_length, frame_step=frame_step, fft_length=fft_length
    )
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.math.pow(spectrogram, 0.5)
    means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
    stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
    spectrogram = (spectrogram - means) / (stddevs + 1e-10)

    return spectrogram

# Function to decode predictions


def decode_probabilities(probabilities, num_to_char):
    decoded_text = ""
    for timestep in probabilities[0]:
        # Get the index with maximum probability
        predicted_label = np.argmax(timestep)
        decoded_text += str(predicted_label) + ', '
    return decoded_text


# Load the saved model
saved_model_path = 'final_model.h5'
model = load_model(saved_model_path, compile=False)

# Function to predict on voice input


def predict_from_audio_file(file_path, model):
    preprocessed_data = preprocess_voice_clip(file_path)

    predictions = model(preprocessed_data)
    print("Predicted Data Before Decoding:", predictions)

    num_to_char = {0: '', 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm', 14: 'n',
                   15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z', 27: "'", 28: '?', 29: '!', 30: ' '}
    predicted_text = decode_probabilities(predictions, num_to_char)
    print("Predicted Text After Decoding:", predicted_text)

    return predicted_text


# Provide the path to your audio file
audio_file_path = 'voice12_converted.wav'  # Replace with your audio file path

predicted_text = predict_from_audio_file(audio_file_path, model)
print("Final Predicted Text:", predicted_text)

if __name__ == "__main__":
    import sys
    audio_file_path = sys.argv[1]
    recognized_text = predict_from_audio_file(audio_file_path, model)
    print(recognized_text)


# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import load_model
# import pyaudio

# # Function to preprocess the voice clip
# def preprocess_voice_clip(audio):
#     frame_length = 256
#     frame_step = 160
#     fft_length = 384

#     audio = tf.squeeze(audio, axis=-1)
#     audio = tf.cast(audio, tf.float32)

#     spectrogram = tf.signal.stft(
#         audio, frame_length=frame_length, frame_step=frame_step, fft_length=fft_length
#     )
#     spectrogram = tf.abs(spectrogram)
#     spectrogram = tf.math.pow(spectrogram, 0.5)
#     means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
#     stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
#     spectrogram = (spectrogram - means) / (stddevs + 1e-10)

#     return spectrogram

# # Function to decode predictions
# def decode_probabilities(probabilities, num_to_char):
#     decoded_text = ""
#     for timestep in probabilities[0]:
#         predicted_label = np.argmax(timestep)  # Get the index with maximum probability
#         decoded_text += str(predicted_label) + ', '
#     return decoded_text

# # Load the saved model
# saved_model_path = 'final_model.h5'
# model = load_model(saved_model_path, compile=False)

# # Function to predict on voice input
# def predict_voice_input(model):
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 16000
#     CHUNK = 1024

#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

#     print("Listening...")

#     frames = []
#     for i in range(0, int(RATE / CHUNK * 5)):  # Adjust the duration of listening
#         data = stream.read(CHUNK)
#         frames.append(np.frombuffer(data, dtype=np.int16))

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     audio_data = np.hstack(frames)
#     audio_tensor = tf.constant(audio_data, dtype=tf.float32)
#     audio_tensor = tf.expand_dims(audio_tensor, axis=0)
#     audio_tensor = tf.expand_dims(audio_tensor, axis=-1)

#     preprocessed_data = preprocess_voice_clip(audio_tensor)

#     predictions = model(preprocessed_data)
#     print("Predicted Data Before Decoding:", predictions)

#     num_to_char = {0: '', 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z', 27: "'", 28: '?', 29: '!', 30: ' '}
#     predicted_text = decode_probabilities(predictions, num_to_char)
#     print("Predicted Text After Decoding:", predicted_text)

#     return predicted_text

# predicted_text = predict_voice_input(model)
# print("Final Predicted Text:", predicted_text)
