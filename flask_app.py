from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import tz
from taxCalculator import *
import os
from send_email import send_email
import pymysql
#from sqlalchemy.sql import func
#from requests import get
#import urllib.request


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='mysql://Ron:MREngineering1$@data2.chto6pl4dabw.us-east-2.rds.amazonaws.com:3306/data2inputs'
db=SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    date_ = db.Column(db.String(40))
    time_ = db.Column(db.String(40))
    salary_ = db.Column(db.Integer())
    nz_ = db.Column(db.Float())
    rent_ = db.Column(db.Integer())
    arnona_ = db.Column(db.Integer())
    expanses_ = db.Column(db.Integer())
    gasoline_ = db.Column(db.Integer())
    car_ = db.Column(db.Integer())
    totalDirectTax_ = db.Column(db.Float())
    totalDirectTaxPer_ = db.Column(db.Float())
    totalTax_ = db.Column(db.Float())
    totalTaxPer_ = db.Column(db.Float())
    content_ = db.Column(db.Text())

    def __init__(self, date_, time_, salary_, nz_, rent_, arnona_, expanses_, gasoline_, car_, totalDirectTax_, totalDirectTaxPer_,  totalTax_, totalTaxPer_, content_):
        self.date_ = date_
        self.time_ = time_
        self.salary_ = salary_
        self.nz_ = nz_
        self.rent_ = rent_
        self.arnona_ = arnona_
        self.expanses_ = expanses_
        self.gasoline_ = gasoline_
        self.car_ = car_
        self.totalDirectTaxPer_ = totalDirectTaxPer_
        self.totalDirectTax_ = totalDirectTax_
        self.totalTax_ = totalTax_
        self.totalTaxPer_ = totalTaxPer_
        self.content_ = content_

port = int(os.environ.get("PORT", 5000))
        
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        
        salary = float(request.form["salary"])
        nz = float(request.form["nz"])
        rent = float(request.form["rent"])
        arnona = float(request.form["arnona"])
        expanses = float(request.form["expanses"])
        gasoline = float(request.form["gasoline"])
        car = float(request.form["car"])
        content = str(request.form["content"])
        
        #send_email(content)
            
        mh = MH(salary,nz)
        pension = salary*0.185
        bl, bb = BL(salary)
        vat = VAT(expanses,gasoline)
        gasTax = gasolineTax(gasoline)
        carTax = carTaxCalc(car)
        totalExp = (expanses-vat)+(gasoline-gasTax) #calculate car monthly expense
        totalExpanseTax = vat+gasTax+carTax
        totalDirectTax = mh+bl+bb
        netSalary = salary - totalDirectTax - 0.06*salary
        totalTax = totalDirectTax + totalExpanseTax
        totalDirectTaxPer = totalDirectTax/salary*100
        totalTaxPer = totalTax/salary*100

        now = datetime.now()
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Jerusalem')
        now = now.replace(tzinfo=from_zone)
        now = now.astimezone(to_zone)
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")
        data = Data(date, time, salary, nz, rent, arnona, expanses, gasoline, car, totalDirectTax, totalDirectTaxPer, totalTax, totalTaxPer, content)
        db.session.add(data)
        db.session.commit()
        #average_height = db.session.query(func.avg(Data.height_)).scalar()
        #average_height = round(average_height,0)
        #count = db.session.query(Data.height_).count()
        

        return render_template("success.html",
                               mhText="mas haknasa is %s ILS " % round(mh),
                               blText="bituh leumi is %s ILS " % round(bl),
                               bbText="bituh briut is %s ILS " % round(bb),
                               vatText="expanses Tax is %s ILS " % round(vat),
                               gasolineText="gas Tax is %s ILS " % round(gasTax),
                               carText="car Tax is %s ILS" % round(carTax),
                               totalDirectTaxText = "סך כל המיסים הישירים - ₪ %s"
                               % round(totalDirectTax),
                               totalDirectTaxPerText = "שמהווים כ-%% %s מההכנסה"
                               % round(totalDirectTaxPer),
                               totalTaxText = "סך כל המיסים - ₪ %s"
                               % round(totalTax),
                               totalTaxPerText = "שמהווים כ-%% %s מההכנסה"
                               % round(totalTaxPer),
                               DATA = [['Category', 'ILS'],
                                      ['מס הכנסה',
                                      round(mh)],
                                      ['ביטוח לאומי',
                                      round(bl)],
                                      ['ביטוח בריאות',
                                      round(bb)]
                                    ],
                               DATA2 = [['Category', 'ILS'],
                                      ['מס הכנסה',     round(mh)],
                                      ['ביטוח לאומי',      round(bl)],
                                      ['ביטוח בריאות',  round(bb)],
                                      ['מע"מ', round(vat)],
                                      ['מס בלו',    round(gasTax)],
                                      ['מס על רכב',    round(carTax)]
                                    ],
                               DATA3 = [['Category', 'ILS'],
                                      ['מס הכנסה',     round(mh)],
                                      ['ביטוח לאומי',      round(bl)],
                                      ['ביטוח בריאות',  round(bb)],
                                      ['מע"מ', round(vat)],
                                      ['מס בלו',    round(gasTax)],
                                      ['מס על רכב',    round(carTax)]
                                    ])


if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=port)
   #app.run()
