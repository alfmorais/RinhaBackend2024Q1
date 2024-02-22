commands = (
    """
    DROP TABLE IF EXISTS Clientes CASCADE;
    """,
    """
    CREATE TABLE Clientes (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(64),
        limite INTEGER,
        saldo_inicial INTEGER DEFAULT 0
    );
    """,
    """
    INSERT INTO Clientes (nome, limite, saldo_inicial) VALUES
        ('o barato sai caro', 1000 * 100, 0),
        ('zan corp ltda', 800 * 100, 0),
        ('les cruders', 10000 * 100, 0),
        ('padaria joia de cocaia', 100000 * 100, 0),
        ('kid mais', 5000 * 100, 0);
    """,
)
