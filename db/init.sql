CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK (role IN ('user', 'admin'))
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES users(id),
    description TEXT NOT NULL,
    total_cents INTEGER NOT NULL CHECK (total_cents > 0)
);

INSERT INTO users (email, role) VALUES
    ('alice@example.test', 'user'),
    ('bob@example.test', 'user'),
    ('admin@example.test', 'admin');

INSERT INTO orders (customer_id, description, total_cents) VALUES
    (1, 'Synthetic laptop order', 129900),
    (2, 'Synthetic monitor order', 34900);
