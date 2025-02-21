import streamlit as st
from wikipedia_fetch import fetch_wikipedia
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from summarizer import summarize_text
from preprocess import preprocess_query
from wikidata_fetch import fetch_from_wikidata, fetch_from_dbpedia, fetch_from_conceptnet
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_fscore_support
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import pandas as pd
import csv
from collections import defaultdict

# Load QA model
MODEL_NAME = "bert-large-uncased-whole-word-masking-finetuned-squad"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
qa_model = AutoModelForQuestionAnswering.from_pretrained(MODEL_NAME)
qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=tokenizer)

# Load Sentence Transformer
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Read the CSV file
csv_file = "historic_scientific_other_dataset.csv"
df = pd.read_csv(csv_file)

# Convert DataFrame to the required list of dictionaries
TEST_DATA = df.to_dict(orient="records")

# Default Answers
DEFAULT_ANSWERS = {
    "What is gravity?": "Gravity is a natural force that attracts two objects toward each other, typically proportional to their masses and inversely proportional to the square of the distance between them.",
    "What is quantum mechanics?": "Quantum mechanics is a fundamental theory in physics that describes nature at the smallest scales of energy levels of atoms and subatomic particles.",
}
# Example questions for historical and scientific classification
# File name
file_name = "example_questions.csv"

# Read CSV and transform into the desired format
example_questions = defaultdict(list)

with open(file_name, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        category = row["category"]
        question = row["question"]
        example_questions[category].append(question)

# Convert defaultdict to a standard dictionary
EXAMPLE_QUESTIONS = dict(example_questions)

# User-friendly instructions
st.sidebar.title("EduBot Instructions")
st.sidebar.write("Ask a historical or scientific question in the input box below.")
st.sidebar.write("Examples:")
st.sidebar.write("- Historical: 'Who was Napoleon Bonaparte?'")
st.sidebar.write("- Scientific: 'What is quantum mechanics?'")


def classify_query(query):
    """
    Classify the user query as historical, scientific, or other.
    """
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    historical_scores = util.cos_sim(query_embedding, embedder.encode(EXAMPLE_QUESTIONS["historical"]))
    scientific_scores = util.cos_sim(query_embedding, embedder.encode(EXAMPLE_QUESTIONS["scientific"]))
    max_historical_score = historical_scores.max().item()
    max_scientific_score = scientific_scores.max().item()

    # Debugging: Log classification scores
    print(f"Query: {query}")
    print(f"Historical Score: {max_historical_score}, Scientific Score: {max_scientific_score}")

    # Adjusted thresholds
    if max_historical_score > 0.3 and max_historical_score > max_scientific_score:
        return "historical"
    elif max_scientific_score > 0.3:
        return "scientific"
    return "other"


def fetch_best_context(query, entity, topic):
    """
    Fetch context from Wikipedia and fallback sources.
    """
    contexts = fetch_wikipedia(entity, multiple=True)
    if not contexts or len(" ".join(contexts)) < 50:
        print("No relevant content retrieved from Wikipedia. Attempting fallback sources...")

        # Fetch from other sources based on topic
        if topic == "scientific":
            wikidata_result = fetch_from_wikidata(entity)
            if wikidata_result:
                return wikidata_result.get("description", "")
        else:
            dbpedia_result = fetch_from_dbpedia(entity)
            if dbpedia_result:
                return dbpedia_result.get("description", "")

        # Fallback to ConceptNet
        conceptnet_result = fetch_from_conceptnet(entity)
        if conceptnet_result:
            return ", ".join(conceptnet_result.get("related_terms", []))

        return "No relevant content found in any source."

    full_context = " ".join(contexts[:5])
    return summarize_text(full_context) if len(full_context) > 1000 else full_context


st.title("EduBot: A Knowledge-Based Chatbot")

query = st.text_input("Ask a historical or scientific question:")

if st.button("Get Answer"):
    if query:
        topic = classify_query(query)
        if topic == "other":
            st.write("Sorry, I can only answer historical or scientific questions. Please try rephrasing.")
        else:
            tokens, entities, key_phrases = preprocess_query(query)
            entity = entities[0][0] if entities else key_phrases[0] if key_phrases else query
            context = fetch_best_context(query, entity, topic)

            if context:
                try:
                    qa_result = qa_pipeline(question=query, context=context)
                    answer = qa_result.get("answer", "").strip()
                    score = qa_result.get("score", 0)

                    if not answer or score < 0.4:
                        st.write("The answer is unclear. Here's the context instead:")
                        st.write(context)
                    else:
                        st.write(f"Answer: {answer}")
                except Exception as e:
                    st.write("An error occurred while processing your question.")
                    print(f"Error: {e}")
            else:
                st.write("No relevant information found in any source.")

# Custom Test Query Section
st.sidebar.header("Custom Test Queries")
custom_query = st.sidebar.text_input("Enter your custom query:")
custom_expected = st.sidebar.selectbox("Select expected topic:", ["historical", "scientific", "other"])

if st.sidebar.button("Add to Test Data"):
    if custom_query:
        TEST_DATA.append({"query": custom_query, "expected_topic": custom_expected})
        st.sidebar.success(f"Added: {custom_query} (Expected: {custom_expected})")

if st.button("Evaluate Bot"):
    predicted_topics = [classify_query(test["query"]) for test in TEST_DATA]
    expected_topics = [test["expected_topic"] for test in TEST_DATA]
    accuracy = accuracy_score(expected_topics, predicted_topics)
    st.write(f"Classification Accuracy: {accuracy:.2f}")
    st.text(classification_report(expected_topics, predicted_topics))
