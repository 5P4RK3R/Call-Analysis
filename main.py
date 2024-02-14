# import streamlit as st
import numpy as np
import io
# Beat tracking example
import librosa
# import matlab.engine
import matplotlib.pyplot as plt
from Core import dsp
# # Start MATLAB engine
# eng = matlab.engine.start_matlab()

# # Call ViSQOL function
# result = eng.visqol('audio.mp4', 'audio.mp4')

# # Process ViSQOL results
# print("ViSQOL Score:", result)

# # Stop MATLAB engine
# eng.quit()

# 1. Get the file path to an included audio example
# filename = librosa.example('nutcracker')


# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
# y, sr = librosa.load("audio.mp4")

# # # 3. Run the default beat tracker
# # tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
# fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
# D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
# img = librosa.display.specshow(D, y_axis='linear', x_axis='time',
#                                sr=sr, ax=ax[0])
# ax[0].set(title='Linear-frequency power spectrogram')
# ax[0].label_outer()

# hop_length = 1024
# D = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop_length)),
#                             ref=np.max)
# librosa.display.specshow(D, y_axis='log', sr=sr, hop_length=hop_length,
#                          x_axis='time', ax=ax[1])
# ax[1].set(title='Log-frequency power spectrogram')
# ax[1].label_outer()
# fig.colorbar(img, ax=ax, format="%+2.f dB")
# y_harm, y_perc = librosa.effects.hpss(y)
# librosa.display.waveshow(y_harm, sr=sr, alpha=0.5, ax=ax[0], label='Harmonic')
# librosa.display.waveshow(y_perc, sr=sr, color='r', alpha=0.5, ax=ax[0], label='Percussive')
# ax[0].set(title='Multiple waveforms')
# ax[0].legend()
# # fig.colorbar(img, ax=ax, format="%+2.f dB")
# plt.savefig('frequency power spectrogram.png')  # Save the figure as a PNG file

# print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
# st.title('My First Streamlit App')

# # Add a slider widget
# x = st.slider('Select a value', 0, 100)

# # Generate random data based on the slider value
# data = np.random.randn(x, 2)

# # Plot the data
# st.write(data)
# import os

# from visqol import visqol_lib_py
# from visqol.pb2 import visqol_config_pb2
# from visqol.pb2 import similarity_result_pb2

# config = visqol_config_pb2.VisqolConfig()

# mode = "audio"
# if mode == "audio":
#     config.audio.sample_rate = 48000
#     config.options.use_speech_scoring = False
#     svr_model_path = "libsvm_nu_svr_model.txt"
# elif mode == "speech":
#     config.audio.sample_rate = 16000
#     config.options.use_speech_scoring = True
#     svr_model_path = "lattice_tcditugenmeetpackhref_ls2_nl60_lr12_bs2048_learn.005_ep2400_train1_7_raw.tflite"
# else:
#     raise ValueError(f"Unrecognized mode: {mode}")

# config.options.svr_model_path = os.path.join(
#     os.path.dirname(visqol_lib_py.__file__), "model", svr_model_path)

# api = visqol_lib_py.VisqolApi()

# api.Create(config)

# similarity_result = api.Measure(reference, degraded)

# print(similarity_result.moslqo)
import streamlit as st
st.title("Compare Audio Files")

# Title for the app
# st.title("File Uploader Example")
col1 = st.columns(1,gap="large")

# with col1:
fileA = hash("fileA")

# File uploader component
uploaded_file = st.file_uploader("Upload a file",key=fileA, type=['mp3', 'wav'])

# Check if file is uploaded
if uploaded_file is not None:
    # Display file details
    file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)
    audio_bytes = None
    if uploaded_file.type == 'audio/wav':
        # For audio files
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format='audio/wav')
    elif uploaded_file.type == 'audio/mp4':
        # For audio files
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format='audio/mp4')
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)

    # # Display audio waveform
    # st.subheader("Audio Waveform")
    # st.audio(audio_bytes, format='audio/wav')

    # Display audio duration
    # duration = librosa.get_duration(y=y, sr=sr)
    # st.write(f"Duration: {duration:.2f} seconds")
    # processor = dsp.DSP()
    # snr= processor.snr(y=y)
    # if snr:
    #     st.write("Signal-to-Noise Ratio (SNR): {:.2f} dB".format(snr))
    # fig, ax = plt.subplots()
    # s = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
    #                             fmax=8000)
    # S_dB = librosa.power_to_db(s, ref=np.max)
    # img = librosa.display.specshow(S_dB, x_axis='time',
    #                         y_axis='mel', sr=sr,
    #                         fmax=8000, ax=ax)
    # fig.colorbar(img, ax=ax, format='%+2.0f dB')
    # ax.set(title='Mel-frequency spectrogram')
    # st.pyplot(fig)


    # And compute the spectrogram magnitude and phase
    S_full, phase = librosa.magphase(librosa.stft(y))
    idx = slice(*librosa.time_to_frames([10, 15], sr=sr))
    fig, ax = plt.subplots()
    img = librosa.display.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max),
                            y_axis='log', x_axis='time', sr=sr, ax=ax)
    fig.colorbar(img, ax=ax)
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, y_axis='linear', x_axis='time',
                                sr=sr, ax=ax[0])
    ax[0].set(title='Linear-frequency power spectrogram')
    ax[0].label_outer()

    hop_length = 1024
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop_length)),
                                ref=np.max)
    librosa.display.specshow(D, y_axis='log', sr=sr, hop_length=hop_length,
                            x_axis='time', ax=ax[1])
    ax[1].set(title='Log-frequency power spectrogram')
    ax[1].label_outer()
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    st.pyplot(fig)
    harmonic, percussive = librosa.effects.hpss(y)
    # librosa.output.write_wav("vocals.wav", harmonic, sr)
    # librosa.output.write_wav("accompaniment.wav", percussive, sr)

# with col2:
#     fileB = hash("fileB")
#     # File uploader component
#     uploaded_file = st.file_uploader("Upload a file",key=fileB, type=['mp3', 'wav'])
#     audio_bytes = None
#     # Check if file is uploaded
#     if uploaded_file is not None:
#         # Display file details
#         file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
#         st.write(file_details)
        
#         if uploaded_file.type == 'audio/wav':
#             # For audio files
#             audio_bytes = uploaded_file.read()
#             st.audio(audio_bytes, format='audio/wav')
#         elif uploaded_file.type == 'audio/mp4':
#             # For audio files
#             audio_bytes = uploaded_file.read()
#             st.audio(audio_bytes, format='audio/mp4')
#         y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
        

#         # # Display audio waveform
#         # st.subheader("Audio Waveform")
#         # st.audio(audio_bytes, format='audio/wav')

#         # Display audio duration
#         duration = librosa.get_duration(y=y, sr=sr)
#         st.write(f"Duration: {duration:.2f} seconds")

#         processor = dsp.DSP()
#         snr= processor.snr(y=y)
#         if snr:
#             st.write("Signal-to-Noise Ratio (SNR): {:.2f} dB".format(snr))
#         librosa.feature.melspectrogram(y=y, sr=sr)
#         fig, ax = plt.subplots()
#         s = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
#                                     fmax=8000)
#         S_dB = librosa.power_to_db(s, ref=np.max)
#         img = librosa.display.specshow(S_dB, x_axis='time',
#                                 y_axis='mel', sr=sr,
#                                 fmax=8000, ax=ax)
#         fig.colorbar(img, ax=ax, format='%+2.0f dB')
#         ax.set(title='Mel-frequency spectrogram')
#         st.pyplot(fig)



#         # And compute the spectrogram magnitude and phase
#         S_full, phase = librosa.magphase(librosa.stft(y))
#         idx = slice(*librosa.time_to_frames([10, 15], sr=sr))
#         fig, ax = plt.subplots()
#         img = librosa.display.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max),
#                                 y_axis='log', x_axis='time', sr=sr, ax=ax)
#         fig.colorbar(img, ax=ax)
#         fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
#         D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
#         img = librosa.display.specshow(D, y_axis='linear', x_axis='time',
#                                     sr=sr, ax=ax[0])
#         ax[0].set(title='Linear-frequency power spectrogram')
#         ax[0].label_outer()

#         hop_length = 1024
#         D = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop_length)),
#                                     ref=np.max)
#         librosa.display.specshow(D, y_axis='log', sr=sr, hop_length=hop_length,
#                                 x_axis='time', ax=ax[1])
#         ax[1].set(title='Log-frequency power spectrogram')
#         ax[1].label_outer()
#         fig.colorbar(img, ax=ax, format="%+2.f dB")
#         st.pyplot(fig)


# st.page_link("Core/dsp.py", label="Home", icon="🏠")
# # st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
# # st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣", disabled=True)
# # st.page_link("http://www.google.com", label="Google", icon="🌎")