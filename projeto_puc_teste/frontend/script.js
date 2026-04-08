const API_DIARIO = "http://127.0.0.1:5000";
const API_VET = "http://127.0.0.1:5001";

const nome = document.getElementById('nome');
const idade = document.getElementById('idade');
const tipo = document.getElementById('tipo');
const foto = document.getElementById('foto');
const petsDiv = document.getElementById('pets');
const diarioDiv = document.getElementById('diario');
const observacoesDiv = document.getElementById('observacoes');
const vetNome = document.getElementById('vetNome');
const vetEspecialidade = document.getElementById('vetEspecialidade');
const vetEndereco = document.getElementById('vetEndereco');
const vetTelefone = document.getElementById('vetTelefone');
const vetsDiv = document.getElementById('vets');
const petSelect = document.getElementById('petSelect');
const vetSelect = document.getElementById('vetSelect');
const appointmentData = document.getElementById('appointmentData');
const appointmentMotivo = document.getElementById('appointmentMotivo');
const appointmentsDiv = document.getElementById('appointments');
const cep = document.getElementById('cep');
const enderecoDiv = document.getElementById('endereco');

let selectedPetId = null;

function cadastrarPet() {
  const file = foto.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const fotoBase64 = e.target.result;
      enviarPet(fotoBase64);
    };
    reader.readAsDataURL(file);
  } else {
    enviarPet(null);
  }
}

function enviarPet(fotoBase64) {
  fetch(`${API_DIARIO}/pets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome: nome.value,
      idade: parseInt(idade.value),
      tipo: tipo.value,
      foto: fotoBase64
    })
  })
  .then(response => response.json())
  .then(() => {
    listarPets();
    nome.value = '';
    idade.value = '';
    tipo.value = '';
    foto.value = '';
  })
  .catch(error => console.error('Erro:', error));
}

function listarPets() {
  fetch(`${API_DIARIO}/pets`)
  .then(response => response.json())
  .then(pets => {
    petsDiv.innerHTML = '';
    petSelect.innerHTML = '<option value="">Selecione um pet</option>';
    pets.forEach(pet => {
      const div = document.createElement('div');
      div.className = 'pet';
      div.innerHTML = `
        <h3>${pet.nome} (${pet.tipo})</h3>
        <p>Idade: ${pet.idade}</p>
        ${pet.foto ? `<img src="${pet.foto}" alt="Foto de ${pet.nome}" style="max-width: 100px;">` : ''}
        <button onclick="selecionarPet(${pet.id})">Ver Diário</button>
        <button onclick="deletarPet(${pet.id})">Deletar</button>
      `;
      petsDiv.appendChild(div);
      const option = document.createElement('option');
      option.value = pet.id;
      option.textContent = pet.nome;
      petSelect.appendChild(option);
    });
  })
  .catch(error => console.error('Erro:', error));
}

function selecionarPet(id) {
  selectedPetId = id;
  buscarDiario(id);
  listarObservacoes(id);
}

function buscarDiario(petId) {
  fetch(`${API_DIARIO}/diario/${petId}`)
  .then(response => response.json())
  .then(diario => {
    if (diario.erro) {
      diarioDiv.innerHTML = '<p>Diário não encontrado. <button onclick="criarDiario()">Criar Diário</button></p>';
    } else {
      diarioDiv.innerHTML = `
        <p>Comida Preferida: ${diario.comida_preferida || 'N/A'}</p>
        <p>Veterinário: ${diario.veterinario || 'N/A'}</p>
        <p>Data Vacinação: ${diario.data_vacinacao || 'N/A'}</p>
        <p>Peso: ${diario.peso || 'N/A'}</p>
        <p>Observações: ${diario.observacoes || 'N/A'}</p>
        <button onclick="editarDiario()">Editar Diário</button>
      `;
    }
  })
  .catch(error => console.error('Erro:', error));
}

function criarDiario() {
  const dados = {
    comida_preferida: prompt('Comida Preferida:'),
    veterinario: prompt('Veterinário:'),
    data_vacinacao: prompt('Data Vacinação:'),
    peso: parseFloat(prompt('Peso:')),
    observacoes: prompt('Observações:')
  };
  fetch(`${API_DIARIO}/diario/${selectedPetId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados)
  })
  .then(() => buscarDiario(selectedPetId))
  .catch(error => console.error('Erro:', error));
}

function editarDiario() {
  // Similar to criar, but PUT
}

function listarObservacoes(petId) {
  fetch(`${API_DIARIO}/observacoes/${petId}`)
  .then(response => response.json())
  .then(observacoes => {
    observacoesDiv.innerHTML = '<button onclick="adicionarObservacao()">Adicionar Observação</button>';
    observacoes.forEach(obs => {
      const div = document.createElement('div');
      div.innerHTML = `<p>${obs.data}: ${obs.texto}</p>`;
      observacoesDiv.appendChild(div);
    });
  })
  .catch(error => console.error('Erro:', error));
}

function adicionarObservacao() {
  const data = prompt('Data:');
  const texto = prompt('Texto:');
  fetch(`${API_DIARIO}/observacoes/${selectedPetId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ data, texto })
  })
  .then(() => listarObservacoes(selectedPetId))
  .catch(error => console.error('Erro:', error));
}

function deletarPet(id) {
  fetch(`${API_DIARIO}/pets/${id}`, { method: "DELETE" })
  .then(() => listarPets())
  .catch(error => console.error('Erro:', error));
}

function cadastrarVet() {
  fetch(`${API_VET}/vets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome: vetNome.value,
      especialidade: vetEspecialidade.value,
      endereco: vetEndereco.value,
      telefone: vetTelefone.value
    })
  })
  .then(() => {
    listarVets();
    vetNome.value = '';
    vetEspecialidade.value = '';
    vetEndereco.value = '';
    vetTelefone.value = '';
  })
  .catch(error => console.error('Erro:', error));
}

function listarVets() {
  fetch(`${API_VET}/vets`)
  .then(response => response.json())
  .then(vets => {
    vetsDiv.innerHTML = '';
    vetSelect.innerHTML = '<option value="">Selecione um vet</option>';
    vets.forEach(vet => {
      const div = document.createElement('div');
      div.innerHTML = `
        <h3>${vet.nome}</h3>
        <p>Especialidade: ${vet.especialidade || 'N/A'}</p>
        <p>Endereço: ${vet.endereco || 'N/A'}</p>
        <p>Telefone: ${vet.telefone || 'N/A'}</p>
        <button onclick="deletarVet(${vet.id})">Deletar</button>
      `;
      vetsDiv.appendChild(div);
      const option = document.createElement('option');
      option.value = vet.id;
      option.textContent = vet.nome;
      vetSelect.appendChild(option);
    });
  })
  .catch(error => console.error('Erro:', error));
}

function deletarVet(id) {
  fetch(`${API_VET}/vets/${id}`, { method: "DELETE" })
  .then(() => listarVets())
  .catch(error => console.error('Erro:', error));
}

function agendarConsulta() {
  fetch(`${API_VET}/appointments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      pet_id: parseInt(petSelect.value),
      vet_id: parseInt(vetSelect.value),
      data: appointmentData.value,
      motivo: appointmentMotivo.value
    })
  })
  .then(() => {
    listarAppointments();
    petSelect.value = '';
    vetSelect.value = '';
    appointmentData.value = '';
    appointmentMotivo.value = '';
  })
  .catch(error => console.error('Erro:', error));
}

function listarAppointments() {
  fetch(`${API_VET}/appointments`)
  .then(response => response.json())
  .then(appointments => {
    appointmentsDiv.innerHTML = '';
    appointments.forEach(app => {
      const div = document.createElement('div');
      div.innerHTML = `
        <p>Pet ID: ${app.pet_id}, Vet ID: ${app.vet_id}, Data: ${app.data}, Motivo: ${app.motivo || 'N/A'}</p>
        <button onclick="deletarAppointment(${app.id})">Deletar</button>
      `;
      appointmentsDiv.appendChild(div);
    });
  })
  .catch(error => console.error('Erro:', error));
}

function deletarAppointment(id) {
  fetch(`${API_VET}/appointments/${id}`, { method: "DELETE" })
  .then(() => listarAppointments())
  .catch(error => console.error('Erro:', error));
}

function buscarEndereco() {
  fetch(`${API_VET}/address/${cep.value}`)
  .then(response => response.json())
  .then(data => {
    if (data.erro) {
      enderecoDiv.innerHTML = '<p>CEP não encontrado</p>';
    } else {
      enderecoDiv.innerHTML = `
        <p>Logradouro: ${data.logradouro}</p>
        <p>Bairro: ${data.bairro}</p>
        <p>Cidade: ${data.localidade}</p>
        <p>UF: ${data.uf}</p>
      `;
    }
  })
  .catch(error => console.error('Erro:', error));
}

// Load data on page load
window.onload = function() {
  listarPets();
  listarVets();
  listarAppointments();
};