from fastapi import FastAPI


app = FastAPI(
    title="IAM Application"
)


@app.get("/")
def root():
    return {
        "message": "IAM Application Running"
    }