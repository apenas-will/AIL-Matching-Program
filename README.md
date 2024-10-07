# AIL Matching Program

## :mag: Overview

This Python project automates the process of pairing teachers (Titulares) with students (Suplentes) for the NGO International Linguistics Academia Julia Lopes de Almeida (AIL), based on various criteria, such as language preferences, availability, and literary interests. Using the Gale-Shapley algorithm, it finds optimal matches, generates output files for communication and record-keeping, and provides a user-friendly interface to select the input CSV file containing the data.

## :jigsaw: Features

- **Teacher-Student Compatibility Matching**: 
  - Matches teachers with students based on criteria like availability, language preferences, and literary interests.
  - Uses a weighted scoring system to determine compatibility.
  - Based on [OKCupid algorithm](https://youtu.be/m9PiPlRuy6E?si=QHwFv_NZ_BnlTrgJ).
  
- **Gale-Shapley Algorithm**: 
  - Implements the [Gale-Shapley algorithm](https://youtu.be/Qcv1IqHWAzg?si=bCLXhHpuMO13UDGH) to find stable matches for teachers and students, prioritizing the best students for the teachers.

- **CSV Output Generation**:
  - Outputs three different CSV files:
    1. A list of students paired with their respective teachers, formatted for automatic email systems.
    2. A list of teachers and their students, formatted for automatic email systems.
    3. A summary for class records.

## :clipboard: How to Use

### :white_check_mark: Prerequisites
Ensure you have Python 3 installed along with the following libraries:
- `csv`
- `tkinter`

### :page_with_curl: Instructions

1. **Run the Script**:
   - The script begins by opening a file dialog window, allowing you to select the CSV file containing the data for teachers and students.
   
2. **Input Data**:
   - The input CSV should contain the following fields:
     - Column 4: Role of the person as Teacher (Titular) or Student (Suplente).
     - Column 6, 7, 8: Proficiency level, Time availability, and literary preferences for students.
     - Column 9, 11, 12, 13: Language proficiency, availability, and literary preferences for teachers.

3. **Compatibility Matching**:
   - The script calculates compatibility based on time availability and literary preferences, scoring the match, and sorts preferences accordingly, based on [OKCuid algorithm](https://youtu.be/m9PiPlRuy6E?si=QHwFv_NZ_BnlTrgJ) of compatibility analysis.

4. **Pairing**:
   - The [Gale-Shapley algorithm](https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm) pairs teachers with students, optimizing for the most compatible matches.

5. **Generate Output**:
   - Once the matching process is complete, the script generates the following CSV files:
     - `tabela suplentes.csv`: Contains the list of students and their paired teacher.
     - `tabela titulares.csv`: Contains the list of teachers and their students.
     - `resumo para diários de classe.csv`: A class record summary for teachers.

6. **Completion**:
   - After generating the output files, the program will print "Pareamento concluído" (Pairing complete).

### CSV Structure Example

The input CSV should follow this structure:
```
ID, Name, Email, Phone, Role, Language, Availability, Literary Preferences, Language to Teach, Number of Students, Proficiency of the students, Availability, Literary Preferences
```
- Teachers should be marked as "Titular" and students as "Suplente" in the `Role` column.

## :file_folder: Output Files

- **`tabela suplentes.csv`**: A list of students (Suplentes) paired with their respective teacher.
- **`tabela titulares.csv`**: A list of teachers (Titulares) and their students.
- **`resumo para diários de classe.csv`**: A detailed summary for class records, listing each teacher's students.

## :spiral_notepad: Notes

- The program ensures that each teacher gets the desired number of students based on availability and interests.
- The pairing process is repeated until all teachers are matched with the required number of students.

## :balance_scale: License

This project is open-source and available under the MIT License. Feel free to use and modify it for your needs!