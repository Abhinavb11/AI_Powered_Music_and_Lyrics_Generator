import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.mixed_precision import set_global_policy
import pickle

# Enable mixed precision for faster training on GPU
set_global_policy('mixed_float16')

# Load preprocessed data
print("Loading data...")
X = np.load("X.npy")
y = np.load("y.npy")

with open("note_to_int.pkl", "rb") as f:
    note_to_int = pickle.load(f)

num_classes = len(note_to_int)
print(f"Number of classes: {num_classes}")

# Subsample data (use 10% for faster prototyping)
sample_size = int(0.1 * len(X))
indices = np.random.choice(len(X), sample_size, replace=False)
X = X[indices]
y = y[indices]
print(f"Subsampled data shape: X={X.shape}, y={y.shape}")

# Reshape X if needed (ensure shape is (samples, timesteps, features))
if len(X.shape) == 2:
    X = X.reshape(X.shape[0], X.shape[1], 1)

# Convert y to one-hot encoding
y = to_categorical(y, num_classes=num_classes)
print(f"One-hot y shape: {y.shape}")

# Define simpler LSTM model
model = Sequential([
    LSTM(128, input_shape=(X.shape[1], X.shape[2]), return_sequences=False),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dense(num_classes, activation='softmax', dtype='float32')  # Ensure output is float32
])

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.summary()

# Define early stopping to prevent overtraining
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train model
print("Training model...")
history = model.fit(
    X, y,
    batch_size=128,  # Increased for faster processing
    epochs=20,       # Reduced for faster prototyping
    validation_split=0.2,  # Use 20% for validation
    callbacks=[early_stopping],
    verbose=1
)

# Save model
model.save("melody_model_fast.h5")
print("Model saved to melody_model_fast.h5")

# Save training history for analysis
with open("training_history.pkl", "wb") as f:
    pickle.dump(history.history, f)