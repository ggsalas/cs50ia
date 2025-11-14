import { useState } from "react";
import { ImageUploader } from "./components/ImageUploader";
import { PredictionResult } from "./components/PredictionResult";
import { useTrafficSignClassifier } from "./hooks/useTrafficSignClassifier";
import type { PredictionResult as PredictionResultType } from "./types/index.ts";
import "./App.css";

function App() {
  const { isLoading, isModelLoaded, error, classifyImage } =
    useTrafficSignClassifier();
  const [result, setResult] = useState<PredictionResultType | null>(null);
  const [isClassifying, setIsClassifying] = useState(false);

  const handleImageSelect = async (image: HTMLImageElement) => {
    if (!isModelLoaded) {
      alert("Model is still loading. Please wait...");
      return;
    }

    try {
      setIsClassifying(true);
      setResult(null);

      const prediction = await classifyImage(image);
      setResult(prediction);
    } catch (error) {
      console.error("Classification error:", error);
      alert("Error classifying image. Please try again.");
    } finally {
      setIsClassifying(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Traffic Sign Classifier</h1>
        <p>Upload a traffic sign image to classify it using AI</p>

        {isLoading && (
          <div className="status loading">
            <div className="spinner-small"></div>
            <span>Loading AI model...</span>
          </div>
        )}

        {error && (
          <div className="status error">
            <span>⚠️ Error: {error}</span>
          </div>
        )}

        {isModelLoaded && !isLoading && (
          <div className="status success">
            <span>✓ Model ready</span>
          </div>
        )}
      </header>

      <main>
        <ImageUploader
          onImageSelect={handleImageSelect}
          disabled={!isModelLoaded || isClassifying}
        />

        <PredictionResult result={result} isLoading={isClassifying} />
      </main>

      <footer>
        <p>Model trained on GTSRB dataset • 43 traffic sign categories</p>
      </footer>
    </div>
  );
}

export default App;
