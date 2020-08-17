import numpy as np

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()

base.prepare(engine, reflect=True)

measurement = base.classes.measurement
station = base.classes.station


#flask setup
app = Flask(__name__)


@app.route("/")
def home():
    return (
        f"Welcome!<br/>"
        f"Available API Routes:<br/>"
        f"____________________________<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results =   session.query(measurement.date, measurement.prcp).\
                order_by(measurement.date).all()

    #list of dictionaries
    date_list = []

    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        date_list2.append(new_dict)
    session.close()
    return jsonify(date_list2)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = {}

    results = session.query(station.station, station.name).all()

    for stat,name in results:
        stations[stat] = name
    session.close()
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    latest_date_query = session.query(measurement.date).order_by(measurement.date.desc()).first()
    
    year_ago = (dt.datetime.strptime(latest_date_query[0],'%Y-%m-%d') - dt.timedelta(days=365))

    results =   session.query(measurement.date, measurement.tobs).\
                    filter(measurement.date >= year_ago).\
                        order_by(measurement.date).all()

    tobs_list = []

    for date, tobs in results:
        dict1 = {}
        dict1[date] = tobs
        tobs_list.append(dict1)

    session.close()

    return jsonify(tobs_list)

@app.route("/api/v1.0/start")
def start():
    session = Session(engine)

    return_list = []

    stations = session.query(measurement.station, func.count(measurement.date)).group_by(measurement.station).\
        order_by(func.count(measurement.date).desc())

    results = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.station == stations[0][0])


    for date, min, max, avg in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)

    session.close()    

    return jsonify(return_list)

@app.route("/api/v1.0/start/end")
def start_end():
    session = Session(engine)
    return "hello world :D"

if __name__ == '__main__':
    app.run(debug=True)