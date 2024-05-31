import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model  # type: ignore
from tensorflow.keras.layers import Input, LSTM, Dense  # type: ignore
from data import data
from generate_react_native_component import generate_react_native_component

# Data Preparation
input_texts = [item[0] for item in data]
target_texts = ["\n" + item[1] + "\n" for item in data]

input_characters = sorted(list(set("".join(input_texts))))
target_characters = sorted(list(set("".join(target_texts))))

num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)

max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])

input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])

encoder_input_data = np.zeros(
    (len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype="float32"
)
decoder_input_data = np.zeros(
    (len(target_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32"
)
decoder_target_data = np.zeros(
    (len(target_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32"
)

for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    for t, char in enumerate(input_text):
        encoder_input_data[i, t, input_token_index[char]] = 1.0
    for t, char in enumerate(target_text):
        decoder_input_data[i, t, target_token_index[char]] = 1.0
        if t > 0:
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.0

# Model Building
latent_dim = 512

encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]

decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm1 = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_lstm2 = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm1(decoder_inputs, initial_state=encoder_states)
decoder_outputs, _, _ = decoder_lstm2(decoder_outputs)
decoder_dense = Dense(num_decoder_tokens, activation="softmax")
decoder_outputs = decoder_dense(decoder_outputs)

model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Model Training
model.compile(optimizer="rmsprop", loss="categorical_crossentropy")
model.fit(
    [encoder_input_data, decoder_input_data],
    decoder_target_data,
    batch_size=60,
    epochs=10,
    validation_split=0.2,
)

# Encoder model
encoder_model = Model(encoder_inputs, encoder_states)

# Decoder model
decoder_state_input_h = Input(shape=(latent_dim,))
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

decoder_outputs, state_h, state_c = decoder_lstm1(
    decoder_inputs, initial_state=decoder_states_inputs
)
decoder_outputs, state_h, state_c = decoder_lstm2(
    decoder_outputs, initial_state=[state_h, state_c]
)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)

decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states
)


def decode_sequence(input_seq):
    states_value = encoder_model.predict(input_seq)

    target_seq = np.zeros((1, 1, num_decoder_tokens), dtype="float32")
    target_seq[0, 0, target_token_index["\n"]] = 1.0

    stop_condition = False
    decoded_sentence = ""
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = target_characters[sampled_token_index]

        decoded_sentence += sampled_char

        if sampled_char == "\n" or len(decoded_sentence) > max_decoder_seq_length:
            stop_condition = True

        target_seq = np.zeros((1, 1, num_decoder_tokens), dtype="float32")
        target_seq[0, 0, sampled_token_index] = 1.0
        states_value = [h, c]

    return decoded_sentence.strip()


test_input_text = "create a function to add two numbers"
test_input_data = np.zeros(
    (1, max_encoder_seq_length, num_encoder_tokens), dtype="float32"
)
for t, char in enumerate(test_input_text):
    test_input_data[0, t, input_token_index[char]] = 1.0

js_code = decode_sequence(test_input_data)
print(
    "Generated JavaScript code:\n", js_code
)  # Add this line to print the JavaScript code
react_native_code = generate_react_native_component()
print("Generated React Native component:\n", react_native_code)

# Directory path for saving files
directory_path = "output/"
os.makedirs(directory_path, exist_ok=True)  # Create the directory if it doesn't exist

# File paths
js_file_name = "generated_code.js"
js_file_path = os.path.join(directory_path, js_file_name)

react_native_file_name = "generated_component.js"
react_native_file_path = os.path.join(directory_path, react_native_file_name)

# Save generated JavaScript code
with open(js_file_path, "w") as js_file:
    js_file.write(js_code)

# Save generated React Native component
with open(react_native_file_path, "w") as rn_file:
    rn_file.write(react_native_code)

print("JavaScript code saved to:", js_file_path)
print("React Native component saved to:", react_native_file_path)
