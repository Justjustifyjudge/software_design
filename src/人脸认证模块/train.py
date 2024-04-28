import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Lambda
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras import backend as K
from sklearn.model_selection import train_test_split

# Assume X_positive and X_negative are numpy arrays containing positive and negative face pairs
# y_positive and y_negative are corresponding labels (1 for positive pairs, 0 for negative pairs)

# Split data into training and validation sets
X_train_pos, X_val_pos, y_train_pos, y_val_pos = train_test_split(X_positive, y_positive, test_size=0.2, random_state=42)
X_train_neg, X_val_neg, y_train_neg, y_val_neg = train_test_split(X_negative, y_negative, test_size=0.2, random_state=42)

# Concatenate positive and negative pairs
X_train = np.concatenate([X_train_pos, X_train_neg], axis=0)
y_train = np.concatenate([y_train_pos, y_train_neg], axis=0)
X_val = np.concatenate([X_val_pos, X_val_neg], axis=0)
y_val = np.concatenate([y_val_pos, y_val_neg], axis=0)

# Siamese Network architecture
def create_siamese_network(input_shape):
    input_img = Input(shape=input_shape)
    x = Conv2D(32, (3, 3), activation='relu')(input_img)
    x = MaxPooling2D((2, 2))(x)
    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    output = Dense(1, activation='sigmoid')(x)
    return Model(input_img, output)

input_shape = X_train.shape[1:]
siamese_model = create_siamese_network(input_shape)

# Contrastive loss function for Siamese Network
def contrastive_loss(y_true, y_pred):
    margin = 1
    square_pred = K.square(y_pred)
    margin_square = K.square(K.maximum(margin - y_pred, 0))
    return K.mean(y_true * square_pred + (1 - y_true) * margin_square)

siamese_model.compile(optimizer=Adam(), loss=contrastive_loss, metrics=['accuracy'])

# Training the Siamese Network
siamese_model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_val, y_val))

# Evaluate the model
siamese_model.evaluate(X_val, y_val)
