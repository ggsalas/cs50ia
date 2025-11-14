# Keras to TensorFlow.js Conversion Example

This is a **practical example** of converting a TensorFlow Keras model to run in the browser using TensorFlow.js.

## About the Model

**Traffic Sign Classifier** - A convolutional neural network trained on the GTSRB dataset to recognize 43 different types of traffic signs.

- **Task:** Image classification (traffic signs)
- **Dataset:** GTSRB (German Traffic Sign Recognition Benchmark)
- **Input:** 30×30 RGB images
- **Output:** 43 traffic sign categories (speed limits, stop, yield, etc.)
- **Architecture:** CNN with Conv2D, MaxPooling, Dense layers

## Converting Keras to TensorFlow.js

```bash
# From project root
python src/convert-to-js/manual_convert.py
```

**What it does:**

1. Loads the Keras model (`model1.keras`)
2. Extracts weights with proper TensorFlow.js naming
3. Converts to browser-compatible format
4. Outputs `model.json` + binary weight files

## Why Custom Script?

Official `tensorflowjs_converter` has compatibility issues with modern environments (Python 3.13+, Keras 3, NumPy 2.x). This script handles the conversion manually.

## Using in Browser

```javascript
import * as tf from "@tensorflow/tfjs";

// Load converted model
const model = await tf.loadLayersModel("/model/model.json");

// Classify image
const tensor = tf.browser
  .fromPixels(imageElement)
  .resizeBilinear([30, 30])
  .expandDims(0);
const predictions = await model.predict(tensor);
```

---

This demonstrates the full workflow: **Train in Python → Convert → Deploy in Browser**
