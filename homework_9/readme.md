# Student Data Processing

This project contains classes to load and process student data from CSV files. The main classes included are `CSVLoader` for loading data and `DataProcessor` for analyzing and visualizing the data.

## Table of Contents

### CSVLoader Class
The CSVLoader class is responsible for loading student data from a specified CSV file into a pandas DataFrame. It provides feedback on the loading status.

- Attributes:  
filename (str): Path to the CSV file.  
dataframe (pd.DataFrame): DataFrame containing the loaded data.  
status (str): Message indicating the success or failure of the loading process.  
- Methods:  
__init__(filename=None): Initializes the class with an optional filename.  
load(): Loads data from the specified CSV file.

### DataProcessor Class
The DataProcessor class processes the loaded student data and provides various methods to analyze and visualize it.

- Attributes:
dataframe (pd.DataFrame): The DataFrame containing student data.
- Methods:  
__init__(dataframe: pd.DataFrame): Initializes with a DataFrame.  
students_below_threshold(threshold): Returns students who scored below the specified threshold in any subject.  
student_below_50: Property that returns students who scored below 50.  
subject_average_score_by_semester: Returns average scores for each subject by semester.  
students_with_highest_scores_method_1: Returns the student(s) with the highest average score across all subjects.  
difficult_subject: Identifies the subject with the lowest average score.  
subject_average_scores_save_to_xlsx(filename): Saves average scores to an Excel file.  
plot_subjects_diagram(): Plots a bar diagram of average subject scores.  
plot_scores_graph(): Plots a line graph of overall average scores by semester.  

## Installation

To use the classes in this project, you need to have Python, pandas, and Matplotlib installed. You can install the required packages using pip:

```bash
pip install pandas matplotlib