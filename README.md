# 🛡️ Guardian AI  
### AI-Powered Grooming Detection System for Online Safety

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![NLP](https://img.shields.io/badge/NLP-Transformers-orange)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![Status](https://img.shields.io/badge/Project-Proof%20of%20Concept-purple)

---

## 📖 Overview

Guardian AI is an AI-powered safety system designed to detect potential **online grooming behaviours** before they escalate into exploitation.

The system uses **Natural Language Processing (NLP), behavioural analysis, and privacy-first AI architecture** to analyze conversations and identify manipulation patterns such as:

- Trust building
- Secrecy requests
- Emotional manipulation
- Image requests
- Personal information requests
- Physical meetup attempts

Unlike traditional moderation systems that rely only on keyword detection, Guardian AI focuses on **conversation context, behavioural progression, and intent** to estimate grooming risk.

---

# 🎯 Problem Statement

Online grooming is a gradual process where attackers build trust and manipulate victims over time. Harmful intent is often hidden behind normal-looking conversations, making traditional keyword-based detection ineffective.

Existing systems face challenges such as:

- Lack of contextual understanding
- High false-positive rates
- Privacy concerns due to cloud-based message analysis
- Difficulty detecting early-stage manipulation

Guardian AI aims to provide an intelligent early-warning system while preserving user privacy.

---

# 💡 Solution

Guardian AI introduces a hybrid AI approach combining:

## 🧠 Local Tripwire AI

A lightweight AI layer that performs early analysis and detects suspicious patterns while minimizing exposure of sensitive conversations.

## 🤖 Sentinel AI Backend

A deeper analysis layer that evaluates behavioural patterns, maintains risk history, and provides final risk assessment.

## 🔒 Privacy-First Architecture

The system improves privacy by:

- Processing messages locally whenever possible
- Sending only required analysis data
- Avoiding storage of raw conversations
- Using hashed identifiers for users

---

# 🏗️ System Architecture

```
                 User Conversation
                        |
                        ↓
          Android Accessibility Service
                        |
                        ↓
              Local Tripwire AI
        (NLP + Rules + Risk Calculation)
                        |
                        ↓
              Risk Assessment JSON
                        |
                        ↓
              Sentinel AI Backend
                 (FastAPI Server)
                        |
                        ↓
              Behaviour Analysis
                        |
                        ↓
             Streamlit Dashboard
```

---

# ⚙️ System Components

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| Android Application | Kotlin | Secure conversation extraction |
| Local Tripwire AI | Python + Transformers | Early grooming detection |
| NLP Model | HuggingFace Transformers | Behaviour classification |
| Backend API | FastAPI | Advanced analysis and history |
| Dashboard | Streamlit | Risk visualization |

---

# 🧠 AI & NLP Pipeline

Guardian AI combines machine learning and rule-based intelligence.

## 1. Zero-Shot NLP Classification

A Transformer-based model analyzes conversation patterns using categories such as:

- Normal conversation
- Trust building
- Secrecy request
- Emotional manipulation
- Image request
- Meetup request
- Personal information request
- Sexual request
- Age discrepancy

The model evaluates behavioural patterns without requiring a large manually labelled dataset.

---

## 2. Behavioural Risk Scoring

The final risk score is calculated using:

```
Final Risk Score =
ML Classification Score
+
Rule-Based Behaviour Score
+
Conversation Context Analysis
```

The system considers:

- Excessive trust building
- Isolation attempts
- Requests for private information
- Image requests
- Attempts to move conversations offline

---

## 3. Noise Detection

Guardian AI reduces false positives using:

- Character entropy analysis
- Text uniqueness ratio
- Vowel distribution checks
- Gibberish detection

---

# 🚨 Risk Classification

| Level | Description |
|------|-------------|
| 🟢 LOW RISK | Normal conversation behaviour |
| 🟡 SUSPICIOUS | Potential manipulation patterns detected |
| 🔴 HIGH RISK | Strong grooming indicators detected |

---

# 📊 Dashboard

The Streamlit dashboard displays:

- Risk score
- Tripwire score
- Threat categories
- Behaviour summary
- Confidence score
- Conversation history

---

# 🛠️ Tech Stack

## Languages
- Python
- Kotlin

## AI / ML
- HuggingFace Transformers
- Zero-Shot Classification
- NLP Behaviour Analysis

## Backend
- FastAPI
- REST APIs
- JSON Communication

## Frontend
- Streamlit Dashboard
- Android Application

## Tools
- Git
- GitHub
- Uvicorn

---

# 📂 Project Structure

```
Guardian-AI/

│
├── android/
│   └── Android Accessibility Service
│
├── local_ai/
│   ├── conversation_analyzer.py
│   ├── risk_engine.py
│   └── adapter.py
│
├── backend/
│   ├── FastAPI Server
│   ├── API Routes
│   └── Database Layer
│
├── dashboard/
│   └── Streamlit Dashboard
│
├── requirements.txt
└── README.md
```

---

# 🚀 Installation & Usage

## Clone Repository

```bash
git clone https://github.com/Minnushar/guardian-ai.git
```

```bash
cd guardian-ai
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Backend

```bash
uvicorn main:app --reload
```

---

## Run Dashboard

```bash
streamlit run dashboard.py
```

---

# 🔮 Future Enhancements

- Real-time Android integration
- Multilingual grooming detection
- Explainable AI reasoning
- Parent/guardian alert system
- Behaviour timeline analysis
- Continuous model improvement using privacy-preserving learning

---

# 🌍 Impact

Guardian AI aims to provide an intelligent digital safety layer that identifies harmful online interactions at an early stage.

By combining **AI-based behavioural understanding** with a **privacy-first architecture**, Guardian AI moves beyond traditional moderation systems toward proactive online protection.

---

# 👥 Team Guardian AI

Built as part of an AI and cybersecurity innovation initiative focused on creating safer online environments.

---

⭐ If you find this project useful, consider starring the repository!