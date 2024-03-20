from flask import Flask, render_template, request
from retrieve import predict_audio

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the bucket name entered by the user
        bucket_name = request.form['bucket_name']
        
        # Run the prediction process
        predictions = predict_audio(bucket_name)
        
        # Render the results template with predictions
        return render_template('results.html', predictions=predictions)
    
    # Render the index template with the form
    return render_template('indexfinal.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
