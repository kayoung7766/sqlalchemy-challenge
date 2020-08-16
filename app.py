# import Flask
from flask import Flask, jsonify
# import sqlalchemy stuff
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement=Base.classes.measurement
Station=Base.classes.station

session = Session(engine)

# Create an app
app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    session=Session(engine)
    return (
    f"The available routes are:<br/>"
    f"Perciptiation: /api/v1.0/precipitation<br/>"
    f"Stations: /api/v1.0/stations<br/>"
    f"Temperature Obserations(tobs): /api/v1.0/tobs<br/>"
    f"Min, Max, and Average Temperature for a Date: /api/v1.0/<start><br/>"
    f"Min, Max, and Average Temperature for Range: /api/v1.0/<start>/<end>")


# Percipitation
@app.route("/api/v1.0/precipitation")
def percipitation():
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#The query
    percip_date=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date>=query_date).all()
#making a list
    precip_list = {date: prcp for date, prcp in percip_date}

    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    stations=session.query(Station).all()

    station_list = []

    for x in stations:
        station_dict = {}
        station_dict["station"]=x.station
        station_dict["name"] = x.name
        station_dict["latitude"] = x.latitude
        station_dict["longitude"] = x.longitude
        station_dict["elevation"] = x.elevation
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature():
    session=Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #Get the query of the data
    station_temperature=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date>=query_date).all()
    
    return jsonify(station_temperature)

@app.route("/api/v1.0/<start>")
def single_date(start):
    session=Session(engine)

    temperature_date= session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    
    one_date = []

    for i in temperature_date:
        one_date_dict = {}
        one_date_dict["Min Temperture"] = temperature_date[0][0]
        one_date_dict["Avg Temperature"] = temperature_date[0][1]
        one_date_dict["Max Temperature"] = temperature_date[0][2]
        one_date.append(one_date_dict)

    return jsonify(one_date)
@app.route("/api/v1.0/<start>/<end>")
def multiple_date(start, end):
    session=Session(engine)

    two_temperature_date= session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    two_date = []

    for i in two_temperature_date:
        two_date_dict = {}
        two_date_dict["Min Temperture"] = two_temperature_date[0][0]
        two_date_dict["Avg Temperature"] = two_temperature_date[0][1]
        two_date_dict["Max Temperature"] = two_temperature_date[0][2]
        two_date.append(two_date_dict)

    return jsonify(two_date)

if __name__ == "__main__":
    app.run(debug=True)
