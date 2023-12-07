# MODULE 10 CHALLENGE 
# Levar McKnight
# Data Analytics Bootcamp


#################################################
# Dependencies
#################################################
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# Reflect the tables
Base.classes.keys()


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__) 

#################################################
# Flask Routes
#################################################
# Home Route
@app.route("/")
def home():
    return(
        f"<center><h2>Welcome to the Hawaii Climate Analysis Local API!</h2>"
        f"<h3>Please select one of the available routes:</h3><br>"
        f"<b>Precipitation:</b> &#20; /api/v1.0/precipitation<br>"
        f"<b>Stations:</b> &#20; /api/v1.0/stations<br>"
        f"<b>Temperature Observations:</b> &#20; /api/v1.0/tobs<br>"
        f"<b>< Start > and < Start >< End > (MMDDYYYY/MMDDYY):</b> &#20; /api/v1.0/start/end</center>"
        )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precip():
    # Return the previous year's precipitation as a json
    previousYear = dt.date(2017,8,23) - dt.timedelta(days=365) 
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previousYear).all()
    session.close()
    # Dictionary with the date as the key and prcp as the value
    precipitation = {date:prcp for date, prcp in results}
    # Convert to json
    return jsonify(precipitation)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    # List of stations
    # Perform a query to retrieve the names of the stations
    results = session.query(Station.station).all()
    session.close()
    # Convert results to a list
    stationList = list(np.ravel(results))
    # Convert to a json
    return jsonify(stationList)

# Temperature Observations Route
@app.route("/api/v1.0/tobs")
def temperatures():
    # Return the previous year's precipitation as a json
    previousYear = dt.date(2017,8,23) - dt.timedelta(days=365) 
    # Perform a query to retrieve the temperatures from the most active station from the past year
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= previousYear).all()  
    session.close()
    # Convert results to a list
    tempList = list(np.ravel(results))
    # Convert to a json
    return jsonify(tempList)

# <Start> and <Start><End> Routes
@app.route("/api/v1.0/<start>/")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):
    # Selection statement
    selection = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # If there is no end date, return all temperatures on and after the start date
    if not end:
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*selection).filter(Measurement.date >= startDate).all()
        session.close()
        # Convert results to a list
        tempList = list(np.ravel(results))
        # Convert to a json
        return jsonify(tempList)
    else:
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")
        results = session.query(*selection)\
            .filter(Measurement.date >= startDate)\
            .filter(Measurement.date <= endDate).all()
        session.close()
        # Convert results to a list
        tempList = list(np.ravel(results))
        # Convert to a json
        return jsonify(tempList)

#################################################
# App Launcher
#################################################
if __name__ == '__main__':
    app.run(debug=True)





