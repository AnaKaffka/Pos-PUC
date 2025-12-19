from .db import conectar

class Pet:
    @staticmethod
    def cadastrar(dados):
        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pets (nome, idade, tipo, foto) VALUES (?, ?, ?, ?)",
            (dados["nome"], dados["idade"], dados["tipo"], dados.get("foto"))
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
            pet_dict = {"id": p[0], "nome": p[1], "idade": p[2], "tipo": p[3], "foto": p[4]}
            
            # Get diary entry (only one per pet now)
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT comida_preferida, veterinario, data_vacinacao, peso FROM diario WHERE pet_id=? LIMIT 1", (p[0],))
            diario = cur.fetchone()
            conn.close()
            
            if diario:
                pet_dict["comida_preferida"] = diario[0]
                pet_dict["veterinario"] = diario[1]
                pet_dict["data_vacinacao"] = diario[2]
                pet_dict["peso"] = diario[3]
            else:
                pet_dict["comida_preferida"] = None
                pet_dict["veterinario"] = None
                pet_dict["data_vacinacao"] = None
                pet_dict["peso"] = None
            
            lista.append(pet_dict)

        return lista

    @staticmethod
    def buscar(id):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pets WHERE id=?", (id,))
        p = cur.fetchone()
        conn.close()

        if p:
            return {"id": p[0], "nome": p[1], "idade": p[2], "tipo": p[3], "foto": p[4]}
        return None

    @staticmethod
    def atualizar_foto(id, foto):
        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "UPDATE pets SET foto=? WHERE id=?",
            (foto, id)
        )
        conn.commit()
        conn.close()
        return {"mensagem": "Foto atualizada"}

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