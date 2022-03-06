from flask import Flask, render_template 
  
app = Flask(__name__) 
  
@app.errorhandler(404) 
  
def not_found(e): 
  
  return render_template("error_404.html") 