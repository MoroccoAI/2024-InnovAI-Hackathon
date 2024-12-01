from langchain_community.document_loaders import PyPDFLoader
import os, sys, json
from flask import Flask, jsonify, request, render_template
from extract_details import extract_details, compare_details
from flask_cors import CORS
import tempfile

sys.path.insert(0, os.path.abspath(os.getcwd()))

import logging





def create_app(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route("/submit", methods=["POST"])
    def submit():
        try:
            logging.debug(f"Request files: {request.files}")
            if 'file' not in request.files or request.files['file'].filename == '':
                return jsonify({"error": "No file uploaded or wrong format!"}), 400

            doc = request.files["file"]
            
            job_offer_text = request.form.get("job_offer_text")
            if not job_offer_text:
                return jsonify({"error": "Job offer text is missing!"}), 400


            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                doc.save(temp_file.name)
                file_path = temp_file.name

            data = _read_file_from_path(file_path)
            resume_details = extract_details(data)
            job_offer_details = extract_details(job_offer_text)
            
            # if "error" in resume_details:
            #     return jsonify({"error": f"Resume parsing error: {resume_details['error']}"}), 500
            # if "error" in job_offer_details:
            #     return jsonify({"error": f"Job offer parsing error: {job_offer_details['error']}"}), 500


            response = compare_details(resume_details, job_offer_details)
            return jsonify({"response": response}), 200
        except Exception as e:
            logging.error(f"Error: {e}")
            return jsonify({"error": str(e)}), 500
 
def _read_file_from_path(path):
    try:
        loader = PyPDFLoader(path)
        pdf_documents = loader.load()
        if not pdf_documents:
            raise ValueError("No text found in the PDF.")
        return pdf_documents[0].page_content
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")







if __name__ == "__main__":
    app = Flask(__name__)
    # CORS(app)
    CORS(app, resources={r"/submit": {"origins": "*"}}) 
    create_app(app)
    app.run(host="0.0.0.0", port=8000, debug=False)



    # CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})