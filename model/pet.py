from .db import conectar

class Pet:
    @staticmethod
    def cadastrar(dados):
        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pets (nome, idade, tipo) VALUES (?, ?, ?)",
            (dados["nome"], dados["idade"], dados["tipo"])
        )
        conn.commit()
        conn.close()
        return {"mensagem": "Pet cadastrado"}

    @staticmethod
    def listar():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pets")
        pets = cur.fetchall()
        conn.close()

        lista = []
        for p in pets:
            lista.append({"id": p[0], "nome": p[1], "idade": p[2], "tipo": p[3]})

        return lista

    @staticmethod
    def buscar(id):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pets WHERE id=?", (id,))
        p = cur.fetchone()
        conn.close()

        if p:
            return {"id": p[0], "nome": p[1], "idade": p[2], "tipo": p[3]}
        return None

    @staticmethod
    def deletar(id):
        print(f"Deletando pet {id}")
        conn = conectar()
        cur = conn.cursor()
        print("Deletando diario")
        cur.execute("DELETE FROM diario WHERE pet_id=?", (id,))
        print("Deletando pet")
        cur.execute("DELETE FROM pets WHERE id=?", (id,))
        print("Commit")
        conn.commit()
        conn.close()
        print("Feito")
        return {"mensagem": "Pet removido"}