# Setup Dashboard 

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9.19
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir Air_Quality
cd Air_Quality
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```