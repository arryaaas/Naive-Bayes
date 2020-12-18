from flask import Flask, render_template, request
from scripts import *
import os

app = Flask(__name__)

data_train = data_training()

data_positif = data_grouping(data_train, "Positif")
data_negatif = data_grouping(data_train, "Negatif")

data_mean = df_mean(data_positif, data_negatif)
data_std = df_std(data_positif, data_negatif)
data_prob = df_prob(data_train, data_positif, data_negatif)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/training')
def training():
    title = "Data Training ( Data Latih )"
    return render_template(
        "training.html", title=title,
        tables=[data_train.to_html(classes="data", header="true")]
    )

@app.route('/grouping')
def grouping():
    title = "Data Grouping ( Pengelompokan Data )"
    return render_template(
        "grouping.html", title=title,
        tables1=[data_positif.to_html(classes="data", header="true")], 
        tables2=[data_negatif.to_html(classes="data", header="true")], 
        total_positif=len(data_positif), total_negatif=len(data_negatif)
    )

@app.route('/mean')
def mean():
    title = "Mean ( Nilai Rata-rata )"
    return render_template(
        "dataframe.html", title=title,
        tables=[data_mean.to_html(classes="data", header="true")]
    )

@app.route('/std')
def std():
    title = "Standar Deviasi ( Simpangan Baku )"
    return render_template(
        "dataframe.html", title=title,
        tables=[data_std.to_html(classes="data", header="true")]
    )

@app.route('/prob')
def prob():
    title = "Probabilitas ( Peluang )"
    return render_template(
        "dataframe.html", title=title,
        tables=[data_prob.to_html(classes="data", header="true")]
    )

@app.route('/testing')
def testing():
    title = "Data Testing ( Data Uji )"
    return render_template("testing.html", title=title)

@app.route('/predict', methods=["POST"])
def predict():
    title = "Predict ( Prediksi )"

    df_testing = pd.DataFrame({
        "Provinsi" : request.form.get("nama_provinsi"),
        "Dalam Perawatan" : int(request.form.get("dalam_perawatan")),
        "Sembuh" : int(request.form.get("sembuh")),
        "Meninggal" : int(request.form.get("meninggal"))
    }, index = [0])

    classification(df_testing, data_mean, data_std)

    return render_template(
        "dataframe.html", title=title,
        tables=[df_testing.to_html(classes="data", header="true")]
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)