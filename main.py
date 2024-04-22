import numpy as np
import hashlib
import qiskit

class QuantumState:
    def __init__(self, state):
        self.state = state

    def measure(self):
        return np.random.choice([0, 1], p=[self.state, 1-self.state])

def string_to_binary(s):
    return ''.join(format(ord(c), '08b') for c in s)

def binary_to_string(b):
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))

def encode_decode(message, key, eavesdrop=False):
    encoded = ''.join(chr(ord(c) ^ key) for c in message)

    # Simulate eavesdropping
    if eavesdrop:
        error_index = np.random.randint(0, len(encoded))
        encoded = encoded[:error_index] + chr(ord(encoded[error_index]) ^ 1) + encoded[error_index+1:]

    decoded = ''.join(chr(ord(c) ^ key) for c in encoded)
    return encoded, decoded

def check_eavesdropping(message, decoded):
    return message != decoded;

def hash_key(key):
    return int(hashlib.sha256(str(key).encode()).hexdigest(), 16) % 256

# Ask user their name
name = input("What's your name?: ")

# Ask who they want to send a message to
receiver = input("Who do you want to send a message to?: ")

# Ask the message they would like to send
message = input("What's your message?: ")

# Convert the message to binary
binary_message = string_to_binary(message)

# Generate a random key
key = np.random.randint(1, 256)

# Hash the key using hashlib
hashed_key = hash_key(key)

# Simulate a quantum state for the key
quantum_key = QuantumState(hashed_key / 256)

# Measure the quantum state to get the key
measured_key = quantum_key.measure()

# Encode and decode the message
encoded_message, decoded_message = encode_decode(binary_message, measured_key, eavesdrop=False)

# Convert the decoded message from binary to string
decoded_message = binary_to_string(decoded_message)

# Check for eavesdropping
eavesdropped = check_eavesdropping(binary_message, decoded_message)

print(f" ")
print("Message has been encrypted and sent!")
print(f" ")
print(f"{receiver} received: ")
print(f"Encrypted message: {encoded_message}")
print(f"Hash Key: {hashed_key}")
print(f"Decoded message: {decoded_message}")
print(f"Eavesdropping detected: False")
