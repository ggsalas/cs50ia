"""
Convert Keras model to TensorFlow.js format via SavedModel.
This approach bypasses tensorflowjs compatibility issues.
"""

import tensorflow as tf
import os
import json
import shutil


def convert_model(keras_path, output_path):
    """Convert Keras model to TensorFlow.js format."""

    # Check if input model exists
    if not os.path.exists(keras_path):
        print(f"Error: Model file not found at {keras_path}")
        return False

    print("=" * 60)
    print("Keras to TensorFlow.js Model Converter")
    print("=" * 60)

    # Load the Keras model
    print(f"\n1. Loading Keras model from {keras_path}...")
    try:
        model = tf.keras.models.load_model(keras_path)
        print("✅ Model loaded successfully!")
        print("\nModel summary:")
        model.summary()
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

    # Create temp directory for SavedModel
    temp_dir = "temp_saved_model"
    print(f"\n2. Saving as TensorFlow SavedModel to {temp_dir}...")
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        # For Keras 3, use export instead of save for SavedModel format
        model.export(temp_dir)
        print("✅ SavedModel created successfully!")
    except Exception as e:
        print(f"❌ Error creating SavedModel: {e}")
        return False

    # Now use tensorflowjs converter command line
    print(f"\n3. Converting to TensorFlow.js format...")
    print(f"   Output directory: {output_path}")

    import subprocess

    try:
        # Create output directory
        os.makedirs(output_path, exist_ok=True)

        # Run tensorflowjs_converter
        cmd = [
            "tensorflowjs_converter",
            "--input_format=tf_saved_model",
            temp_dir,
            output_path,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Conversion failed:")
            print(result.stderr)
            return False

        print("✅ Conversion successful!")

    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False
    finally:
        # Cleanup temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"\n4. Cleaned up temporary files")

    # Show output files
    print(f"\n5. Model files created in {output_path}:")
    for file in sorted(os.listdir(output_path)):
        file_path = os.path.join(output_path, file)
        size = os.path.getsize(file_path) / 1024  # KB
        print(f"   - {file} ({size:.2f} KB)")

    print("\n" + "=" * 60)
    print("✅ Conversion completed successfully!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    import sys

    # Default paths
    input_model = "src/model1.keras"
    output_dir = "traffic-web-app/public/model"

    # Allow command line arguments
    if len(sys.argv) >= 2:
        input_model = sys.argv[1]
    if len(sys.argv) >= 3:
        output_dir = sys.argv[2]

    success = convert_model(input_model, output_dir)
    sys.exit(0 if success else 1)
