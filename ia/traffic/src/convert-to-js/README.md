# Keras to TensorFlow.js Model Conversion Guide

This directory contains scripts to convert Keras models to TensorFlow.js format for use in web applications.

## Quick Start

```bash
# Convert the traffic sign model (from project root)
python src/convert-to-js/manual_convert.py

# Convert a custom model
python src/convert-to-js/manual_convert.py path/to/your/model.keras path/to/output/directory
```

## Why This Custom Script?

The official `tensorflowjs_converter` CLI tool has compatibility issues with:
- Python 3.13
- NumPy 2.x
- Keras 3.x
- TensorFlow 2.20+

Our custom conversion script (`manual_convert.py`) handles all these compatibility issues automatically.

## Available Scripts

### 1. `manual_convert.py` (Recommended)

**Primary conversion script with full compatibility.**

**Usage:**
```bash
python src/convert-to-js/manual_convert.py [input_model] [output_dir]
```

**Default paths:**
- Input: `src/model1.keras`
- Output: `traffic-web-app/public/model`

**Examples:**
```bash
# Use default paths (from project root)
python src/convert-to-js/manual_convert.py

# Convert specific model to specific directory
python src/convert-to-js/manual_convert.py models/my_model.keras web/public/tfjs_model

# Convert from absolute path
python src/convert-to-js/manual_convert.py /home/user/models/model.keras ./output
```

**Output:**
- `model.json` - Model architecture and metadata
- `group1-shard1of1.bin` - Model weights (or multiple shards for large models)

### 2. `convert_via_savedmodel.py`

**Alternate method using TensorFlow SavedModel intermediate format.**

Useful if you need to debug conversion issues or need the SavedModel format.

```bash
python src/convert-to-js/convert_via_savedmodel.py [input_model] [output_dir]
```

### 3. `convert_model.py`

**Legacy script with numpy compatibility workarounds.**

Use this if you encounter issues with the other scripts.

```bash
python src/convert-to-js/convert_model.py [input_model] [output_dir]
```

## Model Requirements

Your Keras model must be:
- ✅ Saved in `.keras` or `.h5` format
- ✅ A Sequential or Functional API model
- ✅ Using standard Keras layers

**Note:** Custom layers or Lambda layers may require additional conversion steps.

## Output Format

The conversion creates a **TensorFlow.js Layers Model** with:

```
 oqtoutput_directory/
├── model.json          # Model architecture, metadata, and weight manifest
└── group1-shard*.bin   # Binary weight files
```

### model.json structure:
- `format`: Always "layers-model"
- `modelTopology`: Keras model architecture in JSON
- `weightsManifest`: Paths and metadata for weight files

## Using the Converted Model in JavaScript

### Loading the model:

```javascript
import * as tf from '@tensorflow/tfjs';

// Load the model
const model = await tf.loadLayersModel('/model/model.json');

// Make predictions
const inputTensor = tf.browser.fromPixels(imageElement)
    .resizeBilinear([30, 30])
    .expandDims(0)
    .toFloat();

const predictions = await model.predict(inputTensor);
```

See the main project documentation for complete usage examples.

## Troubleshooting

### Error: "Module 'numpy' has no attribute 'object'"

**Solution:** The script automatically patches this. If you still see it, the tensorflowjs package needs updating:

```bash
pip install --upgrade tensorflowjs
```

Or manually patch:
```bash
# Already handled by manual_convert.py
```

### Error: "Expected Keras version 2; got Keras version 3"

**Solution:** This is why `manual_convert.py` exists. It handles Keras 3 compatibility automatically by using manual weight extraction.

### Error: "tensorflow.compat.v1' has no attribute 'estimator'"

**Solution:** The script mocks tensorflow_hub to bypass this issue. No action needed.

### Large model files (>100MB)

If your model is very large, the conversion will automatically split weights into multiple shard files:
- `group1-shard1of2.bin`
- `group1-shard2of2.bin`
- etc.

This is normal and TensorFlow.js will load them automatically.

### Model not loading in browser

**Check:**
1. ✅ Files are in `/public` directory (for Vite/React apps)
2. ✅ Path in `loadLayersModel()` is correct
3. ✅ Model files are being served (check Network tab)
4. ✅ CORS headers allow loading (if from different origin)

## Environment Setup

### Required packages:

```bash
pip install tensorflow tensorflowjs
```

### Current environment (used for this project):
- Python 3.13.7
- TensorFlow 2.20.0
- Keras 3.11.3
- NumPy 2.2.6
- tensorflowjs 3.18.0+ (patched)

## Model Information

### Traffic Sign Classifier Model:

**Architecture:**
- Input: 30x30x3 RGB images
- Conv2D: 32 filters, 3x3 kernel
- MaxPooling2D: 3x3 pool size
- Flatten
- Dense: 900 units
- Dropout: 0.5
- Dense (Output): 43 units (traffic sign categories)

**Size:**
- Total parameters: 2,373,339 trainable (9.05 MB)
- Converted model: ~9.1 MB

**Performance:**
- Expected prediction time: < 100ms in modern browsers
- WebGL acceleration: Automatic

## Advanced Usage

### Convert with specific quantization:

```bash
# The manual script doesn't support quantization yet
# For production, consider using the official converter after fixing dependencies
```

### Batch conversion:

```bash
for model in models/*.keras; do
    output_name=$(basename "$model" .keras)
    python src/convert-to-js/manual_convert.py "$model" "output/tfjs/$output_name"
done
```

### Verify conversion:

```bash
# Check output files exist
ls -lh traffic-web-app/public/model/

# Verify model.json is valid JSON
python -m json.tool traffic-web-app/public/model/model.json > /dev/null && echo "Valid JSON"
```

## Contributing

If you improve the conversion scripts or find workarounds for compatibility issues, please document them here.

## References

- [TensorFlow.js Official Docs](https://www.tensorflow.org/js)
- [Model Conversion Guide](https://www.tensorflow.org/js/guide/conversion)
- [TensorFlow.js Layers Model Format](https://github.com/tensorflow/tfjs/blob/master/tfjs-layers/src/keras_format/types.ts)

---

**Last Updated:** November 13, 2025  
**Compatibility:** Python 3.13+, TensorFlow 2.20+, Keras 3.x
