export type PredictionResult = {
  predictedClass: number;
  category: string;
  confidence: number;
  top3: Array<{
    category: string;
    confidence: number;
  }>;
};

export type ClassifierState = {
  isLoading: boolean;
  isModelLoaded: boolean;
  error: string | null;
};
