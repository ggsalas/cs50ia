export interface PredictionResult {
  predictedClass: number;
  category: string;
  confidence: number;
  top3: Array<{
    category: string;
    confidence: number;
  }>;
}

export interface ClassifierState {
  isLoading: boolean;
  isModelLoaded: boolean;
  error: string | null;
}
