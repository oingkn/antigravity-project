# Final Project: Neural Network Application

> **AI Programming 101 — Final Project**
> Submission deadline: **end of Week 12**

---

## 🎯 Objectives

The final project challenges students to design, implement, train, and evaluate a **deep learning model** for a problem of their choosing. Students will:

1. Identify a real-world problem suited to deep learning
2. Collect or source an appropriate dataset
3. Design and implement a neural network architecture in PyTorch
4. Train with best practices (regularisation, learning-rate scheduling, early stopping)
5. Evaluate rigorously and compare against a classical ML baseline
6. *Optionally* deploy the model as an accessible application

---

## 🧩 Project Tracks

Choose one of the following tracks:

### Track 1 — Image Classification / Object Detection
- Build a CNN (or fine-tune a pre-trained ResNet / EfficientNet) to classify images
- Suggested datasets: CIFAR-10, Food-101, custom scraped dataset (≥ 5 classes)

### Track 2 — Text Classification / Sentiment Analysis
- Build an MLP over TF-IDF features **and** a fine-tuned DistilBERT model; compare results
- Suggested datasets: IMDB Reviews, AG News, custom social-media dataset

### Track 3 — Tabular Regression / Classification with MLP
- Design a deep MLP for a challenging tabular dataset not covered in lectures
- Must outperform a Random Forest baseline
- Suggested datasets: any Kaggle competition dataset (check terms of use)

### Track 4 — Open Track (Instructor Approval Required)
- Generative models, time-series forecasting, reinforcement learning, etc.
- Submit a one-page project proposal by **end of Week 8**

---

## 📋 Requirements

### 1 · Problem Definition & Dataset (10 pts)

- [ ] Clearly state the problem and why deep learning is appropriate
- [ ] Describe the dataset: size, source, class balance (or target distribution)
- [ ] Implement a reproducible data-loading script or notebook section
- [ ] Show exploratory visualisations (class distribution, sample images/texts, statistics)

### 2 · Data Pipeline & Augmentation (10 pts)

- [ ] Build a proper `Dataset` / `DataLoader` using PyTorch
- [ ] Apply at least **2 data augmentation / preprocessing** techniques
  - Images: random crop, horizontal flip, colour jitter, normalisation, etc.
  - Text: lower-casing, tokenisation, padding/truncation, etc.
  - Tabular: feature scaling, synthetic oversampling (SMOTE), etc.
- [ ] Verify augmentations with visualised examples

### 3 · Model Architecture (20 pts)

- [ ] Implement the model as a `torch.nn.Module` subclass
- [ ] Justify your architectural choices (layer sizes, depth, activation functions)
- [ ] Include at least **one regularisation technique** (Dropout, BatchNorm, weight decay)
- [ ] Print the model summary and total parameter count

### 4 · Training (20 pts)

- [ ] Use **mini-batch gradient descent** with an appropriate optimiser (Adam recommended)
- [ ] Apply a **learning-rate scheduler** (StepLR, CosineAnnealing, or ReduceLROnPlateau)
- [ ] Implement **early stopping** based on validation loss
- [ ] Plot training loss and validation metric vs epoch

### 5 · Evaluation & Baseline Comparison (20 pts)

- [ ] Evaluate on a held-out test set
- [ ] Report all relevant metrics:
  - Classification: accuracy, F1-macro, confusion matrix, ROC-AUC (if binary)
  - Regression: MAE, RMSE, R²
- [ ] Train a **classical ML baseline** (Random Forest or Gradient Boosting) on the same data
- [ ] Compare deep model vs baseline in a table and analyse the difference

### 6 · Report & Presentation (20 pts)

- [ ] Submit a **4-page PDF report** (IEEE or ACM two-column format is fine):
  - Abstract (½ page)
  - Introduction & motivation
  - Data & methods
  - Results & analysis
  - Conclusion & future work
- [ ] Prepare a **7-minute live demo or recorded video**:
  - Walk through the notebook
  - Show model predictions on 3–5 new/unseen examples
  - Discuss one thing that surprised you and one limitation of your model

---

## 🚀 Bonus Opportunities (up to +15 pts)

| Bonus Task | Points |
|-----------|--------|
| Deploy the model as a web app (Gradio, Streamlit, or FastAPI + Dockerfile) | +5 |
| Try **transfer learning** (fine-tune a pre-trained backbone) | +5 |
| Publish your training code to a public GitHub repo with a proper README | +3 |
| Achieve competitive performance on a public Kaggle leaderboard | +2 |

---

## 🗂️ Deliverables

Submit a single `.zip` archive via the course portal:

```
<student_id>_final/
├── notebook.ipynb         # Complete, fully-executed notebook
├── report.pdf             # 4-page PDF report
├── demo_video.mp4         # (or link in README)
├── model.pt               # Saved model weights (torch.save)
├── requirements.txt       # All dependencies with pinned versions
└── README.md              # Quick-start instructions
```

---

## 🏆 Grading Rubric

| Section | Points |
|---------|--------|
| Problem Definition & Dataset | 10 |
| Data Pipeline & Augmentation | 10 |
| Model Architecture | 20 |
| Training | 20 |
| Evaluation & Baseline Comparison | 20 |
| Report & Presentation | 20 |
| **Total** | **100** |

Bonus points may bring your total above 100 but will be capped at **110**.

---

## 📆 Project Timeline

| Date | Milestone |
|------|-----------|
| End of Week 8 | Track selection (+ proposal for Track 4) |
| End of Week 9 | Dataset loaded, EDA complete |
| End of Week 10 | Baseline model trained and evaluated |
| End of Week 11 | Deep model trained; ablation study done |
| End of Week 12 | Final submission + presentations |

---

## 💡 Tips

- **Start early.** Training deep networks can take hours — leave enough time.
- **Version-control your code.** Push to GitHub after each meaningful change.
- **Use `torch.save` / `torch.load`** to checkpoint your model so you don't have to retrain from scratch.
- **Ask for help.** Office hours exist for a reason!
- A model that *barely* beats the baseline but is *well understood and well explained* scores better than a mysterious model with unexplained high accuracy.
