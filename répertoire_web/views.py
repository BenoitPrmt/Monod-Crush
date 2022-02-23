from flask import Flask, render_template, request

app = Flask(__name__)
ADRESSE_IP="127.0.0.1"
@app.route('/')
def index():
 return render_template('index.html')

@app.route('/resultat',methods = ['GET'])
def resultat():
  result=request.args
  n = result['nom']
  p = result['prenom']
  return render_template("result.html", nom=n, prenom=p)

app.run(debug=True,host=ADRESSE_IP,port="5002")
