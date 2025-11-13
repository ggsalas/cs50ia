"""
Convert Keras model to TensorFlow.js format.
This script works around numpy compatibility issues.
"""

import tensorflow as tf
import sys
import os

# Workaround for numpy compatibility
import numpy as np

if not hasattr(np, "object"):
    np.object = object
if not hasattr(np, "bool"):
    np.bool = bool

try:
    import tensorflowjs as tfjs
except ImportError:
    print("Error: tensorflowjs not installed")
    print("Install with: pip install tensorflowjs")
    sys.exit(1)


def convert_model(input_path, output_path):
    """Convert Keras model to TensorFlow.js format."""

    # Check if input model exists
    if not os.path.exists(input_path):
        print(f"Error: Model file not found at {input_path}")
        sitys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    print(f"Loading Keras model from {input_path}...")
    try:
        model = tf.keras.models.load_model(input_path)
        print("Model loaded successfully!")
        print(f"Model summary:")
        model.summary()
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

    print(f"\nConverting to TensorFlow.js format...")
    print(f"Output directory: {output_path}")

    try:
        tfjs.converters.save_keras_model(model, output_path)
        print("\n✅ Conversion successful!")
        print(f"Model files saved to: {output_path}")
        print("\nFiles created:")
        for file in os.listdir(output_path):
            file_path = os.path.join(output_path, file)
            size = os.path.getsize(file_path) / 1024  # KB
            print(f"  - {file} ({size:.2f} KB)")
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Default paths
    input_model = "src/model1.keras"
    output_dir = "traffic-web-app/public/model"

    # Allow command line arguments
    if len(sys.argv) >= 2:
        input_model = sys.argv[1]
    if len(sys.argv) >= 3:
        output_dir = sys.argv[2]

    print("=" * 60)
    print("Keras to TensorFlow.js Model Converter")
    print("=" * 60)

    convert_model(input_model, output_dir)
