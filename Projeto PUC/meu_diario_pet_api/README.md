# 🐾 Meu Diário Pet - API Backend

## 📌 Descrição do Projeto

Este projeto corresponde ao **backend da aplicação Meu Diário Pet**, desenvolvido como um MVP (Minimum Viable Product) para a disciplina de Desenvolvimento Full Stack Básico da PUC.

A API foi construída em **Python utilizando o framework Flask**, sendo responsável por gerenciar o cadastro de pets e os registros de observações do diário de cada pet.

O sistema segue os princípios REST estudados em aula, como separação entre cliente e servidor, uniformidade de interfaces, desenvolvimento em camadas e ausência de estado (stateless).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Flask** - Framework web minimalista
- **Flask-CORS** - Gerenciamento de CORS
- **Flask-Swagger-UI** - Documentação interativa da API
- **Pydantic** - Validação de dados
- **SQLite** - Banco de dados relacional

---

## 📂 Estrutura do Projeto

```
meu_diario_pet_api/
├── app.py                      # Aplicação principal Flask
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
├── database.db                 # Banco de dados SQLite (gerado automaticamente)
├── model/
│   ├── db.py                  # Configuração do banco de dados
│   ├── pet.py                 # Modelo e operações de Pet
│   ├── diario.py              # Modelo e operações de Diário
│   └── observacao.py          # Modelo e operações de Observação
├── schemas/
│   ├── pet_schema.py          # Schemas de validação para Pet
│   ├── diario_schema.py       # Schemas de validação para Diário
│   └── observacao_schema.py   # Schemas de validação para Observação
└── static/
    ├── swagger.json           # Especificação OpenAPI
    ├── index.html             # Página inicial da API
    ├── script.js              # Scripts da página inicial
    └── style.css              # Estilos da página inicial
```

---

## ▶️ Como Executar o Projeto

### 1️⃣ Pré-requisitos

- Python 3.7 ou superior instalado
- pip (gerenciador de pacotes Python)

### 2️⃣ Instalar as dependências

```bash
cd meu_diario_pet_api
pip install -r requirements.txt
```

### 3️⃣ Executar a aplicação

```bash
python app.py
```

A API será executada em:
```
http://127.0.0.1:5000
```

---

## 📑 Documentação da API (Swagger)

A documentação interativa da API está disponível através do Swagger em:

```
http://127.0.0.1:5000/swagger
```

No Swagger você pode:

- Visualizar todas as rotas disponíveis
- Testar as requisições diretamente no navegador
- Ver a estrutura das requisições e respostas
- Consultar os códigos de status HTTP

---

## 🔗 Endpoints da API

### **Pets**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/pets` | Cadastrar um novo pet |
| GET | `/pets` | Listar todos os pets cadastrados |
| GET | `/pets/<id>` | Buscar um pet pelo ID |
| PUT | `/pets/<id>` | Atualizar foto de um pet |
| DELETE | `/pets/<id>` | Remover um pet |

### **Diário**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/pets/<id>/diario` | Adicionar um registro ao diário do pet |
| GET | `/pets/<id>/diario` | Buscar o diário de um pet |
| PUT | `/pets/<id>/diario` | Atualizar o diário de um pet |

### **Observações**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/pets/<id>/observacoes` | Adicionar uma observação ao diário do pet |
| GET | `/pets/<id>/observacoes` | Listar todas as observações de um pet |
| DELETE | `/observacoes/<id>` | Deletar uma observação específica |

### **Outros**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Página inicial da API |
| GET | `/api` | Informações da API |
| GET | `/swagger` | Documentação Swagger |

---

## 📝 Exemplos de Uso

### Cadastrar um Pet

```json
POST /pets
Content-Type: application/json

{
  "nome": "Rex",
  "idade": 3,
  "tipo": "Cachorro",
  "foto": "data:image/jpeg;base64,..."
}
```

### Adicionar uma Observação

```json
POST /pets/1/observacoes
Content-Type: application/json

{
  "data": "2025-12-19",
  "texto": "Rex comeu bem hoje e brincou bastante no parque."
}
```

---

## 💾 Banco de Dados

O banco de dados SQLite é criado automaticamente na primeira execução da aplicação. As seguintes tabelas são criadas:

- **pets** - Armazena informações dos pets
- **diario** - Armazena dados gerais do diário de cada pet
- **observacoes** - Armazena observações diárias dos pets

---

## 🎯 Princípios Aplicados

- **Arquitetura em Camadas**: Separação entre models, schemas e rotas
- **REST**: Uso adequado de métodos HTTP e URIs
- **Stateless**: Cada requisição contém todas as informações necessárias
- **Validação**: Uso de Pydantic para validar dados de entrada
- **CORS**: Configurado para permitir integração com frontend
- **Documentação**: API documentada com Swagger/OpenAPI

---

## 🤝 Contribuindo

Este projeto faz parte de um trabalho acadêmico da PUC. Para sugestões ou melhorias, entre em contato com o desenvolvedor.

---

## 📄 Licença

Projeto desenvolvido para fins educacionais.