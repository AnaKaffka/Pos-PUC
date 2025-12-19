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
        const comida = p.comida_preferida ? `🥩 ${p.comida_preferida}<br>` : '';
        const veterinario = p.veterinario ? `🩺 ${p.veterinario}<br>` : '';
        const vacinacao = p.data_vacinacao ? `💉 ${p.data_vacinacao}<br>` : '';
        const peso = p.peso ? `⚖️ ${p.peso}kg<br>` : '';
        petsDiv.innerHTML += `
          <div class="card" style="text-align: left;">
            <div style="display: flex; margin-bottom: 10px;">
              ${img}
              <div style="flex: 1;">
                ${comida}${veterinario}${vacinacao}${peso}
              </div>
            </div>
            <div>
              <b>${p.nome}</b> (${p.tipo}, ${p.idade} anos)<br>
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
        .then(diarioData => {
          // Also fetch observações
          fetch(`${API}/pets/${id}/observacoes`)
            .then(r => r.json())
            .then(observacoes => {
              const img = pet.foto ? `<img src="${pet.foto}" alt="Foto do pet" style="width: 80px; height: 80px; object-fit: cover; margin-right: 10px; border: 1px solid #ccc;">` : '';
              const temDiario = diarioData && diarioData.id;
              const botaoTexto = temDiario ? 'Alterar' : 'Salvar';
              
              diario.innerHTML = `
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                  ${img}
                  <b>${pet.nome}</b>
                </div>
                <input type="file" id="novaFoto" accept="image/*">
                <button onclick="atualizarFoto(${id})">Atualizar Foto</button><br><br>
                <h3>Dados do Diário</h3>
                <input id="comida" placeholder="Comida preferida" value="${diarioData.comida_preferida || ''}">
                <input id="vet" placeholder="Veterinário" value="${diarioData.veterinario || ''}">
                <input id="data" type="date" value="${diarioData.data_vacinacao || ''}">
                <input id="peso" type="number" placeholder="Peso" value="${diarioData.peso || ''}">
                <input id="obs" placeholder="Observações" value="${diarioData.observacoes || ''}">
                <button onclick="salvarDiario(${id}, ${temDiario})">${botaoTexto}</button>
              `;
              
              // Add observações section
              diario.innerHTML += `<hr><h3>Observações (${observacoes.length})</h3>`;
              diario.innerHTML += `
                <div style="margin-bottom: 15px;">
                  <input type="date" id="dataObservacao" style="margin-bottom: 5px;">
                  <textarea id="textoObservacao" placeholder="Observação (máx 500 caracteres)" maxlength="500" style="width: 100%; height: 80px; margin-bottom: 5px;"></textarea>
                  <div style="font-size: 12px; margin-bottom: 5px;">
                    <span id="charCount">0</span>/500
                  </div>
                  <button onclick="salvarObservacao(${id})">Adicionar Observação</button>
                </div>
              `;
              // Update character counter
              document.getElementById('textoObservacao').addEventListener('input', (e) => {
                document.getElementById('charCount').textContent = e.target.value.length;
              });
              // Display observações
              if (observacoes.length === 0) {
                diario.innerHTML += `<p style="color: #999;">Nenhuma observação adicionada.</p>`;
              } else {
                observacoes.forEach(obs => {
                  diario.innerHTML += `
                    <div style="background: #fff; padding: 10px; margin: 5px 0; border-left: 3px solid #4CAF50; display: flex; justify-content: space-between; align-items: center;">
                      <div>
                        <strong>${obs.data}</strong><br>
                        ${obs.texto}
                      </div>
                      <button onclick="deletarObservacao(${obs.id})" style="background: #ff4444; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 3px;">✕</button>
                    </div>
                  `;
                });
              }
            })
            .catch(error => console.error('Erro ao carregar observações:', error));
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

function salvarDiario(id, temDiario) {
  console.log('Salvar diario chamado para id:', id, 'temDiario:', temDiario);
  const comida = document.getElementById('comida');
  const vet = document.getElementById('vet');
  const data = document.getElementById('data');
  const peso = document.getElementById('peso');
  const obs = document.getElementById('obs');
  
  console.log('Valores:', {
    comida: comida ? comida.value : 'undefined',
    vet: vet ? vet.value : 'undefined',
    data: data ? data.value : 'undefined',
    peso: peso ? peso.value : 'undefined',
    obs: obs ? obs.value : 'undefined'
  });
  
  if (!comida || !vet || !data || !peso || !obs) {
    console.error('Um ou mais campos não encontrados');
    alert('Erro: campos do diário não encontrados');
    return;
  }
  
  const metodo = temDiario ? "PUT" : "POST";
  
  fetch(`${API}/pets/${id}/diario`, {
    method: metodo,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      comida_preferida: comida.value,
      veterinario: vet.value,
      data_vacinacao: data.value,
      peso: parseFloat(peso.value),
      observacoes: obs.value
    })
  })
  .then(response => {
    console.log('Resposta status:', response.status);
    if (!response.ok) {
      throw new Error('Erro: ' + response.status);
    }
    return response.json();
  })
  .then(data => {
    console.log('Dados salvos:', data);
    const mensagem = temDiario ? 'Registro atualizado com sucesso!' : 'Registro salvo com sucesso!';
    alert(mensagem);
    abrirDiario(id);
  })
  .catch(error => {
    console.error('Erro ao salvar diario:', error);
    alert('Erro ao salvar: ' + error.message);
  });
}

function salvarObservacao(petId) {
  console.log('Salvar observação chamado para pet:', petId);
  const dataObs = document.getElementById('dataObservacao');
  const textoObs = document.getElementById('textoObservacao');
  
  if (!dataObs || !textoObs) {
    console.error('Campos de observação não encontrados');
    alert('Erro: campos não encontrados');
    return;
  }
  
  if (!dataObs.value || !textoObs.value) {
    alert('Preencha a data e o texto da observação');
    return;
  }
  
  if (textoObs.value.length > 500) {
    alert('O texto não pode ter mais de 500 caracteres');
    return;
  }
  
  fetch(`${API}/pets/${petId}/observacoes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      data: dataObs.value,
      texto: textoObs.value
    })
  })
  .then(response => {
    console.log('Resposta status:', response.status);
    if (!response.ok) {
      throw new Error('Erro: ' + response.status);
    }
    return response.json();
  })
  .then(data => {
    console.log('Observação salva:', data);
    document.getElementById('dataObservacao').value = '';
    document.getElementById('textoObservacao').value = '';
    document.getElementById('charCount').textContent = '0';
    alert('Observação adicionada!');
    abrirDiario(petId);
  })
  .catch(error => {
    console.error('Erro ao salvar observação:', error);
    alert('Erro ao salvar: ' + error.message);
  });
}

function deletarObservacao(obsId) {
  console.log('Deletar observação chamado para id:', obsId);
  if (confirm('Tem certeza que deseja deletar esta observação?')) {
    fetch(`${API}/observacoes/${obsId}`, {
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
      console.log('Observação deletada:', data);
      alert('Observação removida!');
      // Get the pet ID from the currently displayed diario
      // We need to pass it somehow - for now, we'll refetch the diary
      const petName = document.querySelector('[onclick*="abrirDiario"]')?.textContent || '';
      location.reload();
    })
    .catch(error => console.error('Erro ao deletar observação:', error));
  }
}

listarPets();