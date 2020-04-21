import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/TOBS<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    last_year= dt.datetime(2017,8,23)-dt.timedelta(days=365)
    percep_out= session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= last_year).all()
    results_dict= [{element[0]:element[1]} for element in percep_out]
    return jsonify(results_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    station_nm = session.query(Station.station).all()
    stations = list(np.ravel(station_nm))

    return jsonify(stations)

@app.route("/api/v1.0/TOBS")
def TOBS():
    last_year= dt.datetime(2017,8,23)-dt.timedelta(days=365)
    temp_observ = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= last_year).all()
    temp_results = list(np.ravel(temp_observ))

    return jsonify(temp_results)

@app.route("/api/v1.0/<start>")
def start_date(start=None):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def temp_date(start=None,end=None):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
