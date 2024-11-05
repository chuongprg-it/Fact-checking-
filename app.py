import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fact_checking', methods=['GET', 'POST'])
def fact_checking():
    if request.method == 'POST':
        input_text = request.form['input_text']
        tsv_path = os.path.join('data', 'dev.combined.not_precomputed.p5.s5.t3.cells.tsv')
        jsonl_path = os.path.join('data', 'dev.combined.not_precomputed.p5.s5.t3.cells.jsonl')
        prob_path = os.path.join('data', 'combined_file.prob')
        claim_id = None  # Initialize claim_id with None

        
        # Đọc file TSV và tìm câu nhập từ textbox
        with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
            lines = tsv_file.readlines()
            for i, line in enumerate(lines):
                columns = line.split('\t')
                if input_text in columns[2]:
                    claim_id = columns[1]
                    break
        if claim_id is None:
            result = "Câu nhập không có trong dữ liệu."
            return render_template('fact_checking.html', result=result)
        # Đọc file JSONL và tìm thông tin theo claim_id
        with open(jsonl_path, 'r', encoding='utf-8') as jsonl_file:
            for jsonl_line in jsonl_file:
                jsonl_data = json.loads(jsonl_line)
                if str(jsonl_data['id']) in str(claim_id):
                    predicted_label = jsonl_data['predicted_label']
                    label = jsonl_data['label']
                    predicted_evidence = jsonl_data['predicted_evidence']
                    evidence = jsonl_data['evidence']
                    gold_evidence = []
                    for entry in evidence:
                        for content_item in entry['content']:
                            gold_evidence.append(content_item)
                            context_items = entry['context'][content_item]
                            print(gold_evidence)
                    break

        # Đọc file prob và lấy xác xuất
        with open(prob_path, 'r', encoding='utf-8') as prob_file:
            prob_lines = prob_file.readlines()
            for i, line in enumerate(prob_lines):
                columns = line.split('\t')
                if claim_id == columns[0]:
                    probabilities = columns[1].split(' ')
                    result = {
                            'input_text': input_text,
                            'predicted_label': predicted_label,
                            'label': label,
                            'probabilities': {
                                'SUPPORTED': probabilities[0],
                                'REFUTED': probabilities[1],
                                'NOT ENOUGH INFORMATION': probabilities[2]
                            },
                            'predicted_evidence': predicted_evidence,
                            'evidence': gold_evidence
                        }
            # probabilities = prob_lines[int(claim_id)].strip().split(' ')

        # result = {
        #     'predicted_label': predicted_label,
        #     'label': label,
        #     'probabilities': {
        #         'SUPPORTED': probabilities[1],
        #         'REFUTED': probabilities[2],
        #         'NOT ENOUGH INFORMATION': probabilities[3]
        #     }
        # }
        
        return render_template('fact_checking.html', result=result)
        
        # result = "Câu nhập không có trong dữ liệu."
        # return render_template('fact_checking.html', result=result)
    return render_template('fact_checking.html')

@app.route('/detail_fact_checking', methods=['GET', 'POST'])
def detail_fact_checking():
    if request.method == 'POST':
        text = request.form['input_text']
        # Thực hiện xử lý detail fact-checking
        detailed_result = f"Kết quả chi tiết fact-checking cho '{text}' là..."
        return render_template('detail_fact_checking.html', detailed_result=detailed_result)
    return render_template('detail_fact_checking.html')


# @app.route('/evidence_retrieval', methods=['POST'])
# def evidence_retrieval():
#     input_text = request.form['input_text']
#     tsv_path = os.path.join('data', 'dev.combined.not_precomputed.p5.s5.t3.cells.tsv')
#     jsonl_path = os.path.join('data', 'dev.combined.not_precomputed.p5.s5.t3.cells.jsonl')

#     text_evidence = []
#     table_evidence = []

#     # Đọc file TSV và tìm câu nhập từ textbox
#     with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
#         lines = tsv_file.readlines()
#         for i, line in enumerate(lines):
#             columns = line.strip().split('\t')
#             if input_text == columns[2]:
#                 claim_id = columns[1]
#                 print(claim_id)
#                 if columns[0] == "claim":
#                     claim = columns[2]
#                 if str(columns[0]) == "text_evid":
#                     if columns[4] != '-1':
#                         text_evidence['wiki_page'] = columns[3]
#                         text_evidence['local_page'] = columns[4]
#                         text_evidence['detail_evidence'] = columns[5]
#                     else: 
#                         text_evidence['wiki_page'] = 'None'
#                         text_evidence['local_page'] = 'None'
#                         text_evidence['detail_evidence'] = 'None'

#                 if str(columns[0]) == "tab_evid":
#                     if columns[4] != '-1':
#                         table_evidence['wiki_page'] = columns[3]
#                         table_evidence['local_page'] = columns[4]
#                         table_evidence['detail_evidence'] = columns[5]
#                     else: 
#                         table_evidence['wiki_page'] = 'None'
#                         table_evidence['local_page'] = 'None'
#                         table_evidence['detail_evidence'] = 'None'
#         # with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
#         #     lines = tsv_file.readlines()
#         #     for i, line in enumerate(lines):
#         #         columns = line.strip().split('\t')
#         #         if input_text == columns[2]:
#         #             claim_id = columns[0]

#         #         with open(jsonl_path, 'r', encoding='utf-8') as jsonl_file:
#         #             for jsonl_line in jsonl_file:
#         #                 jsonl_data = json.loads(jsonl_line)
#         #                 if jsonl_data['id'] == claim_id:
#         #                     text_evidence = jsonl_data['text_evidence'][0] if jsonl_data['text_evidence'] else "N/A"
#         #                     table_evidence = jsonl_data['table_evidence'][0] if jsonl_data['table_evidence'] else "N/A"
#         #                     result = {
#         #                         'input_text': input_text,
#         #                         'text_evidence': text_evidence,
#         #                         'table_evidence': table_evidence
#         #                     }
#                     result = {
#                         'input_text': input_text,
#                         'claim': claim,
#                         'text_evidence': text_evidence,
#                         'table_evidence': table_evidence
#                     }
#                     return render_template('detail_fact_checking.html', result=result)

#     result = {
#         'input_text': input_text,
#         'message': "Câu nhập không có trong dữ liệu."
#     }
#     return render_template('detail_fact_checking.html', result=result)


@app.route('/evidence_retrieval', methods=['POST'])
def evidence_retrieval():
    input_text = request.form['input_text']
    tsv_path = os.path.join('data', 'dev.combined.not_precomputed.p5.s5.t3.cells.tsv')
    jsonl_path = os.path.join('data', 'dev.combined.not_precomputed.p5.s5.t3.cells.jsonl')
    prob_path = os.path.join('data', 'combined_file.prob')
    claim_id = None  # Initialize claim_id with None
    #######
    # Đọc file TSV và tìm câu nhập từ textbox
    with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
        lines = tsv_file.readlines()
        for i, line in enumerate(lines):
            columns = line.split('\t')
            if input_text in columns[2]:
                claim_id = columns[1]
                break
    if claim_id is None:
        result = "Câu nhập không có trong dữ liệu."
        return render_template('detail_fact_checking.html', result=result)
    # Đọc file JSONL và tìm thông tin theo claim_id
    with open(jsonl_path, 'r', encoding='utf-8') as jsonl_file:
        for jsonl_line in jsonl_file:
            jsonl_data = json.loads(jsonl_line)
            if str(jsonl_data['id']) in str(claim_id):
                predicted_label = jsonl_data['predicted_label']
                label = jsonl_data['label']
                predicted_evidence = jsonl_data['predicted_evidence']
                evidence = jsonl_data['evidence']
                gold_evidence = []
                for entry in evidence:
                    for content_item in entry['content']:
                        gold_evidence.append(content_item)
                        context_items = entry['context'][content_item]
                        print(gold_evidence)
                break

    # Đọc file prob và lấy xác xuất
    with open(prob_path, 'r', encoding='utf-8') as prob_file:
        prob_lines = prob_file.readlines()
        for i, line in enumerate(prob_lines):
            columns = line.split('\t')
            if claim_id == columns[0]:
                probabilities = columns[1].split(' ')
    #######
    text_evidences = []
    table_evidences = []

    # Đọc file TSV và tìm câu nhập từ textbox
    with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
        lines = tsv_file.readlines()
        for i, line in enumerate(lines):
            columns = line.strip().split('\t')
            if input_text == columns[2]:
                claim_id = columns[1]
                print(claim_id)
                if columns[0] == "claim":
                    claim = columns[2]
                if str(columns[0]) == "text_evid":
                    text_evidence = {
                        'wiki_page': columns[3] if columns[4] != '-1' else 'None',
                        'local_page': columns[4] if columns[4] != '-1' else 'None',
                        'detail_evidence': columns[5] if columns[4] != '-1' else 'None'
                    }
                    text_evidences.append(text_evidence)

                if str(columns[0]) == "tab_evid":
                    table_evidence = {
                        'wiki_page': columns[3] if columns[4] != '-1' else 'None',
                        'local_page': columns[4] if columns[4] != '-1' else 'None',
                        'detail_evidence': columns[5] if columns[4] != '-1' else 'None'
                    }
                    table_evidences.append(table_evidence)
                    # Lọc bỏ các giá trị None
                    text_evidences = [evidence for evidence in text_evidences if evidence['wiki_page'] != 'None' and evidence['local_page'] != 'None' and evidence['detail_evidence'] != 'None']
                    table_evidences = [evidence for evidence in table_evidences if evidence['wiki_page'] != 'None' and evidence['local_page'] != 'None' and evidence['detail_evidence'] != 'None']
                    print(text_evidences)
                    print(table_evidences)
                    result = {
                        'input_text': input_text,
                        'claim': claim,
                        'text_evidence': text_evidences,
                        'table_evidence': table_evidences,
                        'predicted_label': predicted_label,
                            'label': label,
                            'probabilities': {
                                'SUPPORTED': probabilities[0],
                                'REFUTED': probabilities[1],
                                'NOT ENOUGH INFORMATION': probabilities[2]
                            },
                        'predicted_evidence': predicted_evidence,
                        'evidence': gold_evidence
                    }
                    return render_template('detail_fact_checking.html', result=result)

    result = {
        'input_text': input_text,
        'message': "Câu nhập không có trong dữ liệu."
    }
    return render_template('detail_fact_checking.html', result=result)

@app.route('/verdict_verification', methods=['POST'])
def verdict_verification():
    input_text = request.form['input_text']
    result = {
        'input_text': input_text,
        'message': "Logic cho Verdict Verification chưa được triển khai."
    }
    return render_template('detail_fact_checking.html', result=result)

    
if __name__ == '__main__':
    app.run(debug=True)
