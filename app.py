# import Flask
from flask import Flask, jsonify
# import sqlalchemy stuff
import sqlalchemy
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
    return (
    f"The available routes are:<br/>"
    f"Perciptiation: /api.v1.0/precipitation<br/>"
    f"Stations: /api.v1.0/stations<br/>"
    f"Temperature Obserations(tobs): /api.v1.0/tobs<br/>"
    f"Min, Max, and Average Temperature for Range: /api.v1.0/<start> and /api v1.0/<start>/<end>")


# Percipitation
@app.route("/api.v1.0/precipitation")
def percipitation():
    return ("?")


if __name__ == "__main__":
    app.run(debug=True)
