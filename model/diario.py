from .db import conectar

class Diario:
    @staticmethod
    def adicionar(pet_id, dados):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO diario
            (pet_id, comida_preferida, veterinario, data_vacinacao, peso, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            pet_id,
            dados["comida_preferida"],
            dados["veterinario"],
            dados["data_vacinacao"],
            dados["peso"],
            dados["observacoes"]
        ))
        conn.commit()
        conn.close()
        return {"mensagem": "Registro adicionado"}

    @staticmethod
    def listar(pet_id):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM diario WHERE pet_id=?", (pet_id,))
        registros = cur.fetchall()
        conn.close()

        lista = []
        for r in registros:
            lista.append({
                "id": r[0],
                "comida_preferida": r[2],
                "veterinario": r[3],
                "data_vacinacao": r[4],
                "peso": r[5],
                "observacoes": r[6]
            })
        return lista