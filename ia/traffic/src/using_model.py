"""
Traffic sign classifier using a trained neural network model.

This module loads a pre-trained Keras model and uses it to classify
traffic signs from images based on the GTSRB dataset categories.
"""

import sys
import cv2
import numpy as np
import tensorflow as tf

IMG_WIDTH = 30
IMG_HEIGHT = 30

# Traffic sign categories (based on GTSRB dataset)
CATEGORIES = {
    0: "Speed limit (20km/h)",
    1: "Speed limit (30km/h)",
    2: "Speed limit (50km/h)",
    3: "Speed limit (60km/h)",
    4: "Speed limit (70km/h)",
    5: "Speed limit (80km/h)",
    6: "End of speed limit (80km/h)",
    7: "Speed limit (100km/h)",
    8: "Speed limit (120km/h)",
    9: "No passing",
    10: "No passing for vehicles over 3.5 metric tons",
    11: "Right-of-way at the next intersection",
    12: "Priority road",
    13: "Yield",
    14: "Stop",
    15: "No vehicles",
    16: "Vehicles over 3.5 metric tons prohibited",
    17: "No entry",
    18: "General caution",
    19: "Dangerous curve to the left",
    20: "Dangerous curve to the right",
    21: "Double curve",
    22: "Bumpy road",
    23: "Slippery road",
    24: "Road narrows on the right",
    25: "Road work",
    26: "Traffic signals",
    27: "Pedestrians",
    28: "Children crossing",
    29: "Bicycles crossing",
    30: "Beware of ice/snow",
    31: "Wild animals crossing",
    32: "End of all speed and passing limits",
    33: "Turn right ahead",
    34: "Turn left ahead",
    35: "Ahead only",
    36: "Go straight or right",
    37: "Go straight or left",
    38: "Keep right",
    39: "Keep left",
    40: "Roundabout mandatory",
    41: "End of no passing",
    42: "End of no passing by vehicles over 3.5 metric tons",
}


def main():
    """
    Load a trained model and classify a traffic sign from an image.

    Reads model path and image path from command-line arguments,
    loads the model, processes the image, and displays predictions
    with confidence scores.
    """
    # Check command-line arguments
    if len(sys.argv) != 3:
        sys.exit("Usage: python using_model.py model.keras image_path")

    model_path = sys.argv[1]
    image_path = sys.argv[2]

    # Load the trained model
    print(f"Loading model from {model_path}...")
    try:
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully!")
    except (OSError, IOError, ValueError) as e:
        sys.exit(f"Error loading model: {e}")

    # Load and preprocess the image
    print(f"\nLoading image from {image_path}...")
    img = cv2.imread(image_path)

    if img is None:
        sys.exit(f"Error: Could not load image from {image_path}")

    # Resize image to match model input
    img_resized = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

    # Add batch dimension and normalize
    img_array = np.array([img_resized])

    # Make prediction
    print("Making prediction...\n")
    predictions = model.predict(img_array)

    # Get the predicted class
    predicted_class = int(np.argmax(predictions[0]))
    confidence = predictions[0][predicted_class] * 100

    # Display results
    print("=" * 60)
    print(f"Predicted Sign: {CATEGORIES[predicted_class]}")
    print(f"Category Number: {predicted_class}")
    print(f"Confidence: {confidence:.2f}%")
    print("=" * 60)

    # Show top 3 predictions
    print("\nTop 3 Predictions:")
    top_3_indices = np.argsort(predictions[0])[-3:][::-1]
    for i, idx in enumerate(top_3_indices, 1):
        print(f"{i}. {CATEGORIES[int(idx)]}: {predictions[0][idx] * 100:.2f}%")


if __name__ == "__main__":
    main()
