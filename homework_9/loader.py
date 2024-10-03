import pandas as pd


class CSVLoader:
    """
    A class to load a CSV file into a pandas DataFrame.

    Attributes:
        filename (str): The path to the CSV file.
        dataframe (pd.DataFrame): The DataFrame containing the loaded data.
        status (str): Status message regarding the loading process.
    """
    def __init__(self, filename=None):
        """
        Initializes the CSVLoader with an optional filename.

        Args:
            filename (str, optional): The path to the CSV file.
        The filename can be set later.
        """
        self.filename = filename
        self.dataframe = None
        self.status = "CSVLoader initialized"

    def load(self):
        """Loads the CSV file into a pandas DataFrame."""
        try:
            self.dataframe = pd.read_csv(self.filename)
            self.status = "success"
        except FileNotFoundError:
            self.status = "CSVLoader file not found"
        except Exception as e:
            self.status = str(e)
