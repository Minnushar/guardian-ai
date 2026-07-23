# 🛡️ Guardian AI

> **An AI-powered grooming detection system that identifies potentially harmful conversations using Natural Language Processing (NLP), behavioral analysis, and a privacy-first architecture.**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

---

## 📖 Overview

Guardian AI is a proof-of-concept intelligent safety system designed to detect **online grooming behaviours** before they escalate into exploitation.

The system combines **Zero-Shot NLP**, **behavioral analysis**, and **rule-based risk scoring** to analyze conversations locally, preserving user privacy while providing real-time risk assessment.

Unlike traditional moderation systems that rely solely on keyword detection, Guardian AI evaluates conversation patterns such as:

- Trust building
- Secrecy requests
- Emotional manipulation
- Image requests
- Physical meetup requests

to estimate the likelihood of grooming behaviour.