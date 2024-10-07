# Importing libraries
import csv
import tkinter as tk
from tkinter import filedialog

# Choosing file in a user-friendly way
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# Create lists to keep the raw data
tit_list = []  
sup_list = []  

# Create lists to keep the useful data
titulares_par = []  
suplentes_par = []  

# Open file and save the data
with open(file_path, 'r') as csv_file:
  csv_reader = csv.reader(csv_file)

  for row in csv_reader:
    if row[4] == "Titular":
      row[11] = row[11].replace(" ", "").split(';')  # Turn into a list the language proficiency required by the teacher
      row[12] = row[12].replace(" ", "").split(';')  # Turn into a list the teacher's time availability
      row[13] = row[13].replace(" ", "").split(';')  # Turn into a list the teacher's literary preferences

      tit_list.append(row) # Teachers' raw data

      # List of dictionaries with the useful teachers' data for pairing
      titulares_par.append({
          'Nome': tit_list[len(tit_list) - 1][1],
          'Email': tit_list[len(tit_list) - 1][2],
          'Telefone': tit_list[len(tit_list) - 1][3],
          'Idioma': tit_list[len(tit_list) - 1][9],
          'Preferências': [],
          'Quant_sup': int(tit_list[len(tit_list) - 1][10]),
          'Estado': "Dis",
          'Suplentes': [],
          'Tel_suplentes': []
      })

    elif row[4] == 'Suplente':
      row[6] = row[6].replace(" ", "")  # Remove blank spaces of students proficiency level  
      row[7] = row[7].replace(" ", "").split(';')  # Turn into a list the student's time availability
      row[8] = row[8].replace(" ", "").split(';')  # Turn into a list the student's literary preferences 
      
      sup_list.append(row) # Students' raw data
      
      # List of dictionaries with the useful students' data for pairing
      suplentes_par.append({
          'Nome': sup_list[len(sup_list) - 1][1],
          'Email': sup_list[len(sup_list) - 1][2],
          'Telefone': sup_list[len(sup_list) - 1][3],
          'Idioma': sup_list[len(sup_list) - 1][5],
          'Preferências': [],
          'Estado': "Dis",
          'Titular': '',
          'Tel_titular': ''
      })

# Create the teachers' lists of preferences 
for i in tit_list:
  temp = [] # Temporary variable to keep the results before final saving

  # Determine the weights of each variable when crating the preferences
  total_h = len(i[12]) * 4
  total_lit = len(i[13]) * 2
  total_p = (total_h + total_lit) / 2
  Total = total_h + total_p + total_lit

  for j in sup_list:
    if j[5] == i[9]:
      # Determine the compatibility of the teacher with the student
      feito_h = len(set(j[7]).intersection(set(i[12]))) * 4
      feito_lit = len(set(j[8]).intersection(set(i[13]))) * 2
      feito_p = 0
      if j[6] in i[11]:
        feito_p = total_p
      total_feito = feito_h + feito_lit + feito_p
      pont = round((total_feito / Total) * 100, 2)  # Final compatibility

      # Create an ordered list with the preferences based on compatibility
      if len(temp) == 0:
        temp.append({"Nome": j[1], "Comp": pont})
      else:
        for k in temp:
          if k["Comp"] < pont:
            temp.insert(temp.index(k), {"Nome": j[1], "Comp": pont})
            break
          else:
            temp.insert(temp.index(k) + 1, {"Nome": j[1], "Comp": pont})
            break

  # Transfer the list of preferences to the teacher dictionary
  for k in temp:
    titulares_par[tit_list.index(i)]["Preferências"].append(k["Nome"])

# Create the teachers' lists of preferences 
for i in sup_list:
  temp = []
  total_h = len(i[7]) * 4
  total_lit = len(i[8]) * 2
  total_p = (total_h + total_lit) / 2
  Total = total_h + total_p + total_lit

  for j in tit_list:
    if j[9] == i[5]:
      # Determine the compatibility of the student with the teacher
      feito_h = len(set(j[11]).intersection(set(i[6]))) * 4
      feito_lit = len(set(j[12]).intersection(set(i[7]))) * 2
      feito_p = 0
      if i[6] in j[11]:
        feito_p = total_p
      total_feito = feito_h + feito_lit + feito_p
      pont = round((total_feito / Total) * 100, 2)  # Final compatibility

      # Create an ordered list with the preferences based on compatibility
      if len(temp) == 0:
        temp.append({"Nome": j[1], "Comp": pont})
      else:
        for k in temp:
          if k["Comp"] < pont:
            temp.insert(temp.index(k), {"Nome": j[1], "Comp": pont})
            break
          else:
            temp.insert(temp.index(k) + 1, {"Nome": j[1], "Comp": pont})
            break

  # Transfer the list of preferences to the students' dictionary
  for k in temp:
    suplentes_par[sup_list.index(i)]["Preferências"].append(k["Nome"])

quant_par = 0 # Variable that keeps the total of paired teachers

# Create the pairs (or groups) of teachers and students using Gale-Shapley Algorithm
while quant_par != len(titulares_par):
  quant_par = 0

  for i in titulares_par:
    # If the teacher has the desired number of students, assign him as paired 
    if len(i["Suplentes"]) == i["Quant_sup"]:
      i["Estado"] = "Par"
      quant_par += 1

    # If the teacher doesn't have the desired number of students, try to assign a new student to him
    if i["Estado"] == "Dis":
      for j in suplentes_par:
        # If the student is the teacher's current top preference...
        if i['Preferências'] and i["Preferências"][0] == j["Nome"]: 
          # and the student is available to be paired, do the pairing process
          if j["Estado"] == "Dis" and len(i["Suplentes"]) < i["Quant_sup"]:
            j["Estado"] = "Par"
            j["Titular"] = i["Nome"]
            j["Tel_titular"] = i["Telefone"]
            i["Suplentes"].append(j["Nome"])
            i["Tel_suplentes"].append(j["Telefone"])
            i["Preferências"].remove(j["Nome"])
            break

          # If the student is paired, but there is a best teacher available, change the teacher 
          elif j["Estado"] == "Par" and len(i["Suplentes"]) < i["Quant_sup"]:
            if j["Preferências"].index(i["Nome"]) < j["Preferências"].index(j["Titular"]):
              
              for k in titulares_par:
                if j["Titular"] == k["Nome"]:
                  k["Estado"] = "Dis"
                  k["Suplentes"].remove(j["Nome"])
                  k["Tel_suplentes"].remove(j["Telefone"])
                  break

              j["Titular"] = i["Nome"]
              j["Tel_titular"] = i["Telefone"]
              i["Suplentes"].append(j["Nome"])
              i["Tel_suplentes"].append(j["Telefone"])
              i["Preferências"].remove(j["Nome"])
              break

            # Remove the teacher's name of the list of preferences of the student
            elif j["Preferências"].index(i["Nome"]) > j["Preferências"].index(j["Titular"]):
              i["Preferências"].remove(j["Nome"])
              break

# Create output files

# Create a file with the students and their teacher (formatted to an automatics email sending system)
campos_sup = ["Nome", "Email", "Titular", "Tel_titular"]
with open("tabela suplentes.csv", "w", newline="",
          encoding="utf-8") as results_s:
  writer = csv.DictWriter(results_s,
                          fieldnames=campos_sup,
                          restval="",
                          extrasaction="ignore",
                          dialect="excel")
  writer.writeheader()
  writer.writerows(suplentes_par)

# Create a file with the teachers and their students (formatted to an automatic email sending system)
campos_tit = ["Nome", "Email", "Suplentes", "Tel_suplentes"]
with open("tabela titulares.csv", "w", newline="",
          encoding="utf-8") as results_t:
  writer = csv.DictWriter(results_t,
                          fieldnames=campos_tit,
                          restval="",
                          extrasaction="ignore",
                          dialect='excel')
  writer.writeheader()
  writer.writerows(titulares_par)

# Create a file for class records
for i in titulares_par:
  for j in i["Suplentes"]:
    i[f'Suplente {i["Suplentes"].index(j)+1}'] = j

campos_diarios = [
    "Nome", "Email", "Idioma", "Suplente 1", "Suplente 2", "Suplente 3",
    "Suplente 4", "Suplente 5"
]
with open("resumo para diários de classe.csv",
          "w",
          newline="",
          encoding="utf-8") as results_t:
  writer = csv.DictWriter(results_t,
                          fieldnames=campos_diarios,
                          restval="",
                          extrasaction="ignore",
                          dialect='excel')
  writer.writeheader()
  writer.writerows(titulares_par)

print("Pareamento concluído")
