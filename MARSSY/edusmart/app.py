from flask import Flask, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
from utils.utils import *

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route('/submit', methods=['POST'])
def submit_answers():
    data = request.json
    out = {}
    
    # Function to run tasks in parallel
    def run_in_parallel():
        with ThreadPoolExecutor() as executor:
            # Submit tasks to the executor
            report_future = executor.submit(generate_customized_report, data)
            cours_future = executor.submit(generate_customized_cours, data)
            custom_qcm_future = executor.submit(generate_customized_qcm, data)
            
            # Collect results
            report = report_future.result()
            cours = cours_future.result()["data"]
            custom_qcm = custom_qcm_future.result()["data"]
            
        return report, cours, custom_qcm
    
    # Run the tasks
    report, cours, custom_qcm = run_in_parallel()
    
    # Prepare the output
    out["cours"] = cours
    out["report"] = report
    out["custom_qcm"] = custom_qcm
    return jsonify(out)

@app.route('/create_general_qcm', methods=['POST'])
def create_general_qcm():
    data = request.json
    data = mapping_front_back_meta_form(data)
    qcm_data = generate_general_qcm_from_cours_parties(**data)
    return jsonify(qcm_data["data"])

if __name__ == '__main__':
    app.run(debug=True)
