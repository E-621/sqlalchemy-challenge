#Import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

############################################# Flask Routes##################################################
#Route to home page
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year @ most active station: /api/v1.0/tobs<br/>"
        f"Temperature from start date[format as (yyyy-mm-dd)]: /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature from start to end dates[format as (yyyy-mm-dd)]: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

#Route to precipitation
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    sel = [Measurement.date,Measurement.prcp]
    result = session.query(*sel).all()
    session.close()

    precipitation = []
    for date, prcp in result:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

#Route to stations
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    sel = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    result = session.query(*sel).all()
    session.close()

    stations = []
    for station,name,lat,lon,el in result:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

#Route to last year of data
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    result = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= '2016-08-23', Measurement.station=="USC00519281").all()
    session.close()

    tobsall = []
    for date, tobs in result:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)

    return jsonify(tobsall)

#Route to start date data
@app.route('/api/v1.0/<start>')
def start_date(start):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    start_tobs = []
    for min,avg,max in result:
        start_tobs_dict = {}
        start_tobs_dict["Min"] = min
        start_tobs_dict["Average"] = avg
        start_tobs_dict["Max"] = max
        start_tobs.append(start_tobs_dict)

    return jsonify(start_tobs)

#Route to date range data
@app.route('/api/v1.0/<start>/<stop>')
def start_stop_date(start,stop):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    start_stop_date_tobs = []
    for min,avg,max in result:
        start_stop_tobs_dict = {}
        start_stop_tobs_dict["Min"] = min
        start_stop_tobs_dict["Average"] = avg
        start_stop_tobs_dict["Max"] = max
        start_stop_date_tobs.append(start_stop_tobs_dict)

    return jsonify(start_stop_date_tobs)

if __name__ == '__main__':
    app.run(debug=True)