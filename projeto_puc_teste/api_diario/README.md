# API Diário de Pet

Esta é a API principal para o sistema de diário de pets, desenvolvida com Flask e SQLAlchemy.

## Funcionalidades

- CRUD de pets
- Gerenciamento de diário médico
- Observações dos pets

## Instalação

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute a aplicação:
   ```bash
   python app.py
   ```

## Docker

Para executar com Docker:
```bash
docker build -t api-diario .
docker run -p 5000:5000 api-diario
```

## Documentação

Acesse `/apidocs` para a documentação Swagger.