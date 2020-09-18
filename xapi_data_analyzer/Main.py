import GlobalData
from ElementCollection import ElementCollection
import pandas as pd
import PySimpleGUI as sg
from datetime import datetime
import pytz


def create_main_window():
    layout = [
        [sg.Text("UW-Madison xAPI Data Analyzer", font="Any 15 bold")],
        [sg.Text("Please select the cleaned xAPI data .csv file from the DoIT Learning Locker "
                 "(usually called dataMM-DD-YY(cleaned).csv)")],
        [sg.FileBrowse(key="FILEIN")],
        [sg.Text("Next, please enter a comma-separated list of the H5P element ID numbers you would like to be "
                 "included in the box below.")],
        [sg.InputText(size=(20, 1), key="IDLIST")],
        [sg.Text("Two files will be saved to the current directory:")],
        [sg.Text("xAPI-Data-Analyzer_$TIMESTAMP.csv and StudentDurations_$TIMESTAMP.csv", font="Any 10 bold")],
        [sg.Button("Go", size=(4, 1)), sg.Exit()]
    ]
    return sg.Window("xAPI Data Analyzer", layout, element_justification="center")


def main():
    sg.theme("SystemDefault")

    main_window = create_main_window()
    while True:
        event, values = main_window.read()

        if event in ("Exit", None):
            break

        if event == "Go":
            try:
                # Parse the ID list
                id_list = values["IDLIST"].split(",")
                id_list = [int(item.strip()) for item in id_list]

                GlobalData.set_data_vars(values["FILEIN"])

                # Generate a timestamp + ElementCollection object and crank out the two CSVs
                timestamp = datetime.now(pytz.timezone("America/Chicago"))
                element_collection = ElementCollection(id_list, GlobalData.raw_data, GlobalData.class_list)
                element_collection.get_dataframe().to_csv("xAPI-Data-Analyzer_" + str(timestamp) + ".csv")

                print(element_collection.get_students_duration())
                df_students = pd.DataFrame.from_dict(element_collection.get_students_duration(), orient='index')
                df_students.to_csv("StudentDurations_" + str(timestamp) + ".csv")

                sg.Popup("All files successfully saved!", title="Success!")

            except KeyError as e:
                # FIXME for some reason this error is always thrown, even for valid keys.
                sg.Popup("ERROR: The following H5P element was not found: " + str(e.args[0]), title="Error")
            except FileNotFoundError:
                sg.Popup("ERROR: Data file not found! Please double-check the path to the data file and try again.",
                         title="Error")

    main_window.close()


main()
