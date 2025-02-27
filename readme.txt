install python3

python -m venv venv // create vertual env

source venv/Scripts/activate // enable the vertual env
(venv) 

librayes to install

pip install fastapi //fast api
pip install tortoise-orm // orm for sql
pip install uvicorn // like nodemon to we do not have to restart server everytime we change something 
pip install pymongo

before running this cmd check your vertual enc is activated with this sign (venv) 

uvicorn app:server --reload // in your terminal

def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=5000, reload=True)

// uvicorn main:server --host 0.0.0.0 --port 5000 --reload

 
