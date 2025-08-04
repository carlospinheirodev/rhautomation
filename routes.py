from main import app
from flask import render_template, request
from rh_analysis import analysis_with_n8n

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        position_requirements = request.form.get('position-requirements')
        analysis_complete = False
        complete_analysis = None
        error_message = None

        try:
            complete_analysis = analysis_with_n8n(position_requirements)

            if 'error' in complete_analysis:
                error_message = complete_analysis['error']
                print(f"Error in analysis: {error_message}")
                if 'received_data' in complete_analysis:
                    print(f"Received data: {complete_analysis['received_data']}")
            else:
                best_candidate = complete_analysis.get('best_candidate', {})
                ranking_list = complete_analysis.get('ranking_list', [])

                return render_template('index.html',
                                      analysis_complete=True,
                                      best_candidate=best_candidate,
                                      ranking_list=ranking_list)
        except Exception as e:
            error_message = f"Erro ao processar a análise: {str(e)}"
            print(error_message)

        return render_template('index.html',
                              analysis_complete=True,
                              error_message=error_message)
    else:
        return render_template('index.html', analysis_complete=False)