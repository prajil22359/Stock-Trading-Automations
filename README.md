# 🏦 Automated Stock Trading Bot and Floorsheet Analyzer

**⏱ Duration**: Jul 24 – Dec 24  
**🛠 Tech Stack**: Python, Selenium WebDriver  
**🔗 GitHub**: [GitHub Repo](#) <!-- Replace # with the actual repository link -->

---

## 🧩 Problem Statement

While actively investing in **NEPSE (Nepal Stock Exchange)**, I often noticed stock price surges triggered by news or sentiment. However, NEPSE enforces a strict **2% per trade cap** and a **10% daily limit**, making timing critical to capture high-momentum moves.

Manual trade execution was too slow — especially typing in the price the moment it opened. To capitalize on such short windows, **speed was everything**.  
Without access to an API, we leveraged **Python + Selenium** to simulate ultra-fast trades and automate the entire process.

---

## 🚀 What We Built

We developed a **high-speed stock trading bot** and a **daily floorsheet analyzer** that:

- Automates market orders with ~10ms frequency
- Increases trade execution speed compared to manual inputs
- Scrapes and filters floorsheet data for high-volume, high-impact trades
- (Optional) Sends Telegram alerts with daily insights

---

## 💡 Features

| Feature | Description |
|--------|-------------|
| ⚡ High-Speed Execution | Repeatedly attempts trades with sub-10ms latency using Selenium |
| 🧠 Floorsheet Analyzer | Parses NEPSE's daily floorsheet to find patterns and anomalies |
| 📤 Telegram Support | Sends daily summary reports to Telegram (optional integration) |
| 🧪 Timing & Reliability Tests | `test.py` helps validate execution timing logic |

---

## 📁 Folder Structure

