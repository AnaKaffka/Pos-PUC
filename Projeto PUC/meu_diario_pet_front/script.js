const API = "http://127.0.0.1:5000";

const nome = document.getElementById('nome');
const idade = document.getElementById('idade');
const tipo = document.getElementById('tipo');
const foto = document.getElementById('foto');
const petsDiv = document.getElementById('pets');
const diario = document.getElementById('diario');

function cadastrarPet() {
  console.log('Cadastrar pet chamado');
  console.log('Nome:', nome.value);
  console.log('Idade:', idade.value);
  console.log('Tipo:', tipo.value);
  const file = foto.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const fotoBase64 = e.target.result;
      console.log('Foto base64 length:', fotoBase64.length);
      enviarPet(fotoBase64);
    };
    reader.onerror = function(e) {
      console.error('Erro ao ler arquivo:', e);
    };
    reader.readAsDataURL(file);
  } else {
    console.log('Sem foto');
    enviarPet(null);
  }
}

function enviarPet(fotoBase64) {
  fetch(`${API}/pets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome: nome.value,
      idade: parseInt(idade.value),
      tipo: tipo.value,
      foto: fotoBase64
    })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Erro na requisição: ' + response.status);
    }
    return response.json();
  })
  .then(() => listarPets())
  .catch(error => console.error('Erro ao cadastrar pet:', error));
}

function listarPets() {
  fetch(`${API}/pets`)
    .then(r => r.json())
    .then(pets => {
      petsDiv.innerHTML = "";
      pets.forEach(p => {
        const img = p.foto ? `<img src="${p.foto}" alt="Foto do pet" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; margin-right: 15px;">` : '';
        const comida = p.ultima_comida ? `🥩 ${p.ultima_comida}<br>` : '';
        const vacinacao = p.ultima_vacinacao ? `💉 ${p.ultima_vacinacao}<br>` : '';
        const peso = p.ultimo_peso ? `⚖️ ${p.ultimo_peso}kg<br>` : '';
        petsDiv.innerHTML += `
          <div class="card" style="text-align: left;">
            <div style="display: flex; margin-bottom: 10px;">
              ${img}
              <div style="flex: 1;">
                ${comida}${vacinacao}${peso}
              </div>
            </div>
            <div>
              <b>${p.nome}</b> (${p.tipo})<br>
              <button onclick="abrirDiario(${p.id})">Abrir Diário</button>
              <span onclick="excluirPet(${p.id})" class="delete-btn" title="Excluir Pet">×</span>
            </div>
          </div>
        `;
      });
    })
    .catch(error => console.error('Erro ao listar pets:', error));
}

function abrirDiario(id) {
  // Fetch pet info to get photo
  fetch(`${API}/pets/${id}`)
    .then(r => r.json())
    .then(pet => {
      console.log('Pet data:', pet);
      console.log('Foto:', pet.foto);
      // Then fetch diary
      fetch(`${API}/pets/${id}/diario`)
        .then(r => r.json())
        .then(registros => {
          const img = pet.foto ? `<img src="${pet.foto}" alt="Foto do pet" style="width: 80px; height: 80px; object-fit: cover; margin-right: 10px; border: 1px solid #ccc;">` : '';
          diario.innerHTML = `
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
              ${img}
              <b>${pet.nome}</b>
            </div>
            <input type="file" id="novaFoto" accept="image/*">
            <button onclick="atualizarFoto(${id})">Atualizar Foto</button><br><br>
            <input id="comida" placeholder="Comida preferida">
            <input id="vet" placeholder="Veterinário">
            <input id="data" type="date">
            <input id="peso" type="number" placeholder="Peso">
            <input id="obs" placeholder="Observações">
            <button onclick="salvarDiario(${id})">Salvar</button>
          `;
          registros.forEach(r => {
            diario.innerHTML += `
              <div class="card">
                🥩 ${r.comida_preferida}<br>
                🩺 ${r.veterinario}<br>
                💉 ${r.data_vacinacao}<br>
                ⚖️ ${r.peso}kg<br>
                📝 ${r.observacoes}
              </div>
            `;
          });
        })
        .catch(error => console.error('Erro ao carregar diário:', error));
    })
    .catch(error => console.error('Erro ao carregar pet:', error));
}

function atualizarFoto(id) {
  const novaFotoInput = document.getElementById('novaFoto');
  const file = novaFotoInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const fotoBase64 = e.target.result;
      fetch(`${API}/pets/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          foto: fotoBase64
        })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro na atualização: ' + response.status);
        }
        return response.json();
      })
      .then(() => {
        alert('Foto atualizada!');
        listarPets(); // Update the pet list
        abrirDiario(id); // Refresh the diary view
      })
      .catch(error => console.error('Erro ao atualizar foto:', error));
    };
    reader.readAsDataURL(file);
  } else {
    alert('Selecione uma nova foto primeiro.');
  }
}

function excluirPet(id) {
  console.log('Excluir pet chamado para id:', id);
  if (confirm('Tem certeza que deseja excluir este pet?')) {
    console.log('Confirmação aceita, fazendo fetch');
    fetch(`${API}/pets/${id}`, {
      method: "DELETE"
    })
    .then(response => {
      console.log('Resposta recebida:', response.status);
      if (!response.ok) {
        throw new Error('Erro na exclusão: ' + response.status);
      }
      return response.json();
    })
    .then(data => {
      console.log('Dados da resposta:', data);
      alert('Pet excluído!');
      listarPets(); // Refresh the list
    })
    .catch(error => console.error('Erro ao excluir pet:', error));
  } else {
    console.log('Confirmação cancelada');
  }
}

function salvarDiario(id) {
  const comida = document.getElementById('comida');
  const vet = document.getElementById('vet');
  const data = document.getElementById('data');
  const peso = document.getElementById('peso');
  const obs = document.getElementById('obs');
  fetch(`${API}/pets/${id}/diario`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      comida_preferida: comida.value,
      veterinario: vet.value,
      data_vacinacao: data.value,
      peso: parseFloat(peso.value),
      observacoes: obs.value
    })
  }).then(() => abrirDiario(id));
}

listarPets();
