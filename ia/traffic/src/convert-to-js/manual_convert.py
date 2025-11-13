"""
Manual conversion script that bypasses tensorflowjs CLI compatibility issues.
"""

import tensorflow as tf
import json
import os
import shutil
import numpy as np


def save_weights_to_json(model, output_dir):
    """Manually save model weights in TensorFlow.js format."""

    os.makedirs(output_dir, exist_ok=True)

    # Get all weights
    weights = []
    weight_specs = []

    for layer in model.layers:
        layer_weights = layer.get_weights()
        for i, w in enumerate(layer_weights):
            weights.append(w)
            weight_specs.append(
                {
                    "name": f"{layer.name}/weight_{i}",
                    "shape": list(w.shape),
                    "dtype": str(w.dtype),
                }
            )

    # Save weights as binary
    weight_data = np.concatenate([w.flatten() for w in weights])
    weight_data = weight_data.astype(np.float32)

    with open(os.path.join(output_dir, "group1-shard1of1.bin"), "wb") as f:
        f.write(weight_data.tobytes())

    # Create model topology
    model_json = {
        "format": "layers-model",
        "generatedBy": "manual-converter",
        "convertedBy": "TensorFlow.js Converter v1.0.0",
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
        # Try using the official API first (might work despite import issues)
        try:
            # Monkey-patch to fix tensorflow_hub issue
            import sys

            if "tensorflow_hub" in sys.modules:
                del sys.modules["tensorflow_hub"]

            # Temporarily mock tensorflow_hub to bypass the import
            import importlib
            import types

            mock_hub = types.ModuleType("tensorflow_hub")
            sys.modules["tensorflow_hub"] = mock_hub

            import tensorflowjs as tfjs

            tfjs.converters.save_keras_model(model, output_path)
            print("✅ Conversion successful (using official API)!")

        except Exception as e:
            print(f"   Official API failed: {e}")
            print("   Trying manual conversion...")

            # Fall back to manual conversion
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
