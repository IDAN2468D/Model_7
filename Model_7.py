import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense
from data import data

# הכנת הנתונים והאינדקסים
input_texts = [item[0] for item in data]
target_texts = ["\n" + item[1] + "\n" for item in data]  # הוספת תו התחלה וסיום

input_characters = set("".join(input_texts))
target_characters = set("".join(target_texts))
input_characters = sorted(list(input_characters))
target_characters = sorted(list(target_characters))

input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])

max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])

num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)

# הכנת המידע לאימון המודל
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

# בניית המודל
latent_dim = 512  # הגדלת מספר הנוירונים

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

# אימון המודל
model.compile(optimizer="rmsprop", loss="categorical_crossentropy")
model.fit(
    [encoder_input_data, decoder_input_data],
    decoder_target_data,
    batch_size=50,
    epochs=10,  # הגדלת מספר האפוקים
    validation_split=0.2,
)

# בניית המודל ל-encoder
encoder_model = Model(encoder_inputs, encoder_states)

# בניית המודל ל-decoder
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
    # השימוש באינדקס המקסימלי של התווים במקום בתוכן עצמו
    # כדי להוסיף את התו המיוחד '\n' לקוד שנוצר
    states_value = encoder_model.predict(input_seq)

    # השימוש בתו המיוחד '\t' כתו ההתחלה במקום '\n'
    target_seq = np.zeros((1, 1, num_decoder_tokens), dtype="float32")
    target_seq[0, 0, target_token_index["\n"]] = 1.0  # שימוש בתו המיוחד '\t' להתחלה

    stop_condition = False
    decoded_sentence = ""
    while not stop_condition:
        # חישוב הפלט, המצבים והקוד שנוצר
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        # קבלת התו המובחר מתוך האותיות האפשריות
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = target_characters[sampled_token_index]

        # הוספת התו לשורה שנוצרת
        decoded_sentence += sampled_char

        # בדיקה האם הגענו לתו הסיום '\n' או שהשורה ארוכה מדי
        if sampled_char == "\n" or len(decoded_sentence) > max_decoder_seq_length:
            stop_condition = True

        # עדכון המצבים עבור הלולאה הבאה
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
print("Generated JavaScript code:\n", js_code)

directory_path = "js/"
file_name = "generated_code.js"
file_path = directory_path + file_name

with open(file_path, "w") as file:
    for input_text, output_text in data:
        file.write("// Input: " + input_text + "\n")
        file.write(output_text + "\n\n")
encoder_lstm_params = (num_encoder_tokens * latent_dim * 4) + (latent_dim * 2)
decoder_lstm_params = (num_decoder_tokens * latent_dim * 4) + (latent_dim * 2)
dense_params = num_decoder_tokens * latent_dim
total_params = encoder_lstm_params + decoder_lstm_params + dense_params

# הדפסת תוצאות החישובים
print("Number of parameters in encoder LSTM:", encoder_lstm_params)
print("Number of parameters in decoder LSTM:", decoder_lstm_params)
print("Number of parameters in final Dense layer:", dense_params)
print("Total number of parameters in the model:", total_params)
