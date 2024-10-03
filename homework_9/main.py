from loader import CSVLoader
from data_processor import DataProcessor

FILENAME = "student_scores_random_names.csv"


def main():
    """
    Demonstrates CSVLoader and DataProcessor classes.
    CSVLoader class loads data from csv file and saves it to pandas dataframe.
    DataProcessor class takes pandas dataframe, generated from CSVLoader and processes different data.
    """
    loader = CSVLoader(FILENAME)
    loader.load()

    if loader.status == "success":
        dp = DataProcessor(loader.dataframe)
    else:
        raise Exception("file not loaded")

    print("\nstudents with scores less than 50:")
    print(dp.student_below_50)

    print("\naverage score for each subject by semester:")
    print(dp.subject_average_score_by_semester)

    print("\nstudent with highest average score:")
    print(dp.students_with_highest_scores_method_1)

    print("\nmost difficult subject:")
    print(dp.difficult_subject)

    if dp.subject_average_scores_save_to_xlsx('average_scores.xlsx') == 'success':
        print("\nfile saved successfully\n")

    dp.plot_subjects_diagram()
    dp.plot_scores_graph()


if __name__ == "__main__":
    main()
