import { useState, useEffect, useCallback } from 'react';
import * as tf from '@tensorflow/tfjs';
import { CATEGORIES, IMG_WIDTH, IMG_HEIGHT } from '../constants/categories';
import type { PredictionResult, ClassifierState } from '../types/index.ts';

export function useTrafficSignClassifier() {
  const [state, setState] = useState<ClassifierState>({
    isLoading: true,
    isModelLoaded: false,
    error: null,
  });
  
  const [model, setModel] = useState<tf.LayersModel | null>(null);

  // Load model on component mount
  useEffect(() => {
    loadModel();
  }, []);

  async function loadModel() {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));
      
      console.log('Loading TensorFlow.js model...');
      const loadedModel = await tf.loadLayersModel('/model/model.json');
      
      console.log('Model loaded successfully!');
      setModel(loadedModel);
      
      setState({
        isLoading: false,
        isModelLoaded: true,
        error: null,
      });
    } catch (error) {
      console.error('Error loading model:', error);
      setState({
        isLoading: false,
        isModelLoaded: false,
        error: error instanceof Error ? error.message : 'Failed to load model',
      });
    }
  }

  /**
   * Classify a traffic sign image
   * @param imageElement - HTML image element to classify
   * @returns Prediction result with top prediction and top 3 predictions
   */
  const classifyImage = useCallback(
    async (imageElement: HTMLImageElement): Promise<PredictionResult> => {
      if (!model) {
        throw new Error('Model not loaded');
      }

      // Use tf.tidy to automatically clean up intermediate tensors
      return tf.tidy(() => {
        // 1. Convert image to tensor and preprocess
        // fromPixels creates a tensor from the image
        const tensor = tf.browser
          .fromPixels(imageElement)
          .resizeBilinear([IMG_WIDTH, IMG_HEIGHT]) // Resize to 30x30
          .expandDims(0) // Add batch dimension: [1, 30, 30, 3]
          .toFloat(); // Convert to float32

        // 2. Run prediction
        const predictions = model.predict(tensor) as tf.Tensor;
        
        // 3. Get prediction data as array
        const predictionData = predictions.dataSync();
        
        // 4. Find the predicted class (highest probability)
        const predictedClass = predictions.argMax(-1).dataSync()[0];
        const confidence = predictionData[predictedClass] * 100;

        // 5. Get top 3 predictions
        // Create array of {index, probability} objects
        const predictionArray = Array.from(predictionData).map((prob, index) => ({
          index,
          prob,
        }));

        // Sort by probability descending and take top 3
        const top3 = predictionArray
          .sort((a, b) => b.prob - a.prob)
          .slice(0, 3)
          .map(({ index, prob }) => ({
            category: CATEGORIES[index],
            confidence: prob * 100,
          }));

        // 6. Return result
        return {
          predictedClass,
          category: CATEGORIES[predictedClass],
          confidence,
          top3,
        };
      });
    },
    [model]
  );

  return {
    ...state,
    classifyImage,
  };
}
