import type { PredictionResult as PredictionResultType } from '../types/index.ts';
import './PredictionResult.css';

interface PredictionResultProps {
  result: PredictionResultType | null;
  isLoading?: boolean;
}

export function PredictionResult({ result, isLoading = false }: PredictionResultProps) {
  if (isLoading) {
    return (
      <div className="prediction-result loading">
        <div className="spinner"></div>
        <p>Classifying image...</p>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <div className="prediction-result">
      <div className="main-prediction">
        <h2>Predicted Sign</h2>
        <div className="prediction-card primary">
          <p className="category">{result.category}</p>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${result.confidence}%` }}
            ></div>
          </div>
          <p className="confidence-text">{result.confidence.toFixed(2)}% confident</p>
        </div>
      </div>

      <div className="top-predictions">
        <h3>Top 3 Predictions</h3>
        <div className="predictions-list">
          {result.top3.map((prediction, index) => (
            <div key={index} className="prediction-card">
              <div className="prediction-header">
                <span className="rank">{index + 1}</span>
                <span className="category">{prediction.category}</span>
              </div>
              <div className="confidence-bar small">
                <div
                  className="confidence-fill"
                  style={{ width: `${prediction.confidence}%` }}
                ></div>
              </div>
              <p className="confidence-text small">
                {prediction.confidence.toFixed(2)}%
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
