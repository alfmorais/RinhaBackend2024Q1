commands = (
    """
    DROP TABLE IF EXISTS Transacoes CASCADE;
    """,
    """
    CREATE TABLE Transacoes (
        id SERIAL PRIMARY KEY,
        valor INTEGER,
        tipo CHAR(1),
        descricao VARCHAR(10),
        cliente_id INTEGER,
        realizada_em TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (cliente_id) REFERENCES Clientes(id)
    );
    """,
)
