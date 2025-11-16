from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="JobDesk API", description="API for the JobDesk project")

@app.get("/")
def root():
    html_content = "<h2>Hello METANIT.COM!</h2>"
    return HTMLResponse(content=html_content)

@app.get("/users/{username}")
def get_user(username: str):
    print(f"Received username: {username}")
    return {"username": username}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)