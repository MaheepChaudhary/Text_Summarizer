class Model():
  
  def __init__(self,vocab_size,sent_max_len,valid_sent_max_len,embedding_size):
    self.vocab_size = vocab_size
    self.sent_max_len = sent_max_len
    self.valid_sent_max_len = valid_sent_max_len
    self.embedding_size = embeddding_size

#we will keep 3 lstm layers in encoder network
  def encoder(self):
    input_layer = Input(shape = (self.sent_max_len,))
    embedding_layer = Embedding(self.vocab_size,self.embedding_size,trainable = True)(input_layer)
    lstm1 = LSTM(self.embedding_size)(embedding_layer)
    lstm2 = LSTM(self.embedding_size)(lstm1)
    encoder_output,state_h,state_c = LSTM(self.embedding_size,return_sequences = True,return_states = True)(lstm2)
    return encoder_output,[state_h,state_c]

#we will keep 1 lstm layers in decoder network  
  def decoder(self):
    input_layer = Input(shape = (self.valid_sent_max_len,))
    embedding_layer = Embedding(self.vocab_size,self.embedding_size,trainable=True)(input_layer)
    decoder_output = LSTM(self.embedding_size,return_sequences = True,return_states = True)(embedding_layer)
    return decoder_output

  def attention(self):
    context_arr = []
    alpha_arr,softmax_arr,final_arr = [],[],[]
    for i in self.decoder:
      for j in self.encoder[0]:
        softmax_arr.append(numpy.dot(i,j))
      alpha_arr = np.array(tf.nn.softmax(softmax_arr))
      #after founding softmax then multiplying it with the hidden outputs of encoding layer
      for x,y in zip(arr,softmax_arr):
        final_arr.append(np.dot(x,y))
      h = []
      #concatenating the array
      for f in final_arr:
        if h == []:
          h = f
        else:
          np.add(h,f)           
      context_arr.append(h)
    return context_arr    
  
  def Dense(self):
    final_vector = tf.concat(self.context_arr,self.decoder)
    dense = TimeDistributed(Dense(self.vocab_size,activation = 'softmax'))
    final_output = dense(final_vector)
    return final_output

  def model(self):
    model = Model([self.encoder.input_layer,self.decoder.input_layer],self.Dense)
    return model.summary