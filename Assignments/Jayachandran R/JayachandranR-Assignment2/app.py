from flask import Flask, request,render_template, url_for
import ibm_db

conn = ibm_db.connect("DATABASE=bludb; HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lhv06993; PWD=u0e19sJ5FZcYvmiu",'','')

check=ibm_db.active(conn)
print(check)
print("Connection successful....")

app = Flask(__name__,template_folder="templates")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/signin',methods=["POST","GET"])
def signin():
   return render_template("signin.html")

@app.route('/addsignin',methods=['POST','GET'])
def addsignin():
    if request.method == "POST":
        email = request.form["email"]
        cpass  = request.form["cpass"]
        
        sql = "SELECT * FROM Sample WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn,sel_sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        name = ibm_db.result(stmt,'NAME')

        if acc:
            if(str(cpass)) == str(acc['CPASS'].strip()):
                return render_template("home.html",msg="Welcome,",name = name)
            else:
                return render_template("signin.html",msg="Invalid E-Mail or Password")

        else:
            return render_template("signup.html",msg="Not a Member SignUp")

@app.route('/signup',methods=['POST','GET'])
def signup(): 
    return render_template("signup.html")

@app.route('/addsignup',methods=["POST","GET"])
def addsignup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form["email"]
        cpass  = request.form["cpass"]
        ccpass = request.form["ccpass"]

        sql = "SELECT * FROM Sample WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn,sel_sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)

        if acc:
            return render_template("signin.html",txt="Your are a Existing User so Sign In")
        
        else:
            ins_sql = "INSERT INTO Sample VALUES(?,?,?,?)"
            pstmt = ibm_db.prepare(conn,ins_sql)
            ibm_db.bind_param(pstmt,1,name)
            ibm_db.bind_param(pstmt,2,email)
            ibm_db.bind_param(pstmt,3,cpass)
            ibm_db.bind_param(pstmt,4,ccpass)

            ibm_db.execute(pstmt)

            return render_template("home.html",msg="Successfully SignedUp")


if __name__ == '__main__':
    app.run(debug=True)
