# import necessary libraries
import numpy as np
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
samples_table = Base.classes.samples
otu_table = Base.classes.otu
samples_metadata_table = Base.classes.samples_metadata

# Create our session (link) from Python to the DB
session = Session(engine)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/names')
def name():
    results = samples_table.__table__.columns.keys()
    sample_names = results[1:-1]
    return jsonify(sample_names)

@app.route('/otu')
def otu():
    results = session.query(otu_table.lowest_taxonomic_unit_found).all()
    otu_description = list(np.ravel(results))
    return jsonify(otu_description)

@app.route('/metadata/<sample>')
def metadata(sample):
    sample = sample.strip("BB_")
    sel = [samples_metadata_table.AGE, samples_metadata_table.BBTYPE, samples_metadata_table.ETHNICITY, samples_metadata_table.GENDER, samples_metadata_table.LOCATION, samples_metadata_table.SAMPLEID]
    results = session.query(*sel).filter(samples_metadata_table.SAMPLEID == sample).all()
    sample = list(np.ravel(results))
    sample_metadata ={}
    sample_metadata["AGE"] = sample[0]
    sample_metadata["BBTYPE"] = sample[1]
    sample_metadata["ETHNICITY"] = sample[2]
    sample_metadata["GENDER"] = sample[3]
    sample_metadata["LOCATION"] = sample[4]
    sample_metadata["SAMPLEID"] = sample[5]
    return jsonify(sample_metadata)

@app.route('/wfreq/<sample>')
def wfreq(sample):
    sel = [samples_metadata_table.WFREQ]
    results = session.query(*sel).filter(samples_metadata_table.SAMPLEID == sample).first()
    return str(results[0])

@app.route('/samples/<sample>')
def sample_otu(sample):
    results = session.query(samples_table).statement
    df = pd.read_sql_query(results, session.bind)
    df = pd.DataFrame(df, columns=['otu_id', sample])
    df = df[(df[[sample]] != 0).all(axis=1)]
    #Sort your Pandas DataFrame (OTU ID and Sample Value)in Descending Order by Sample Value
    df = df.sort_values(by=sample, ascending=False)
    sample_otu_result = {"otu_ids": df['otu_id'].values.tolist(),"sample_values": df[sample].values.tolist()}
    sample_otu_list = list(np.ravel(sample_otu_result))
    return jsonify(sample_otu_list)

if __name__ == "__main__":
    app.run()



