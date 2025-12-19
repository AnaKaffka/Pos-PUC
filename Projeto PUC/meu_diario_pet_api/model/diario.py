from .db import conectar

class Diario:
    @staticmethod
    def buscar_ou_criar(pet_id):
        """Retorna o diário do pet ou None se não existir"""
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM diario WHERE pet_id=? LIMIT 1", (pet_id,))
        r = cur.fetchone()
        conn.close()
        
        if r:
            return {
                "id": r[0],
                "comida_preferida": r[2],
                "veterinario": r[3],
                "data_vacinacao": r[4],
                "peso": r[5],
                "observacoes": r[6]
            }
        return None

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
    def atualizar(pet_id, dados):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            UPDATE diario
            SET comida_preferida=?, veterinario=?, data_vacinacao=?, peso=?, observacoes=?
            WHERE pet_id=?
        """, (
            dados["comida_preferida"],
            dados["veterinario"],
            dados["data_vacinacao"],
            dados["peso"],
            dados["observacoes"],
            pet_id
        ))
        conn.commit()
        conn.close()
        return {"mensagem": "Registro atualizado"}

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