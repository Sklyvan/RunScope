# 🏃‍♂️ RunScope – Advanced Running Metrics Analyzer

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![Repo](https://img.shields.io/badge/GitHub-%40Sklyvan-blue?logo=github)](https://github.com/Sklyvan/RunScope)

> 🧠 **Run smarter. Analyze deeper.**  
> 🚀 Unlock hidden insights from your GPS data with scientifically calculated metrics.

---

## 📦 What is RunScope?

**RunScope** is a Python library that processes `TCX` files to compute **advanced running metrics** using science-backed formulas.  

🎯 Whether you're chasing a SUB-3 marathon or optimizing cadence for efficiency — RunScope has your back.

---

## 🔍 Features

✅ **TCX File Parsing**  
✅ **Zone-Based Analysis** (Heart Rate, Pace, Cadence)  
✅ **VO₂ Max estimation** via multiple scientific methods  
✅ **Execution Scoring** vs. Target Plan  
✅ **Efficiency Metrics**: Ground Contact Balance, Vertical Ratio, Form Power  
✅ **Run Summaries** & Custom Visualizations  
✅ **Fatigue & Aerobic/Anaerobic Effect Scoring**

---

## 🧠 Example Metrics

| Metric                    | Description                                      |
|--------------------------|--------------------------------------------------|
| 🫀 `VO2 Max`             | Estimate via Daniels, Jack T., and Garmin models |
| 📊 `Pace Zones`         | Time spent in each pace range                    |
| 🧱 `Fatigue Index`      | Cumulative muscular + cardio fatigue             |
| 🦵 `Form Power`         | Estimate of power lost to poor form              |
| ⚖️ `Ground Contact Balance` | % left vs right (asymmetry metric)          |
| 📈 `Vertical Ratio`     | Vertical oscillation / stride length             |

---

## 🚀 Installation

Install using `pip` from source:

```bash
    git clone https://github.com/Sklyvan/RunScope.git
    cd RunScope
    pip install -e .
```
Or with standard build tools:
```bash
    pip install .
```
✅ Python 3.10+ required.

## 📁 Project Structure
```
    run_scope/
    │
    ├── models.py         # Data models for each run
    ├── parser.py         # TCX/GPX/FIT file parsing
    ├── metrics.py        # Core calculations and derived metrics
    ├── zones.py          # Zone definitions and analysis
    ├── utils.py          # Helpers: smoothing, conversions, etc.
    ├── config.py         # Defaults, thresholds, settings
    └── __init__.py
```

---

## 📊 Coming Soon 
🗺️ Support for `GPX` and `FIT`

🌐 Web Dashboard Module with Streamlit

📈 Automated PDF Reports

🔄 Strava/Garmin Synchronization

🤖 AI Models for Prediction

---

## 📜 License
Licensed under the MIT License – feel free to use it for personal or commercial projects.
See [LICENSE](LICENSE) for more details.

## 🧭 Stay Connected
📫 github.com/Sklyvan/RunScope
<br>
📈 Let's decode the science of running together.

> Train hard. Run smart. Analyze everything. 🧬