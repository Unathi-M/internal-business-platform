CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'admin'))
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES users(id),
    description TEXT NOT NULL,
    total_cents INTEGER NOT NULL CHECK (total_cents > 0)
);

INSERT INTO users (email, password_hash, role) VALUES
    (
        'alice@example.test',
        'scrypt$16384$8$1$bf349fb6d238eda2f1322c37151a20fb$29516b928aead1582ac36025e663d7d2132a382a4d5846365e0e7ddad4ecdcb7',
        'user'
    ),
    (
        'bob@example.test',
        'scrypt$16384$8$1$cd65e5ab24fc0cda7ff3f724c46c5d4e$8e6d7793d7bb814bccc092c0964215dfa0a14eb3dc524ca8d0bdc1b3382306af',
        'user'
    ),
    (
        'admin@example.test',
        'scrypt$16384$8$1$4d1dac08aee35cf3115898bbd40fa09a$fb8187f7f7e898b2b80ec0bc3794364a5973fb5063094ad8f5d00aa3d38d45b3',
        'admin'
    );

INSERT INTO orders (customer_id, description, total_cents) VALUES
    (1, 'Synthetic laptop order', 129900),
    (2, 'Synthetic monitor order', 34900);
