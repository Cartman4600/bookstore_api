# bookstore_api

Ein API- und Datenbankprojekt für einen Buchladen mit Café.

## Projektbeschreibung

Dieses Projekt stellt eine RESTful API für einen Buchladen mit integriertem Café bereit. Es dient als Test- und Lernprojekt zur Entwicklung von APIs und Datenbankanwendungen.

## Technologien

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**

## Projektstruktur

- `main.py`: Einstiegspunkt der Anwendung
- `auth.py`: Authentifizierungslogik
- `database.py`: Datenbankverbindung und -initialisierung
- `models/`: Datenbankmodelle
- `schemas/`: Pydantic-Schemas für Datenvalidierung
- `routers/`: API-Routen
- `data/`: Beispieldaten
- `sql/`: SQL-Skripte zur Datenbankinitialisierung

## Installation und Ausführung

1. Repository klonen:
   ```bash
   git clone https://github.com/Cartman4600/bookstore_api.git
   cd bookstore_api
   ```

2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Auf Windows: venv\Scripts\activate
   ```

3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. Datenbank einrichten:
   - PostgreSQL installieren und einen neuen Benutzer sowie eine neue Datenbank erstellen.
   - SQL-Skripte im `sql/`-Verzeichnis ausführen, um die Datenbanktabellen zu erstellen.
   - Beispieldaten einplfegen.

5. Anwendung starten:
   ```bash
   uvicorn main:app --reload
   ```

6. API-Dokumentation aufrufen:
   - Swagger UI: [http://localhost:5000/docs](http://localhost:5000/docs)
   - ReDoc: [http://localhost:5000/redoc](http://localhost:5000/redoc)

