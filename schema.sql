CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE sessions (
    session_key VARCHAR(255) PRIMARY KEY,
    user_id INT REFERENCES users(id),
    ip_address VARCHAR(45) NOT NULL,
    expires_at TIMESTAMP NOT NULL
);

CREATE TABLE airports (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL
);

CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    origin_id INT REFERENCES airports(id),
    destination_id INT REFERENCES airports(id),
    departure_time TIMESTAMP NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    available_seats INT NOT NULL
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    flight_id INT REFERENCES flights(id),
    passengers INT NOT NULL,
    booking_ref VARCHAR(6) UNIQUE NOT NULL, -- Localizador (ex: ABC123)
    ticket_numbers JSONB, -- Array de números de tickets (ex: ["TKT001", "TKT002"])
    created_at TIMESTAMP DEFAULT NOW()
);