# 🐾 Meu Diário Pet - Frontend

Interface web para o sistema de gerenciamento de pets e seus diários de observações.

## 📋 Descrição

Este é o frontend da aplicação **Meu Diário Pet**, desenvolvido com HTML, CSS e JavaScript puro. A aplicação permite cadastrar pets, visualizar informações detalhadas e manter um diário de observações diárias para cada animal.

## 🚀 Funcionalidades

- **Cadastro de Pets**: Registre novos pets com nome, idade, tipo e foto
- **Listagem de Pets**: Visualize todos os pets cadastrados
- **Diário de Observações**: Adicione observações diárias para cada pet
- **Visualização de Observações**: Consulte o histórico de observações de cada pet
- **Interface Responsiva**: Design adaptável para diferentes dispositivos

## 🛠️ Tecnologias Utilizadas

- HTML5
- CSS3
- JavaScript (ES6+)
- Fetch API para comunicação com o backend

## 📁 Estrutura de Arquivos

```
meu_diario_pet_front/
├── index.html      # Página principal da aplicação
├── style.css       # Estilos da aplicação
├── script.js       # Lógica e interações
└── README.md       # Este arquivo
```

## ⚙️ Como Usar

### Pré-requisitos

- Um navegador web moderno (Chrome, Firefox, Edge, Safari)
- O backend da aplicação rodando (meu_diario_pet_api)

### Configuração

1. **Inicie o backend**:
   ```bash
   cd ../meu_diario_pet_api
   python app.py
   ```

2. **Abra o frontend**:
   - Abra o arquivo `index.html` diretamente no navegador, ou
   - Use um servidor local como Live Server (extensão do VS Code)

### Usando a Aplicação

1. **Cadastrar um Pet**:
   - Preencha nome, idade e tipo do pet
   - (Opcional) Adicione uma foto
   - Clique em "Cadastrar"

2. **Visualizar Pets**:
   - Os pets cadastrados aparecem automaticamente na seção "Meus Pets"
   - Cada card mostra as informações do pet

3. **Adicionar Observação ao Diário**:
   - Selecione um pet
   - Escreva a observação do dia
   - Clique em "Adicionar ao Diário"

4. **Consultar Diário**:
   - As observações aparecem na seção "Diário do Pet"
   - Mostra data e conteúdo de cada observação

## 🔗 Integração com Backend

O frontend se comunica com a API REST do backend através das seguintes endpoints:

- `GET /pets` - Lista todos os pets
- `POST /pet` - Cadastra um novo pet
- `GET /diario/:pet_id` - Obtém observações de um pet
- `POST /observacao` - Adiciona nova observação

**URL Base da API**: `http://127.0.0.1:5000`

## 🎨 Personalização

Para personalizar a aparência da aplicação, edite o arquivo `style.css`. As principais classes incluem:

- `.pet-card` - Cards dos pets
- `.observacao-item` - Itens de observação
- `button` - Botões da interface

## 📝 Notas

- Certifique-se de que o backend está rodando antes de usar o frontend
- As imagens dos pets são armazenadas em base64
- A aplicação usa requisições assíncronas (async/await)

## 🤝 Contribuindo

Este projeto faz parte de um trabalho acadêmico da PUC. Para sugestões ou melhorias, entre em contato com o desenvolvedor.

## 📄 Licença

Projeto desenvolvido para fins educacionais.