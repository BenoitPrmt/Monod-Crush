from flask import render_template 
  
def not_found(e): 
  
  return render_template("error/all_error.html", error_code = 404) #a modifier pour recuperer le numéro de l'erreur

