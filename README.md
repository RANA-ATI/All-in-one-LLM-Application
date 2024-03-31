# All in one LLM

This is a LLM based application. It has LLama-v2 LLM used. One can utilize one of the two facilities.

- **Simple LLM** : You can ask questions, and the application will provide relevant answers based on the information it has.
- **Customzied RAG** : RAG is a technique that combines information retrieval with language generation, allowing for more precise and informative responses to user queries. One has to upload pdf files to utilize its power and just query through to have results from those PDFs

### Setup

1. Clone the repository to your local machine:

```bash
git clone <repository_url>
```

2. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

3. Replace <your_replicate_api_token> in the customizable_llm_rag.py and simple_llm.py files with your actual [Replicate](https://replicate.com/) API token.

### Usage

Once you've completed the setup, you can start the application by running:

```bash
python app.py
```

This will start the Flask server, and you can access the application via your web browser at http://localhost:5000.

### License

This project is licensed under the MIT License.
