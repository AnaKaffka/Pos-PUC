# API Veterinários

Esta é a API secundária para o sistema de veterinários e agendamentos, integrada com ViaCEP para validação de endereços.

## Funcionalidades

- CRUD de veterinários
- Gerenciamento de agendamentos
- Validação de endereços via ViaCEP

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
docker build -t api-vet .
docker run -p 5001:5001 api-vet
```

## Documentação

Acesse `/apidocs` para a documentação Swagger.