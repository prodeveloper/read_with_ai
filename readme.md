# PDF Page-by-Page Analysis Tool

NOTE: This is still in development and not ready for production use.

## Introduction

This Streamlit app allows you to analyze PDF documents page by page, providing concise summaries and enabling focused reading. Unlike tools that summarize entire documents, our app lets you explore content incrementally, making it ideal for in-depth study of academic papers, legal documents, or any lengthy PDF.

## Key Features

- Upload any PDF file
- Get AI-generated summaries for specific pages
- Build understanding progressively as you move through the document
- Cached summaries for faster repeated access

## Use Cases

This tool is particularly beneficial for:

- **Academic Research**: Quickly grasp the main points of each page in a scholarly article or textbook.
- **Legal Document Review**: Efficiently analyze lengthy contracts or legal texts.
- **Literature Review**: Summarize key points from multiple sources in a systematic manner.
- **Technical Documentation**: Break down complex technical documents into more digestible segments.

## How to Use

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set your Gemini API key in a `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
4. Run the Streamlit app: `streamlit run stream.py`
5. Upload your PDF or specify the path to your PDF in the app
6. Enter the page number you want to summarize
7. View the AI-generated summary for that page

## Example

Once you run the app, you'll see a simple interface where you can:

1. Specify the path to your PDF (or use the default "map_reduce.pdf")
2. Enter a page number to summarize
3. View the generated summary

The app will display:
- The unique key for the summarized page (for caching purposes)
- A concise summary of the specified page (maximum 5 bullet points)

## Benefits

1. **Efficient Reading**: Quickly identify key sections that require more in-depth reading.
2. **Better Comprehension**: Build a solid understanding of the document's structure and content.
3. **Time-Saving**: Focus your attention on the most relevant parts of the document.
4. **Improved Retention**: Reinforce your understanding by summarizing and questioning as you go.

## Why This Approach?

- Efficient for long documents: Focus on relevant sections
- Better comprehension: Build understanding page by page
- Time-saving: Quickly identify key areas for in-depth reading
- Ideal for academic work: Grasp main points before detailed study

## How It Works

1. **Upload PDF**: Users can upload their PDF document to the application.
2. **Select Page**: Specify which page you want to analyze.
3. **Generate Summary**: The AI generates a concise summary (maximum 5 bullet points) for the selected page.
4. **Caching**: Summaries are cached for faster access on repeated queries.

## Contributing

We welcome contributions! Feel free to submit issues or pull requests on our GitHub repository.

## License

[Insert your chosen license here]