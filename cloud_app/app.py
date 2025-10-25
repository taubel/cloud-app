from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def root():
    content = """
    <html>
        <head>
            <title>Cloud app</title>
        </head>
        <body>
            <h1>Hi!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=content, status_code=200)
