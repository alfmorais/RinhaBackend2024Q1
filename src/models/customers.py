commands = (
    """
    DROP TABLE IF EXISTS Clientes CASCADE;
    """,
    """
    CREATE TABLE Clientes (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(64),
        limite INTEGER,
        saldo INTEGER DEFAULT 0
    );
    """,
    """
    INSERT INTO Clientes (nome, limite, saldo) VALUES
        ('o barato sai caro', 100000, 0),
        ('zan corp ltda', 80000, 0),
        ('les cruders', 1000000, 0),
        ('padaria joia de cocaia', 10000000, 0),
        ('kid mais', 500000, 0);
    """,
)
