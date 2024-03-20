import boto3
import io
import librosa
import numpy as np
import pickle

def predict_audio(bucket_name):
    with open('classifier.pkl', 'rb') as file:
        clf = pickle.load(file)
    
    # Replace 'your-access-key-id' and 'your-secret-access-key' with your actual AWS credentials
    aws_access_key_id = "YOUR-ACCESS-KEY"
    aws_secret_access_key = "YOUR-SECRET-ACCESS-KEY"

    # Initialize an S3 client with your credentials
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    predictions = []
    # Iterate over each object in the bucket
    for obj in response.get('Contents', []):
        file_key = obj['Key']
        
        # Check if the file has a .wav extension
        if file_key.endswith('.wav'):
            try:
                # Get the object from S3
                audio_response = s3.get_object(Bucket=bucket_name, Key=file_key)
                
                # Read the audio data from the response and convert it to bytes
                audio_bytes = audio_response['Body'].read()
                
                # Convert bytes to a file-like object
                audio_file_like = io.BytesIO(audio_bytes)
                
                # Load audio using librosa
                audio, sample_rate = librosa.load(audio_file_like)
                
                # Extract MFCC features
                mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
                mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
                
                # Prepare features for prediction
                prediction_feature = mfccs_scaled_features.reshape(1, -1)
                
                # Make prediction
                predicted_label = np.argmax(clf.predict(prediction_feature), axis=1)
                
                # Print prediction result
                if predicted_label == 0:
                    prediction = "clean"
                else:
                    prediction = "infested"
                
                # Add prediction to the list
                predictions.append((file_key, prediction))
            
            except Exception as e:
                # If an error occurs during prediction, add an error message to the list
                predictions.append((file_key, f"Error: {str(e)}"))
    
    return predictions
