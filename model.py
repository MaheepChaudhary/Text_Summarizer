from config import * 


class LSTM_Model():
  
  def __init__(self,vocab_size,sent_max_len,valid_sent_max_len,embedding_size):
    self.vocab_size = vocab_size
    self.sent_max_len = sent_max_len
    self.valid_sent_max_len = valid_sent_max_len
    self.embedding_size = embedding_size

#we will keep 3 lstm layers in encoder network
  def encoder_decoder(self):

    input_layer_encoder = Input(shape=(self.sent_max_len,)) 
    enc_emb = Embedding(self.vocab_size, self.embedding_size,trainable=True)(input_layer_encoder) 

    #LSTM 1 
    encoder_lstm1 = LSTM(self.embedding_size,return_sequences=True,return_state=True) 
    encoder_output1, state_h1, state_c1 = encoder_lstm1(enc_emb) 

    #LSTM 2 
    encoder_lstm2 = LSTM(self.embedding_size,return_sequences=True,return_state=True) 
    encoder_output2, state_h2, state_c2 = encoder_lstm2(encoder_output1) 

    #LSTM 3 
    encoder_lstm3=LSTM(self.embedding_size, return_state=True, return_sequences=True) 
    encoder_outputs, state_h, state_c= encoder_lstm3(encoder_output2) 
    '''
    input_layer_encoder = Input(shape = (self.sent_max_len,))
    print(input_layer_encoder.shape)
    print(self.vocab_size)
    embedding_layer = Embedding(self.vocab_size,self.embedding_size,trainable = True)(input_layer_encoder)
    print("The shape of the embedding layer is ",embedding_layer.shape)
    lstm1 = LSTM(self.embedding_size)(embedding_layer)
    print("The shape of thge LSTM layer is ",lstm1.shape)
    lstm2 = LSTM(self.embedding_size)(lstm1)
    print(lstm2.shape)
    encoder_output,state_h,state_c = LSTM(self.embedding_size,return_sequences = True, return_states = True)(lstm2)
    
    input_layer = Input(shape = (self.valid_sent_max_len,))
    embedding_layer = Embedding(self.vocab_size,self.embedding_size,trainable=True)(input_layer)
    decoder_output,_,_ = LSTM(self.embedding_size,return_sequences = True,return_state = True)(embedding_layer)
    model = Model([input_layer_encoder,input_layer],self.Dense)
    '''
    input_layer = Input(shape=(None,)) 
    dec_emb_layer = Embedding(self.vocab_size, self.embedding_size,trainable=True) 
    dec_emb = dec_emb_layer(input_layer) 

    #LSTM using encoder_states as initial state
    decoder_lstm = LSTM( self.embedding_size, return_sequences=True, return_state=True) 
    decoder_outputs,decoder_fwd_state, decoder_back_state = decoder_lstm(dec_emb,initial_state=[state_h, state_c]) 
    print(tensorflow.shape(decoder_outputs))
    print("attetnion model startting")
    context_arr = []
    alpha_arr,softmax_arr,final_arr = [],[],[]
    print("1st loop starting")
    for i in decoder_outputs:
      print("2nd loop starting")
      for j in encoder_outputs:
        softmax_arr.append(numpy.dot(i,j))
      alpha_arr = np.array(tf.nn.softmax(softmax_arr))
      #after founding softmax then multiplying it with the hidden outputs of encoding layer
      final_arr = alpha_arr*softmax_arr
      h = []
      #concatenating the array
      for f in final_arr:
        if h == []:
          h = f
        else:
          np.add(h,f)           
      context_arr.append(h)    
    print(np.array(context_arr).shape)
    print(np.array(decoder_ouputs).shape)
    final_vector = tf.concat(concat_dim=1,values = [context_arr,decoder_outputs])
    print("the shape of the final_vector",np.array(final_vector).shape)
    dense = TimeDistributed(Dense(self.vocab_size,activation = 'softmax'))
    final_output = dense(decoder_outputs)
    #final_output = dense(final_vector)

    model = Model([input_layer_encoder,input_layer],final_output)
    return model
  

       
  

  