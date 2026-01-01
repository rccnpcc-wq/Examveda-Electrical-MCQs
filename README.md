# ⚡ Electrical Engineering MCQ Bank
### *A Comprehensive, Interactive Study Resource*

**Author:** Rising Engineer  
**Project Status:** 61 Topics | Complete Image Integration | MathJax Support

---

## 📖 Overview
This project is a powerful two-stage system designed to scrape comprehensive Electrical Engineering MCQs from Examveda and transform them into a **beautiful, interactive digital textbook**. It features technical diagram preservation and professional mathematical formula rendering using LaTeX.

## ✨ Key Features
* **Complete Data Scraping:** Automatically fetches questions, options, and detailed solutions for all 61 electrical topics.
* **Technical Diagram Support:** Downloads and localizes images, ensuring the MCQ bank is fully functional offline.
* **Interactive HTML Interface:** Features a "Show/Hide Answer" toggle for active recall study.
* **Professional Math Rendering:** Integrated **MathJax** engine renders complex electrical formulas ($\rho, \Omega, \Sigma$) with textbook quality.
* **Dynamic Table of Contents:** A clickable TOC for instant navigation across thousands of questions.

---

## 🛠️ Installation & Setup

### 1. Requirements
Ensure you have **Python 3.x** installed. Then, install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 2. Project Structure

```
├── Code.py                # Data & Image Scraper
├── html_generator.py      # HTML Book Builder
├── requirements.txt       # Project Dependencies
├── Final_Electrical_MCQs_with_Images.txt  # Raw Data (Generated)
└── mcq_images/            # Technical Diagrams (Downloaded)
```

---

## 📸 Preview

### Interactive Question Interface
![Question Interface](./Preview%20Images/img1.png)

The final HTML file features an elegant, interactive study interface with:
- Clean question presentation with multiple-choice options
- One-click "Show/Hide Answer & Solution" toggles for active learning
- Professional formatting with clear visual hierarchy

### Comprehensive Table of Contents
![Table of Contents](./Preview%20Images/img2.png)

Navigate through all 61 electrical engineering topics with the clickable table of contents, featuring question counts for each topic.

---

## 🚀 How to Use

### Step 1: Data Collection
Run the scraper to collect all questions and images.

```bash
python Code.py
```

Note: This script is configured to create a fresh file (`mode="w"`) starting from Topic 1 (`start_from=0`).

### Step 2: Build the Book
Once the scraping is complete, run the generator to create your interactive HTML file.

```bash
python html_generator.py
```

### Step 3: Study
Open `Electrical_Engineering_Bank.html` in any web browser to begin.

---

## 📦 Dependencies
* **Requests:** For web crawling and image downloading.
* **BeautifulSoup4:** For data extraction from HTML.
* **MathJax:** Cloud-delivered LaTeX rendering for equations.
* **Setuptools:** Core package management tool.

---

Created by Rising Engineer — 2026
