# YouTube Sentiment Pipeline: Real-Time Voice of Customer (VoC) Engine

An enterprise-grade NLP pipeline designed to extract, analyze, and process natural language feedback from streaming multimedia and digital marketplace URLs. This framework transitions product development and retention workflows from reactive bug-hunting to proactive, ROI-driven strategic roadmapping by computing high-precision sentiment matrices.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://abei-sentimentanalysis.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Core Architecture & Features

This system bypasses traditional unweighted keyword indexing by deploying a hybrid rule/lexicon-based Natural Language Processing framework.

- **Dual-Engine NLP Analytics:** Integrates **VADER (Valence Aware Dictionary and sEntiment Reasoner)** for micro-intensity nuance tracking (optimized for social colloquialisms, slang, and syntax variations) alongside **TextBlob** for robust baseline polarity screening.
- **Dynamic Split-Screen UI:** A low-latency executive dashboard layout featuring multi-variant intelligence inputs, high-visibility interactive KPI metrics, and contextual pulse trackers.
- **Visual Trend Analytics:** Renders data distribution trends using automated continuous area mapping to trace consumer sentiment densities over linear data streams.
- **Data Audit Trail System:** Built-in administrative debugging panel featuring transparent raw scoring, data-frame indexing, and exhaustive dataset export options.
- **Automated Infrastructure Keep-Alive:** Implements a headless GitHub Actions engine performing scheduled cron telemetry requests every 12 hours to eliminate server sleep latency and guarantee 100% active operational runtime.

---

## 🛠️ Technology Stack

- **Interface & Dashboard Engine:** Streamlit (Forced CSS inject configurations for high-contrast UI components and zero-overlap layouts)
- **Data Ingestion & Transformation Matrices:** Pandas, NumPy
- **Natural Language Orchestration:** `vaderSentiment`, `textblob`
- **Automation Pipeline:** GitHub Actions Core (Ubuntu Ingestion Runtime Engine)

---

## 📦 Project Structure

```text
├── .github/
│   └── workflows/
│       └── keep_alive.yml     # Automated 12-hour cron app ping framework
├── app.py                     # Core analytical logic layer and Streamlit UI code
├── requirements.txt           # Ironclad baseline package dependencies
└── README.md                  # System documentation
