"""
Manual conversion script that bypasses tensorflowjs CLI compatibility issues.
Uses proper TensorFlow.js weight naming conventions.
"""

import tensorflow as tf
import json
import os
import shutil
import numpy as np


def save_weights_to_json(model, output_dir):
    """Manually save model weights in TensorFlow.js format with correct naming."""

    os.makedirs(output_dir, exist_ok=True)

    # Get all weights
    weights = []
    weight_specs = []

    for layer in model.layers:
        layer_weights = layer.get_weights()
        layer_name = layer.name

        # Skip layers without weights
        if len(layer_weights) == 0:
            continue

        # For each weight in the layer (typically kernel and bias)
        for i, w in enumerate(layer_weights):
            weights.append(w)

            # Use proper TensorFlow.js naming convention
            # kernel (weights) = 0, bias = 1
            if i == 0:
                weight_name = f"{layer_name}/kernel"
            elif i == 1:
                weight_name = f"{layer_name}/bias"
            else:
                weight_name = f"{layer_name}/weight_{i}"

            weight_specs.append(
                {"name": weight_name, "shape": list(w.shape), "dtype": "float32"}
            )

    # Save weights as binary
    weight_data = np.concatenate([w.flatten() for w in weights])
    weight_data = weight_data.astype(np.float32)

    with open(os.path.join(output_dir, "group1-shard1of1.bin"), "wb") as f:
        f.write(weight_data.tobytes())

    # Create model topology
    model_json = {
        "format": "layers-model",
        "generatedBy": "keras-manual-converter",
        "convertedBy": "TensorFlow.js Converter v4.0.0",
        "modelTopology": json.loads(model.to_json()),
        "weightsManifest": [
            {"paths": ["group1-shard1of1.bin"], "weights": weight_specs}
        ],
    }

    # Save model.json
    with open(os.path.join(output_dir, "model.json"), "w") as f:
        json.dump(model_json, f, indent=2)

    return True


def convert_model(keras_path, output_path):
    """Convert Keras model to TensorFlow.js format."""

    print("=" * 60)
    print("Manual Keras to TensorFlow.js Converter")
    print("=" * 60)

    # Load model
    print(f"\n1. Loading Keras model from {keras_path}...")
    try:
        model = tf.keras.models.load_model(keras_path)
        print("✅ Model loaded successfully!")
        model.summary()
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

    # Save to TensorFlow.js format manually
    print(f"\n2. Converting to TensorFlow.js format...")
    print(f"   Output directory: {output_path}")

    try:
        save_weights_to_json(model, output_path)
        print("✅ Conversion successful (using manual method)!")

        # Show output files
        print(f"\n3. Model files created in {output_path}:")
        for file in sorted(os.listdir(output_path)):
            file_path = os.path.join(output_path, file)
            size = os.path.getsize(file_path) / 1024  # KB
            print(f"   - {file} ({size:.2f} KB)")

        print("\n" + "=" * 60)
        print("✅ Conversion completed successfully!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys

    input_model = "src/model1.keras"
    output_dir = "traffic-web-app/public/model"

    if len(sys.argv) >= 2:
        input_model = sys.argv[1]
    if len(sys.argv) >= 3:
        output_dir = sys.argv[2]

    success = convert_model(input_model, output_dir)
    sys.exit(0 if success else 1)
