from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Aplicación DevOps en AWS</h1>
    <p>Despliegue automatizado con Docker, GitHub Actions y AWS.</p>
    <p>Proyecto final - Soluciones Tecnológicas del Futuro.</p>
    """

@app.route("/health")
def health():
    return {"status": "ok", "service": "docker-flask-devops"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
