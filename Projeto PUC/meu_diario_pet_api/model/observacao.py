from .db import conectar

class Observacao:
    @staticmethod
    def adicionar(pet_id, data, texto):
        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO observacoes (pet_id, data, texto) VALUES (?, ?, ?)",
            (pet_id, data, texto[:500])  # Limita a 500 caracteres
        )
        conn.commit()
        conn.close()
        return {"mensagem": "Observação adicionada"}

    @staticmethod
    def listar(pet_id):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM observacoes WHERE pet_id=? ORDER BY data DESC", (pet_id,))
        observacoes = cur.fetchall()
        conn.close()

        lista = []
        for o in observacoes:
            lista.append({
                "id": o[0],
                "data": o[2],
                "texto": o[3]
            })
        return lista

    @staticmethod
    def deletar(id):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM observacoes WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Observação removida"}
