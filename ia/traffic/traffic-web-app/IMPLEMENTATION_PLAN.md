# Traffic Sign Classifier - Implementation Plan

## Project Overview
Build a web app with offline AI support to detect traffic sign images using TensorFlow.js, converting the existing Keras model to run in the browser.

---

## Phase 1: Setup & Dependencies

### 1.1 Install TensorFlow.js
- [ ] Add `@tensorflow/tfjs` package to dependencies
  ```bash
  npm install @tensorflow/tfjs
  ```

### 1.2 Convert the Keras Model
- [x] Install `tensorflowjs` in Python environment ✅
- [x] Convert `src/model1.keras` to TensorFlow.js format ✅
  ```bash
  # Due to compatibility issues with Python 3.13 and tensorflowjs CLI,
  # used custom conversion script:
  python ../src/manual_convert.py
  ```
- [x] Verify model files created in `public/model/`: ✅
  - `model.json` (8.3 KB)
  - `group1-shard1of1.bin` (9.1 MB)

---

## Phase 2: Clean & Structure the App

### 2.1 Clean Default Vite/React Content
- [ ] Remove unused assets (`vite.svg`, `react.svg`)
- [ ] Clean up `App.tsx` (remove counter example)
- [ ] Update `index.html` title to "Traffic Sign Classifier"
- [ ] Simplify `App.css` and `index.css`

### 2.2 Create Project Structure
```
src/
├── components/
│   ├── ImageUploader.tsx      # File upload + preview component
│   └── PredictionResult.tsx   # Display classification results
├── hooks/
│   └── useTrafficSignClassifier.ts  # TensorFlow.js logic
├── constants/
│   └── categories.ts          # 43 traffic sign categories
├── types/
│   └── index.ts               # TypeScript interfaces
└── App.tsx                    # Main layout
```

- [ ] Create folder structure
- [ ] Create empty files for each component/module

---

## Phase 3: Build Core Features

### 3.1 Define Types and Constants
- [x] Create `src/types/index.ts` with interfaces: ✅
  - PredictionResult interface
  - ClassifierState interface

- [x] Create `src/constants/categories.ts` with all 43 categories ✅
  - All traffic sign categories (0-42)
  - Model dimensions (IMG_WIDTH, IMG_HEIGHT)
  - NUM_CATEGORIES constant

### 3.2 Create Classifier Hook
- [ ] Build `src/hooks/useTrafficSignClassifier.ts`:
  - Load TensorFlow.js model from `/model/model.json`
  - Image preprocessing (resize to 30x30)
  - Prediction function
  - Memory management (dispose tensors)
  - Loading and error states

### 3.3 Build UI Components

#### 3.3.1 ImageUploader Component
- [ ] Create `src/components/ImageUploader.tsx`:
  - File input (accept images)
  - Drag & drop support
  - Image preview
  - Clear/reset functionality

#### 3.3.2 PredictionResult Component
- [ ] Create `src/components/PredictionResult.tsx`:
  - Display top prediction with confidence %
  - Show top 3 predictions
  - Visual confidence indicators
  - Category labels

#### 3.3.3 Main App Component
- [ ] Update `src/App.tsx`:
  - Main layout
  - Integrate ImageUploader
  - Integrate PredictionResult
  - Handle classification flow
  - Loading states
  - Error handling

---

## Phase 4: Polish & Optimization

### 4.1 Styling
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Loading spinner while model loads
- [ ] Error states UI
- [ ] Clean, modern design
- [ ] Accessibility (ARIA labels, keyboard navigation)

### 4.2 Performance Optimization
- [ ] Lazy load TensorFlow.js model
- [ ] Image compression before processing
- [ ] Web Worker for heavy computation (optional)
- [ ] Bundle size optimization

### 4.3 Error Handling
- [ ] Model loading failures
- [ ] Invalid image formats
- [ ] Network errors
- [ ] Browser compatibility checks

### 4.4 Testing
- [ ] Test with sample traffic sign images
- [ ] Cross-browser testing
- [ ] Mobile device testing

---

## Optional Features (Future Enhancements)

### Camera Support (Not in current scope)
- Create `src/components/CameraCapture.tsx`
- Access webcam via `getUserMedia`
- Capture photo button
- Switch between upload and camera modes

### Advanced Features (Not in current scope)
- Batch image processing
- Export prediction results
- Prediction history
- Model performance metrics display
- Dark mode toggle
- Offline support with Service Worker
- Full PWA with install prompt and manifest

---

## Technical Specifications

### Model Details
- **Input**: 30x30 RGB images
- **Output**: 43 categories (traffic signs)
- **Framework**: TensorFlow.js (converted from Keras)

### Browser Requirements
- Modern browsers with WebGL support
- File API support for image upload

### File Size Estimates
- TensorFlow.js library: ~500KB (gzipped)
- Converted model: ~500KB - 2MB (depends on model complexity)
- Total app bundle: ~1-3MB

---

## Development Workflow

1. **Start Development Server**
   ```bash
   npm run dev
   ```

2. **Build for Production**
   ```bash
   npm run build
   ```

3. **Preview Production Build**
   ```bash
   npm run preview
   ```

---

## Implementation Decisions

1. **Camera Support**: ❌ No - File upload only
2. **Design**: Simple/minimal UI
3. **Offline Support**: ❌ No Service Worker - Online only
4. **Sample Images**: ❌ No - User provides their own images

---

## Success Criteria

- ✅ Model converts successfully to TensorFlow.js
- ✅ Web app loads and classifies images
- ✅ Classification accuracy matches Python version
- ✅ Responsive design works on all devices
- ✅ Error handling covers edge cases
- ✅ Performance is acceptable (< 2s for prediction)

---

## Timeline Estimate

- Phase 1 (Setup): 30 minutes
- Phase 2 (Structure): 30 minutes
- Phase 3 (Core Features): 2-3 hours
- Phase 4 (Polish): 1-2 hours

**Total**: 4-6 hours

---

*Last Updated: Thu Nov 13 2025*
