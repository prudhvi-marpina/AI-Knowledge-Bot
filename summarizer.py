from transformers import pipeline

# Load pre-trained summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_text(text):
    """
    Summarize the given text using a pre-trained summarization model.
    Handles large text by splitting into manageable chunks.
    """
    # Break down large text into chunks for summarization
    max_chunk_size = 1000  # Maximum input size for the model
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    summarized_text = ""
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
        summarized_text += summary[0]["summary_text"] + " "

    return summarized_text.strip()


# Test the function
if __name__ == "__main__":
    text = (
        "The Civil War was fought in the United States from 1861 to 1865. "
        "The Union faced secessionists in eleven Southern states grouped together as the Confederate States of America. "
        "The central cause of the war was the status of slavery, especially the expansion of slavery into territories "
        "acquired as a result of the Louisiana Purchase and the Mexican–American War."
    )
    summary = summarize_text(text)
    print("Summary:", summary)
