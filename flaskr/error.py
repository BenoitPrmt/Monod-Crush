from flask import render_template 

def not_found(e): 
  '''retourner le numéro de l'erreur et afficher la page all_error.html'''

  number = []
  e = str(e).split(" ") #split e pour isoler le numéro
  number.append(e)

  return render_template("error/all_error.html", error_code = e[0]) #revoi la page d'erreur et e[0] = numéro erreur

