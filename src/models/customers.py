commands = (
    """
    DROP TABLE IF EXISTS Clientes CASCADE;
    """,
    """
    CREATE TABLE Clientes (
        id SERIAL PRIMARY KEY,
        limite INTEGER,
        saldo_inicial INTEGER DEFAULT 0
    );
    """,
    """
    INSERT INTO Clientes (limite, saldo_inicial) VALUES
        (100000, 0),
        (80000, 0),
        (1000000, 0),
        (10000000, 0),
        (500000, 0);
    """,
)
