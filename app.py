from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from utils import load_openai_embeddings, load_db
from flask import Flask, request, jsonify, redirect, url_for, render_template
import subprocess

load_dotenv()

class retrieval_chat():

    def __init__(self) -> None:
        
        # embedding_function = load_embeddings()
        embedding_function = load_openai_embeddings()

        db = load_db(embedding_function)

        self.qa = RetrievalQA.from_llm(llm=ChatOpenAI(temperature=0.1), retriever=db.as_retriever(kwargs={"k": 7}), return_source_documents=True)

    def answer_question(self, question :str):
        output = self.qa({"query": question})
        # print("Source Documents: ")
        # print(output["source_documents"])
        return output["result"]

app = Flask(__name__)
UPLOAD_FOLDER = 'new_documents'
qa = retrieval_chat()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' in request.files:
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('index'))

@app.route('/add_document', methods=['POST'])
def add_document():
    subprocess.run(["python", "add_document.py"])
    return redirect(url_for('index'))

@app.route('/query', methods=['POST'])
def query():
    # data = request.formjson
    question = request.form['query']
    answer = qa.answer_question(question)
    formatted_response = answer.replace("\n", "<br>")
    return render_template('index.html', response = formatted_response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
