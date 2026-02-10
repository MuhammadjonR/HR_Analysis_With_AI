# 🚀 AI Talent Scout Pro

**AI Talent Scout Pro** is a cutting-edge, AI-powered Applicant Tracking System (ATS) designed to streamline the recruitment process. By leveraging **RAG (Retrieval-Augmented Generation)** and **Llama 3** models, it intelligently analyzes resumes against Job Descriptions (JD) to provide deep technical insights and rankings.



## ✨ Key Features

* **🔍 Hybrid Search Engine:** Combines **BM25 keyword search** with **ChromaDB Vector embeddings** for highly accurate candidate retrieval.
* **⚖️ Strict Weighted Scoring:** A rigorous evaluation system that assigns scores (0-100) based on specific JD requirements (LLM, RAG, Experience, etc.).
* **📊 Visual Analytics:** Interactive **Radar Charts** to compare the top 5 candidates' technical proficiency at a glance.
* **📧 Personalized Outreach:** Automatically generates professional, candidate-specific interview invitation emails.
* **📥 PDF Reports:** Export detailed analysis results into professional PDF documents for stakeholders.
* **📁 Dynamic CV Management:** Easy upload interface with an automated pipeline for parsing and indexing PDF resumes.

---

## 📸 Screenshots

| Dashboard Overview | Technical Analysis |
| :--- | :--- |
| ![Main Interface](img/Main.png) | ![Analysis Results](img/Analysis.png) |

| Skill Comparison | Automated Email Drafts |
| :--- | :--- |
| ![Radar Chart](img/Radar.png) | ![Report Generation](img/Report.png) |

---

## 🛠 Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Framework:** [LangChain](https://www.langchain.com/)
* **LLM:** [Ollama](https://ollama.com/) (Llama 3, Nomic-Embed-Text)
* **Vector Database:** [ChromaDB](https://www.trychroma.com/)
* **Data Visualization:** Plotly
* **Document Processing:** PyPDF2, LangChain DirectoryLoaders

---

## 🚀 Installation & Setup

### 1. Clone the Repository

git clone [https://github.com/MuhammadjonR/HR_Analysis_With_AI.git](https://github.com/MuhammadjonR/HR_Analysis_With_AI.git)
cd AI-Talent-Scout-Pro

### 2. Set Up Virtual Environment
```
Bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
### 3. Install Dependencies
```
Bash
pip install -r requirements.txt
```
### 4. Pull Required AI Models (Ollama)
```
Ensure you have Ollama installed and running:

Bash
ollama pull llama3
ollama pull nomic-embed-text
```
### 5. Run the Application
```
Bash
streamlit run main.py
```
💡 Usage Guide
Upload Resumes: Use the sidebar to upload candidate CVs in PDF format.

Indexing: Click "Save & Index" to build the vector database.

Define Requirements: Paste your Job Description into the main text area.

Analyze: Hit "Start AI Analysis" to receive ranked results, technical critiques, and interview questions.

🤝 Contributing
Contributions make the open-source community an amazing place to learn and create.

Fork the Project.

Create your Feature Branch (git checkout -b feature/AmazingFeature).

Commit your Changes (git commit -m 'Add some AmazingFeature').

Push to the Branch (git push origin feature/AmazingFeature).

Open a Pull Request.

### 📝 License
Distributed under the MIT License. See LICENSE for more information.

#### 👨‍💻 Developer: Rakhmataliev Muhammadjon

### 📧 Contact: [rakhmatalievm@gmail.com](Email)


---
