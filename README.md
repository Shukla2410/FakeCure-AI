# FakeCure‑AI 🩺

FakeCure‑AI is a lightweight medical misinformation detection bot.  
Users can forward health‑related messages to a Telegram bot and receive a quick, concise explanation based on trusted medical information instead of random internet claims. [page:1]

---

## 🚀 Overview

- Telegram bot for checking **health and treatment claims**.
- Flask backend that reads from a curated `trusted_data.json` knowledge base.
- Returns short, human‑readable replies explaining why a claim looks reliable or suspicious. [page:1]

---

## ✨ Features

- Accepts forwarded or typed health messages in Telegram.
- Matches claims against structured trusted data (e.g., verified treatments, common myths). [page:1]
- Flags likely misinformation and provides a brief explanation instead of just “true/false”.
- Simple Python/Flask codebase that can be extended with ML/NLP models later. [page:1]

---

## 🧠 How It Works

1. User sends a health‑related message to the Telegram bot.
2. The bot sends the text to the Flask API.
3. The API loads `trusted_data.json`, searches for relevant entries, and returns:
   - Whether the claim looks supported or suspicious.
   - A short explanation or reference. [page:1]
4. The bot formats this into a friendly reply in Telegram.

---

## 🛠 Tech Stack

- Python  
- Flask (REST API)  
- Telegram Bot API  
- JSON (`trusted_data.json` as a simple knowledge base) [page:1]

---

