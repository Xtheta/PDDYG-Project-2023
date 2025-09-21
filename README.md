# 📊 Multidimensional Data Structures – Implementation and Comparison

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)

## 📌 Project Overview
This project focuses on the **implementation and experimental evaluation of multidimensional data structures** using real-world datasets.  
We study the performance of key operations:  
- Building, inserting, deleting, updating  
- Queries: similarity search, **k-nearest neighbors (kNN)**, interval queries, stabbing queries, and 3-sided queries  

The goal is to **assess efficiency and scalability** in handling complex multidimensional queries.

---

## ⚙️ Implementation Details
We implemented four widely used multidimensional data structures:
- **K-D Tree**
- **Quad Tree**
- **Range Tree**
- **R-Tree**

### Dataset
- Source: [Wikipedia – Computer Science Scientists](https://en.wikipedia.org/wiki/List_of_computer_scientists)  
- Format: `(Surname: String, #Awards: Integer, Education: text-vector)`  
- Indexing performed on:  
  - **Surname** (alphabetical range)  
  - **Number of Awards** (threshold filter)  

### Query Example
Using **Locality-Sensitive Hashing (LSH)** for similarity on the education field:  

> *"Find computer science scientists with an education similarity >60%, surname in [A, G], and at least 4 awards."*

### Experimental Comparison
We compared:
- **K-D Tree + LSH**  
- **Quad Tree + LSH**  
- **Range Tree + LSH**  
- **R-Tree + LSH**  

📌 Metrics: query response time, memory efficiency, and scalability.

---

## 📂 Repository Structure
- `KD_Tree.py` → K-D Tree implementation  
- `Quad_Tree.py` → Quad Tree implementation  
- `Range_Tree.py` → Range Tree implementation  
- `R_Tree.py` → R-Tree implementation  
- `lsh.py` → Locality-Sensitive Hashing for similarity search  
- `main.py` → Run experiments and comparative analysis  
- `scientists.csv` → Dataset of computer science scientists  
- `webScaper.py` → Web scraper to collect dataset from Wikipedia  
- `diagrams/` → Visualizations and analysis diagrams  

---

## 🚀 How to Run
Clone the repo:
```bash
git clone https://github.com/Xtheta/PDDYG-Project-2023.git
cd PDDYG-Project-2023
