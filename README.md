🛡️ CyberShield — Multilingual Cyberbullying Detection using XAI

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?style=flat-square&logo=fastapi)
![HuggingFace](https://img.shields.io/badge/Model-MuRIL-orange?style=flat-square&logo=huggingface)
![XAI](https://img.shields.io/badge/XAI-SHAP%20%7C%20LIME%20%7C%20Attention-purple?style=flat-square)
![Languages](https://img.shields.io/badge/Languages-English%20%7C%20Hindi%20%7C%20Telugu-red?style=flat-square)

> A senior design project that detects cyberbullying across **English, Hindi, and Telugu** social media text using a fine-tuned **MuRIL transformer**, with full **Explainable AI (XAI)** — showing *why* each prediction was made using SHAP, LIME, and Attention visualisation.

---

## 🌐 Live Demo

![CyberShield Demo](docs/demo.png)

---

## ✨ Features

- 🔍 **Multilingual detection** — English, Hindi (Devanagari + Romanized), Telugu (native + code-mixed)
- 🤖 **MuRIL transformer** — Google's BERT model purpose-built for Indian languages, fine-tuned on cyberbullying data
- 💡 **3 XAI methods** — Attention heatmaps, LIME feature importance, SHAP Shapley values
- 🏷️ **5 categories** — Not Bullying, Insult, Threat, Hate Speech, Harassment
- ⚡ **REST API** — FastAPI backend with `/api/predict` and `/api/batch` endpoints
- 🎨 **Full web UI** — Dark-themed dashboard with real-time XAI visualisations
- 📦 **Batch analysis** — Analyse up to 50 comments at once

---

## 🏗️ Architecture
Raw Text (EN / HI / TE)
↓
Language Detection + IndicNLP Normalisation
↓
MuRIL Transformer (fine-tuned)
↓
┌──────────────────────────────┐
│  Label + Confidence Score    │
│  not_bullying / insult /     │
│  threat / hate_speech /      │
│  harassment                  │
└──────────────────────────────┘
↓
XAI Explainability Layer
├── Attention Heatmap
├── LIME (local perturbation)
└── SHAP (Shapley values)
↓
Prevention Action
├── Warn poster
├── Flag for review
└── Auto-remove (high severity)

---

## 🚀 Quick Start

### Run the demo (no training needed)

```bash
git clone https://github.com/YOUR_USERNAME/CyberShield-XAI.git
cd CyberShield-XAI/cybershield_demo
pip install fastapi "uvicorn[standard]"
python app.py
```

Open **http://localhost:8000** in your browser.

### Train the full model

```bash
pip install -r requirements.txt

# 1. Prepare data (place datasets in data/raw/)
python ml/1_data_preparation.py

# 2. Fine-tune MuRIL
python ml/2_model_training.py

# 3. Launch with real model
cd website && uvicorn app:app --reload --port 8000
```

---

## 📁 Project Structure
CyberShield-XAI/
│
├── cybershield_demo/          # ← Start here (demo, no GPU needed)
│   ├── app.py                 # FastAPI backend with mock model
│   ├── index.html             # Full frontend (CSS + JS embedded)
│   └── setup_and_run.py      # One-click launcher
│
├── ml/
│   ├── 1_data_preparation.py  # Load, clean, split EN/HI/TE datasets
│   ├── 2_model_training.py    # Fine-tune MuRIL with Focal Loss
│   └── 3_xai_explainer.py    # SHAP, LIME, Attention XAI module
│
├── website/
│   ├── app.py                 # Production FastAPI backend
│   ├── templates/index.html   # Main HTML page
│   └── static/               # CSS + JS assets
│
├── data/
│   ├── raw/                   # Place downloaded datasets here
│   └── processed/             # Auto-generated train/val/test splits
│
├── models/
│   └── cyberbullying_detector/ # Saved MuRIL model after training
│
├── requirements.txt
└── README.md

---

## 🗃️ Datasets

| Language | Dataset | Source |
|----------|---------|--------|
| English | Cyberbullying Classification | [Kaggle](https://www.kaggle.com/datasets/andrewmvd/cyberbullying-classification) |
| English | Hate Speech & Offensive Language | [Kaggle](https://www.kaggle.com/datasets/mrmorj/hate-speech-and-offensive-language-dataset) |
| Hindi | HASOC 2019/2020 Hindi Track | [HASOC](https://hasocfire.github.io/hasoc/2020/dataset.html) |
| Hindi | Hindi-English Code-Mixed | [Bohra et al. 2018](https://www.semanticscholar.org/paper/A-Dataset-of-Hindi-English-Code-Mixed-Social-Media-Bohra-Vijay/69faa9008a9933518217c152b5c63c84122cb67b) |
| Telugu | HOLD-Telugu @ DravidianLangTech 2024 | [ACL Anthology](https://aclanthology.org/2024.dravidianlangtech-1.8/) |
| Telugu | Telugu Code-Mixed Hate Speech | [Kaggle](https://www.kaggle.com/datasets/saipanda9/telugu-codemixed-hate-speech) |

---

## 🧠 Model Details

| Component | Details |
|-----------|---------|
| Base model | `google/muril-base-cased` |
| Parameters | 236M |
| Max sequence length | 128 tokens |
| Loss function | Focal Loss (γ=2.0) + class weights |
| Optimizer | AdamW with warmup |
| Training | 5 epochs, early stopping |

---

## 📊 XAI Methods

| Method | Type | What it shows |
|--------|------|---------------|
| **Attention** | Built-in | Which tokens the model focused on |
| **LIME** | Black-box | Which words locally changed the prediction |
| **SHAP** | Black-box | Exact Shapley attribution per token |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Model | HuggingFace Transformers, PyTorch |
| XAI | SHAP, LIME, Attention extraction |
| Backend | FastAPI, Uvicorn |
| Frontend | HTML5, CSS3, Vanilla JS |
| Data processing | pandas, scikit-learn, IndicNLP |

---

## 📌 Labels

| Label | Description | Example |
|-------|-------------|---------|
| `not_bullying` | Safe / benign content | "Have a great day!" |
| `insult` | Personal attacks, name-calling | "You are so stupid" |
| `threat` | Physical or psychological threats | "I will hurt you" |
| `hate_speech` | Content targeting group identity | "These people are enemies" |
| `harassment` | Repeated offensive targeting | "I'll follow you everywhere" |

---

## 👨‍💻 Author

Bandi Santhosh Reddy — Senior Design Project  
VIT-AP University  

---

## 📄 License

MIT License — free to use for academic and research purposes.
