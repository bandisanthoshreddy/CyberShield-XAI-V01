# 🛡️ CyberShield — Multilingual Cyberbullying Detection using XAI

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
