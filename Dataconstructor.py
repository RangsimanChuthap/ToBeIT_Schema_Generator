"""CSV Data constructor"""
import csv
from traceback import print_exc
import tkinter as tk
from tkinter.filedialog import askopenfilename
from ctypes import windll
from shutil import copyfile
from os import remove, path

# STOP WINDOWS FROM BLURRING THE GUI
windll.shcore.SetProcessDpiAwareness(1)

wingui = tk.Tk()
wingui.title("Chose CSV file to open")
wingui.withdraw()

datasheet = askopenfilename(
    title="Chose a file to open",
    filetypes=[("CSV file", "*.csv"), ("All file", "*.*")]
)

print("opening", datasheet)
TEMPFILENAME = "tempgenerator.csv"
SANITIZEDFILENAME = "SCHEMA.csv"

try:
    if path.exists(TEMPFILENAME):
        print(f"Warning! temp file detected, this program doesnt know what temp file it belong to "
        f"but continuing meant the program will overriding the existing {TEMPFILENAME} in this"
        f"directory, continue? (Y/N)")
        action = input().lower()

        while action != "y":
            if action == "n":
                print("Process aborted due to temp file conflict")
                raise SystemExit
            else:
                action = input().lower()

    with open(datasheet, 'r', encoding="UTF-8") as regis_data:
        reader = csv.reader(regis_data)
        startcount = 1

        # In case of น้อนๆ ค่ายเกิน 9999 คน
        csv_len = (sum(1 for line in regis_data) // 10) + 1
        reserve_digit = max(csv_len, 4)
        regis_data.seek(0,0)

        # Use TEMP csv to prevent corruptinf existing schema
        with open(TEMPFILENAME, 'w', encoding="UTF-8", newline="") as temp_csv:
            writer = csv.writer(temp_csv)

            writer.writerow(["usernane", "firstname", "lastname"])

            header = regis_data.readline().strip().split(",")
            
            nameindex = [None,None]
            validnamedict = {0: ["firstname", "name", "ชื่อ", "ชื่อจริง"],
                            1: ["lastname", "สกุล", "นามสกุล", "surname"]}

            for index , item in enumerate(header):
                itemhead = item.lower().replace(" ", "").replace("_", "").replace("-","")
                for key, value in validnamedict.items():
                    for reftable in value:
                        if itemhead == reftable:
                            nameindex[key] = index if not nameindex[key] else \
                            print("DUPLICATE KEY DETECTED, COULD NOT GENERATE SCHEMA")

            if None in nameindex:
                print("Name or last name field DIDN'T FOUND, COULD NOT GENERATE SCHEMA")
                raise SystemExit

            try:
                temp_csv.truncate()
                for line in reader:
                    constructed_data = [f'tobeit70{startcount:0{reserve_digit}d}',"??","??"]
                    constructed_data[1] = line[nameindex[0]]
                    constructed_data[2] = line[nameindex[1]]
                    startcount += 1
                    writer.writerow(constructed_data)

                temp_csv.flush()
                copyfile(TEMPFILENAME, SANITIZEDFILENAME)
                print("Operation executed successfully!")
                print(f"SCHEMA generated successfully in '{SANITIZEDFILENAME}'")

            except Exception:
                print("Exception has occured!")
                print(print_exc())

except UnicodeDecodeError:
    print("Cannot open file, perhaps due to wrong format?")

except FileNotFoundError:
    print("File not found? perhaps you didn't select a file or pointed toward nonexistance file")

finally:
    remove(TEMPFILENAME)
