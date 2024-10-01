import subprocess
import sys
try:
    from flask import Flask, render_template, request, jsonify
    from sqlalchemy import create_engine, func
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.automap import automap_base
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sqlalchemy'])
finally:
    from flask import Flask, render_template, request, jsonify
    from sqlalchemy import create_engine, func
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.automap import automap_base



Base = automap_base()
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
Base.prepare(engine, reflect=True)
#Table Reference
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


@app.route('/')
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Query the last 12 months of precipitation data
    session = Session()
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    precip_data = {date: prcp for date, prcp in results}
    session.close()
    return jsonify(precip_data)

@app.route('/api/v1.0/stations')
def stations():
    session = Session()
    results = session.query(Station.station, Station.name).all()
    session.close()
    # Convert results to a list of dictionaries
    stations_list = [{ "station": station, "name": name } for station, name in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session()
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2017-08-23').all()
    session.close()
    tobs_data = {date: tobs for date, tobs in results}
    return jsonify(tobs_data)

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session()
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    # Convert results to a list of dictionaries
    return jsonify([{"min": result[0], "avg": result[1], "max": result[2]} for result in results])

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    session = Session()
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    # Convert results to a list of dictionaries
    return jsonify([{"min": result[0], "avg": result[1], "max": result[2]} for result in results])

if __name__ == '__main__':
    app.run(debug=True)