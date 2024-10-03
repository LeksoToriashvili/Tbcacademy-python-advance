import pandas as pd
from matplotlib import pyplot as plt


class DataProcessor:
    """
    A class to process student data in a DataFrame.

    Attributes:
        dataframe (pd.DataFrame): The DataFrame containing student data.
    """
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initializes the DataProcessor with a DataFrame.

        Args:
            dataframe (pd.DataFrame): The DataFrame to process.
        """
        self._df = dataframe

    def students_below_threshold(self, threshold):
        """
        Returns students who scored below a specified threshold in any subject.

        Args:
            threshold (float): The score threshold.
        """
        condition = (self._df[['Math', 'Physics', 'Chemistry', 'Biology', 'English']] < threshold) & \
                    ~self._df[['Math', 'Physics', 'Chemistry', 'Biology', 'English']].isna()
        students_below_50 = self._df[condition.any(axis=1)]

        return students_below_50

    @property
    def student_below_50(self):
        """Returns students who scored below 50 in any subject."""
        return self.students_below_threshold(50)

    @property
    def subject_average_score_by_semester(self):
        """Returns average score for each subject by semester"""
        return self._df.groupby('Semester').mean(numeric_only=True)

    @property
    def students_with_highest_scores_method_1(self):
        """Returns student with highest average score with all subjects studied"""
        average_scores = self._df.groupby('Student').mean(numeric_only=True)
        average_scores['Overall_Average'] = average_scores.mean(axis=1)
        average_scores = average_scores.dropna()
        highest_average_score = average_scores['Overall_Average'].max()
        top_students = average_scores[average_scores['Overall_Average'] == highest_average_score]
        return top_students

    @property
    def students_with_highest_scores_method_2(self):
        """Returns student with highest average score without all subjects studied"""
        average_scores = self._df.groupby('Student').mean(numeric_only=True)
        average_scores['Overall_Average'] = average_scores.mean(axis=1)
        highest_average_score = average_scores['Overall_Average'].max()
        top_students = average_scores[average_scores['Overall_Average'] == highest_average_score]
        return top_students

    @property
    def difficult_subject(self):
        """Returns most difficult subject, wich means lowest average score in that subject."""
        average_scores = self._df[['Math', 'Physics', 'Chemistry', 'Biology', 'English']].mean()
        lowest_average_subject = average_scores.idxmin()
        lowest_average_score = str(average_scores.min())
        return f'{lowest_average_subject} with average score of {lowest_average_score}'

    def subject_average_scores_save_to_xlsx(self, filename='average_scores.xlsx'):
        """
        Stores average scores for each subject by semester.
        :param filename: filename, where the average scores are saved in xlsx format.
        :return: 'success' on success, otherwise returns error message.
        """
        average_by_semester = self.subject_average_score_by_semester
        try:
            average_by_semester.to_excel(filename, sheet_name='Averages', index=True, header=True)
            return 'success'
        except Exception as e:
            return e

    def plot_subjects_diagram(self):
        """Plots total average scores by subject."""
        average_by_semester = self.subject_average_score_by_semester
        average_by_semester = average_by_semester.mean(numeric_only=True)
        average_by_semester.plot(kind='bar')
        plt.title('Average subjects scores in all semester')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_scores_graph(self):
        """Plots total average scores by semester."""
        df = self._df
        df['Overall_Average'] = df[['Math', 'Physics', 'Chemistry', 'Biology', 'English']].mean(axis=1, skipna=True)
        average_by_semester = df.groupby('Semester')['Overall_Average'].mean()
        average_by_semester.plot(kind='line', marker='o')
        plt.title('Average all subjects scores by semester')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
