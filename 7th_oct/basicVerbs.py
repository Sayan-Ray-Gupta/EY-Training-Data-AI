from fastapi import FastAPI

#create FastAPI instance
app = FastAPI()


# --------GET----------
@app.get("/students")
def get_students():
    return {"This is the GET request"}

#--------POST----------

@app.post("/students")
def create_students():
    return {"This is the POST request"}


#---------PUT-----------

@app.put("/students")
def update_student():
    return {"This is the PUT request"}

#---------DELETE--------

@app.delete("/students")
def delete_student():
    return {"This is the DELETE request"}