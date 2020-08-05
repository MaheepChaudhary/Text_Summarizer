from model import LSTM_Model

mod = LSTM_Model(vocab_size = 122630, sent_max_len = 50, valid_sent_max_len = 50, embedding_size = 100)
model = mod.encoder_decoder()
print(model.summary())

