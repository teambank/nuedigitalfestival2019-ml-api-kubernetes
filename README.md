Nürnberg Digital Festival: Deployen von Machine-Learning Modellen als Microservice in Kubernetes
==============================

[Vortrag im Rahmen des Nürnberg Digital Festivals beim DevBBQ@TeamBank](ML_API_on_Kubernetes.md).

1. [Installation](#installation)
2. [Usage](#usage)


# <a name="installation"></a>Installation

## Umgebung einrichten und Pakete installieren

1. `conda` Umgebung erzeugen, aktivieren und weitere Pakete nachladen:
```
conda env create -f environment.yml
activate nuedigitalmlapi
```
DVC (data version control) muss manuell über pip installiert werden:
```
pip install dvc[s3]
dvc init
```

`nuedigitalmlapi` Package installieren
```
pip install -e .
```

## S3 Modell Repository einrichten

Credentials Datei `credentials` im Projekt-Root ablegen:
```ini
[default]
aws_access_key_id = <AWS_ACCESS_KEYID>
aws_secret_access_key = <AWS_SECRET_ACCESS_KEY>
```

S3 Bucket in AWS anlegen: https://docs.aws.amazon.com/quickstarts/latest/s3backup/step-1-create-bucket.html

DVC für S3 Endpunkt konfigurieren:
```
dvc remote add -d modelrepo s3://<bucket_name>/<folder_name>
dvc remote modify modelrepo profile credentials
```

Alternativ: [Minio](https://docs.min.io/) Instanz (z.B. lokal) starten.

DVC für S3 Minio Endpunkt konfigurieren
```
dvc remote add -d modelrepo s3://<bucket_name>/<folder_name>
dvc remote modify modelrepo endpointurl https://<minio_endpoint>:<port>
dvc remote modify modelrepo credentialpath credentials
```

# <a name="usage"></a>Usage

## Training des Modells
Pipeline ausführen, um Datensatz zu laden und Modell zu trainieren:
```
dvc repro model.pkl.dvc
```

Daten in DVC Remote Repository speichern:
```
dvc push
```

## API

API testen.
```
SET FLASK_ENV=development
flask run
```

# Tests

Unittests ausführen
```
pytest
```

## Deployment

OpenShift Instanz z.B. unter https://manage.openshift.com/ oder via [Minishift](https://docs.okd.io/latest/minishift/getting-started/installing.html) bereitstellen und Projekt auswählen.

Login Kommando aus Web-Console kopieren und ausführen. Projekt/Namespace für Deployment setzen.

Folgende BasicAuth-Secrets in OpenShift anlegen.

| Secret-Name | Username | Passwort | Verwendung |
|---|---|---|---|
| github | <GITHUB_USERNAME> | <[GITHUB_ACCESS_TOKEN](https://github.com/settings/tokens)> | Zugriff auf Code |

### Deployment durchführen
```
# ImageStream und BildConfig erzeugen
oc apply -f deployment\imageStream.yml
oc apply -f deployment\buildConfig.yml

# Secret mit S3 credentials erzeugen
oc create secret generic aws-credentials --from-file=credentials
oc label secret aws-credentials app=nuedigitalmlapi
oc get secret/aws-credentials --export -o yaml

# DVC Config als Secret
oc create secret generic dvc-config --from-file .dvc\config
oc label secret dvc-config app=nuedigitalmlapi

# Build starten
oc start-build nuedigitalmlapi-build --from-repo .

# ConfigMap aus Datei erzeugen
oc create configmap neudigitalkiapi-gunicorn --from-file config.py
oc label configmap neudigitalkiapi-gunicorn app=nuedigitalmlapi
oc get cm/neudigitalkiapi-gunicorn --export -o yaml

# Pods deployen 
oc apply -f deployment\deployment.yml

# Service und Route erzeugen 
oc apply -f deployment\service.yml
oc apply -f deployment\route.yml

# Tag setzen für Deployment in Produktion
oc tag neudigitalkiapi:v1.0.0 neudigitalkiapi:latest
```

### Deployment löschen
```
oc delete all,secret,configmap --selector app=nuedigitalmlapi
```


