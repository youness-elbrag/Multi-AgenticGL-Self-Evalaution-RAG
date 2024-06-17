import torch
import pandas as pd
from datetime import datetime, timedelta

class TaskDurationEstimator:
    def __init__(self, model_class, tokenizer, min_total_hours, max_total_hours):
        self.model = model_class
        self.tokenizer = tokenizer
        self.min_total_hours = min_total_hours
        self.max_total_hours = max_total_hours

    def load_model(self, model_path):
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
    
    def predict_task_duration(self, task_description):
        # Tokenize the task description
        self.tokenizer.model_max_length = 40
        task_token = self.tokenizer.encode(task_description, padding='max_length', return_tensors="pt")
        # Predict the normalized time duration using the model
        with torch.no_grad():
            prediction_normalized = self.model(task_token).squeeze().item()
            # Scale the prediction to actual hours
            time_duration_hours = int(prediction_normalized * (self.max_total_hours - self.min_total_hours) + self.min_total_hours)
        return time_duration_hours

    def estimate_finished_date(self, current_date, time_duration_hours):
        # Calculate the number of days and remaining hours from the duration in hours
        time_duration_days = time_duration_hours // 24
        remaining_hours = time_duration_hours % 24
        # Calculate the finished date based on the current date and time duration
        finished_date = current_date + timedelta(days=time_duration_days, hours=remaining_hours)
        return finished_date

    def single_task_duration(self, task_description):
        # Predict the time duration for the task
        time_duration_hours = self.predict_task_duration(task_description)
        # Get the current date and time
        current_date = datetime.now()
        # Estimate the finished date for the task
        finished_date = self.estimate_finished_date(current_date, time_duration_hours)
        
        # Prepare data for DataFrame
        data = {
            "Task Description": [task_description],
            "Estimated Time Duration (hours)": [time_duration_hours],
            "Current Time Start Task": [current_date.strftime("%Y-%m-%d %H:%M:%S")],
            "Estimated Finished Date": [finished_date.strftime("%Y-%m-%d %H:%M:%S")]
        }
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        return df

    def multi_task_durations(self, tasks):
        # List to store task details
        task_details = []

        # Iterate over each task and calculate the details
        for task_description in tasks:
            # Predict the time duration for the task
            time_duration_hours = self.predict_task_duration(task_description)
            # Get the current date and time
            current_date = datetime.now()
            # Estimate the finished date for the task
            finished_date = self.estimate_finished_date(current_date, time_duration_hours)
            # Append the details to the list
            task_details.append({
                'Task': task_description,
                'Predicted_Duration_Hours': time_duration_hours,
                'Current_Time': current_date.strftime("%Y-%m-%d %H:%M:%S"),
                'Estimated_Finished_Date': finished_date.strftime("%Y-%m-%d %H:%M:%S"),
            })

        # Create a DataFrame from the task details
        task_df = pd.DataFrame(task_details)
        return task_df

