# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.3
#   kernelspec:
#     display_name: Python [conda env:nuedigex]
#     language: python
#     name: conda-env-nuedigex-py
# ---

# # Trainingsdaten aufbereiten
#
# In diesem Notebook werden die Roh-Daten für das Training aufbereitet.
#
# DVC Pipeline wurde mit folgendem Befehl eingerichtet:
# ```
# dvc run --no-exec -o ..\data\interim\model_dev_data.pkl -d Trainingsdaten_aufbereiten.py -w notebooks python Trainingsdaten_aufbereiten.py
# ```
#

import pandas as pd
import numpy as np
import sklearn.datasets

# ## Daten einlesen
#
# Nachdem die Daten mit im Ordner `data/raw` abgelegt wurden, sollten diese mit 
# ```
# dvc add data/raw
# ```
# dem Data Version Control Projekt hinzugefügt werden.
#
# Anschließend können diese Daten hier Pfad muss angepasst werden.
#

data = sklearn.datasets.load_iris()
train_df = pd.DataFrame(data.data, columns=data.feature_names)
train_df["label"] = data.target
train_df["label"] = train_df["label"].map(lambda x: data.target_names[x])
train_df.head()

# ## Daten aufbereiten
#
# An dieser Stelle wird werden die Aufbereitungsschritte an `train_df` durchgeführt.
#

# ## Aubereitete Daten ausgeben
#
# Der DataFrame wird dann als Pickle ausgeben.
#

train_df.to_pickle("../data/interim/model_dev_data.pkl")

train_df["label"].unique()
