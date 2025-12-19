# 🐾 Diário de Pets – Back-end

## 📌 Descrição do Projeto
Este projeto corresponde ao **back-end da aplicação Diário de Pets**, desenvolvido como um
MVP (Minimum Viable Product) para a disciplina de Desenvolvimento Full Stack Básico.

A API foi construída em **Python utilizando o framework Flask**, sendo responsável por
gerenciar o cadastro de pets e os registros do diário de cada pet, como alimentação,
veterinário, datas de vacinação, peso e observações.

O sistema segue os princípios estudados em aula, como separação entre cliente e servidor,
uniformidade de interfaces, desenvolvimento em camadas e ausência de estado (stateless).

---

## 🛠️ Tecnologias Utilizadas
- Python 3
- Flask
- Flask-CORS
- SQLite
- Swagger (OpenAPI)

---

## 📂 Estrutura do Projeto
diario-pets-backend/
┣ app.py
┣ database.db
┣ requirements.txt
┗ README.md

yaml
Copiar código

---

## ▶️ Como Executar o Projeto

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/seu-usuario/diario-pets-backend
cd diario-pets-backend
2️⃣ Instalar as dependências
bash
Copiar código
pip install -r requirements.txt
3️⃣ Executar a aplicação
bash
Copiar código
python app.py
A API será executada em:

arduino
Copiar código
http://localhost:5000
📑 Documentação da API (Swagger)
A documentação interativa da API está disponível através do Swagger em:

bash
Copiar código
http://localhost:5000/swagger
No Swagger é possível visualizar:

Todas as rotas disponíveis

Métodos HTTP utilizados

Estrutura das requisições e respostas

Códigos de status esperados

🔗 Rotas da API
Pets
POST /pets – Cadastrar um novo pet

GET /pets – Listar todos os pets cadastrados

GET /pets/<id> – Buscar um pet pelo ID

DELETE /pets/<id> – Remover um pet

Diário do Pet
POST /pets/<id>/diario – Adicionar um registro ao diário do pet

GET /pets/<id>/diario – Listar os registros do diário do pet

💡 Observações
O banco de dados SQLite é criado automaticamente na primeira execução da aplicação.

A API não mantém estado entre requisições (stateless).

O projeto foi desenvolvido com foco em simplicidade, organização e clareza do código.