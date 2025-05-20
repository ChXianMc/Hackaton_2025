from app import app  # noqa: F401

# Importar las rutas
import routes  # noqa: F401
import routes_appointment  # noqa: F401
import routes_medication  # noqa: F401
import routes_message  # noqa: F401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
