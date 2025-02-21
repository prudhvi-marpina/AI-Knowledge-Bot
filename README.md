# AI-Knowledge-Bot

EduBot is an **AI-powered chatbot** designed to answer queries on **historical events** and **scientific concepts** using **Natural Language Processing (NLP)**. It integrates **structured data (WikiData)** and **unstructured content (Wikipedia API)** to provide **accurate, summarized responses**.

## 🚀 Features
- 📖 **Query Understanding**: Uses **spaCy** for **tokenization, Named Entity Recognition (NER), and stop-word removal**.
- 🔎 **Data Retrieval**: Fetches structured data using **SPARQL queries on WikiData** and unstructured content via the **Wikipedia API**.
- 📝 **Summarization**: Leverages **pre-trained BART** models for concise, high-quality text summaries.
- 🤖 **Chatbot Interface**: Built on **Streamlit** for real-time interaction and testing.
- 🎯 **Smart Categorization**: Determines whether a query is **historical or scientific** using a scoring mechanism.

## 🎯 Use Cases
EduBot is designed for:
1. 📚 **Students** – Quick explanations of scientific and historical concepts.
2. 🔬 **Researchers** – Quick access to verified knowledge.
3. 🌎 **Knowledge Seekers** – General understanding of complex topics.
4. 👩‍🏫 **Educators & Teachers** – Supplementary teaching tool.

## 🏗️ Project Architecture
### **1️⃣ Preprocessing**
- Uses **spaCy** for:
  - Tokenization
  - Named Entity Recognition (NER)
  - Stop-word removal

### **2️⃣ Data Retrieval**
- **Structured Data**: WikiData SPARQL queries.
- **Unstructured Data**: Wikipedia API for contextual information.

### **3️⃣ Summarization**
- **BART Transformer Model** for generating short and informative responses.

### **4️⃣ Chatbot Framework**
- Implemented in **Streamlit** for a simple and interactive UI.

## 🛠️ Installation & Setup
### **Prerequisites**
- Python 3.8+
- `pip` package manager
- Clone the repository:
  ```sh
  git clone https://github.com/prudhvi-marpina/AI-Knowledge-Bot.git
  cd AI-Knowledge-Bot

