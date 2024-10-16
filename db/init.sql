# db/init.sql
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS challenges (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    points INTEGER DEFAULT 10
);

CREATE TABLE IF NOT EXISTS player_progress (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    challenge_id INTEGER REFERENCES challenges(id),
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attempts INTEGER DEFAULT 1,
    UNIQUE(player_id, challenge_id)
);

-- Insertar desafíos iniciales
INSERT INTO challenges (name, description, points) VALUES
('Servicio Básico', 'Conectar con el primer servicio de la red', 10),
('Servicio Avanzado', 'Establecer conexión con el segundo servicio', 20);
