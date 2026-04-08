# Projeto PUC Avançado - Sistema de Cuidado de Pets

Este é um sistema modular de microserviços para gerenciamento de pets, desenvolvido como projeto avançado da PUC.

## Arquitetura

O sistema é composto por três módulos:

1. **API Diário de Pets** (porta 5000): Gerencia pets, diários médicos e observações.
2. **API Veterinários** (porta 5001): Gerencia veterinários, agendamentos e integração com ViaCEP.
3. **Front-end**: Interface web que consome ambas as APIs.

## Tecnologias

- **Back-end**: Python, Flask, SQLAlchemy, Pydantic, Flasgger
- **Front-end**: HTML, CSS, JavaScript
- **Banco de dados**: SQLite
- **Containerização**: Docker
- **Integração Externa**: ViaCEP API

## Como executar

### Com Docker

1. Para cada módulo, navegue até a pasta e execute:
   ```bash
   docker build -t <nome> .
   docker run -p <porta>:<porta> <nome>
   ```

### Localmente

1. Instale as dependências em cada API:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute as APIs:
   ```bash
   # API Diário
   python api_diario/app.py

   # API Vet
   python api_vet/app.py
   ```

3. Abra o front-end em um navegador: `frontend/index.html`

## Documentação

Cada API possui documentação Swagger em `/apidocs`.

## Repositórios

Este projeto deve ser dividido em repositórios GitHub separados para cada módulo desenvolvido.