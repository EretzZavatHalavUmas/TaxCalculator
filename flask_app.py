from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import tz
from taxCalculator import *
import os
from send_email import send_email
import pymysql

# from sqlalchemy.sql import func
# from requests import get
# import urllib.request


app = Flask(__name__)
app.secret_key = 'random string'
app.config[
    "SQLALCHEMY_DATABASE_URI"] = 'mysql://Ron:MREngineering1$@data2.chto6pl4dabw.us-east-2.rds.amazonaws.com:3306/data2inputs'
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    date_ = db.Column(db.String(40))
    time_ = db.Column(db.String(40))
    salary_ = db.Column(db.Integer())
    nz_ = db.Column(db.Float())
    salary2_ = db.Column(db.Float())
    nz2_ = db.Column(db.Float())
    rent_ = db.Column(db.Integer())
    arnona_ = db.Column(db.Integer())
    expanses_ = db.Column(db.Integer())
    gasoline_ = db.Column(db.Integer())
    car_ = db.Column(db.Integer())
    car2_ = db.Column(db.Integer())
    totalDirectTax_ = db.Column(db.Float())
    totalDirectTaxPer_ = db.Column(db.Float())
    totalTax_ = db.Column(db.Float())
    totalTaxPer_ = db.Column(db.Float())

    def __init__(self, date_, time_, salary_, nz_, salary2_, nz2_, rent_, arnona_, expanses_, gasoline_, car_, car2_, totalDirectTax_, totalDirectTaxPer_,  totalTax_, totalTaxPer_):
        self.date_ = date_
        self.time_ = time_
        self.salary_ = salary_
        self.nz_ = nz_
        self.salary2_ = salary2_
        self.nz2_ = nz2_
        self.rent_ = rent_
        self.arnona_ = arnona_
        self.expanses_ = expanses_
        self.gasoline_ = gasoline_
        self.car_ = car_
        self.car2_ = car2_
        self.totalDirectTaxPer_ = totalDirectTaxPer_
        self.totalDirectTax_ = totalDirectTax_
        self.totalTax_ = totalTax_
        self.totalTaxPer_ = totalTaxPer_


port = int(os.environ.get("PORT", 5000))


@app.route("/calc")
def calc():
    return render_template("calc.html")


@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        
        salary = float(request.form["salary"])
        nz = float(request.form["nz"])
        salary2 = request.form.get("salary2") #when it's disabled, the default type is Nonetype
        nz2 = request.form.get("nz2") #when it's disabled, the default type is Nonetype

        #if it gets a value for salary2 and nz2 it converts them to float
        if(salary2):
            salary2 = float(salary2)
            nz2 = float(nz2)

        rent = float(request.form["rent"])
        arnona = float(request.form["arnona"])
        expanses = float(request.form["expanses"])
        car = float(request.form["car"])
        car2 = request.form.get("car2") #when it's disabled, the default type is Nonetype

        #if it gets a value for car2 convert it to float
        if(car2):
            car2 = float(car2)

        gasoline = float(request.form["gasoline"])
        mh = MH(salary,nz)
        pension = salary*0.185
        bl, bb = BL(salary)

        totalSalary = salary
        #when it gets 2 salaries
        if(salary2):
            mh2 = MH(salary2,nz2)
            bl2, bb2 = BL(salary2)
            print(mh2,bl2,bb2)
            print('1')
            mh = mh + mh2
            bl = bl+bl2
            bb = bb+bb2
            totalSalary += salary2

        vat = VAT(expanses,gasoline)
        gasTax = gasolineTax(gasoline)
        carTax = carTaxCalc(car)

        #if it gets a value for salary2 and nz2 it converts them to float
        if(car2):
            carTax += carTaxCalc(car2)

        totalExpanseTax = vat+gasTax+carTax+arnona
        totalDirectTax = mh+bl+bb
        totalTax = totalDirectTax + totalExpanseTax
        totalDirectTaxPer = totalDirectTax/(totalSalary)*100
        totalTaxPer = totalTax/(totalSalary)*100

        now = datetime.now()
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Jerusalem')
        now = now.replace(tzinfo=from_zone)
        now = now.astimezone(to_zone)
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")
        data = Data(date, time, salary, nz, salary2, nz2, rent, arnona, expanses, gasoline, car, car2, totalDirectTax, totalDirectTaxPer, totalTax, totalTaxPer)
        db.session.add(data)
        db.session.commit()

        return render_template("success.html",
                               mhText="mas haknasa is %s ILS " % round(mh),
                               blText="bituh leumi is %s ILS " % round(bl),
                               bbText="bituh briut is %s ILS " % round(bb),
                               vatText="expanses Tax is %s ILS " % round(vat),
                               gasolineText="gas Tax is %s ILS " % round(gasTax),
                               carText="car Tax is %s ILS" % round(carTax),
                               totalDirectTaxText="המיסים הישירים - ₪ %s "
                                                  % round(totalDirectTax),
                               totalDirectTaxPerText="שמהווים כ-%% %s מההכנסה"
                                                     % round(totalDirectTaxPer),
                               totalTaxText="סך כל המיסים - ₪ %s "
                                            % round(totalTax),
                               totalTaxPerText="שמהווים כ-%% %s מההכנסה"
                                               % round(totalTaxPer),
                               DATA=[['Category', 'ILS'],
                                     ['מס הכנסה',
                                      round(mh)],
                                     ['ביטוח לאומי',
                                      round(bl)],
                                     ['ביטוח בריאות',
                                      round(bb)]
                                     ],
                               DATA2=[['Category', 'ILS'],
                                      ['מס הכנסה', round(mh)],
                                      ['ביטוח לאומי', round(bl)],
                                      ['ביטוח בריאות', round(bb)],
                                      ['מע"מ', round(vat)],
                                      ['מס בלו', round(gasTax)],
                                      ['מס על רכב', round(carTax)],
                                      ['ארנונה', round(arnona)]
                                      ],
                               DATA3=[['Category', 'ILS'],
                                      ['מס הכנסה', round(mh)],
                                      ['ביטוח לאומי', round(bl)],
                                      ['ביטוח בריאות', round(bb)],
                                      ['מע"מ', round(vat)],
                                      ['מס בלו', round(gasTax)],
                                      ['מס על רכב', round(carTax)]
                                      ])


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        content = (request.form["contact-text"])
        print(content)
        print(type(content))
        if(send_email(content)):
            flash('Email sent successfully!')
            return render_template('contact.html')
        else:
            flash("Error, your email wasn't delivered !")
            return render_template('contact.html')
    return render_template("contact.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    # app.run()
