import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.datasets import imdb

# Set seed for reproducibility
tf.random.set_seed(7)  

# Load and preprocess data
top_words = 5000
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=top_words)
max_review_length = 500

X_train = pad_sequences(X_train, maxlen=max_review_length)
X_test = pad_sequences(X_test, maxlen=max_review_length)

# Build the RNN model
embedding_vector_length = 32

model=tf.keras.models.Sequential([
   tf.keras.layers.Embedding(top_words, embedding_vector_length, input_length=max_review_length),
   tf.keras.layers.SimpleRNN(24, return_sequences=False),
   tf.keras.layers.Dense(64, activation='relu'),
   tf.keras.layers.Dense(32, activation='relu'),
   tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Print a summary of the model architecture
model.summary()

early_stop = tf.keras.callbacks.EarlyStopping(monitor='accuracy', mode='min', patience=10)
# Train the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=64,callbacks=[early_stop])

# Evaluate the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1] * 100))

model.save(r"C:\Users\shari\S3\Deep Learning\DL\Assignment\modelrnn.keras")