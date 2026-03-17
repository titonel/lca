// Exemplo de como usar JS para carregar dados no Modal de Edição
function editarPaciente(id) {
    console.log("Iniciando edição do ID:", id);

    fetch('/api/paciente/' + id + '/')
        .then(r => r.json())
        .then(data => {
            if(data.status === 'error') throw new Error(data.message);

            safeSet('paciente_id', data.id);
            safeSet('nome', data.nome);
            safeSet('nascimento', data.nascimento);
            safeSet('data_insercao', data.data_insercao);
            safeSet('cpf', data.cpf);
            safeSet('cross', data.cross);
            safeSet('sexo', data.sexo);
            safeSet('municipio', data.municipio);
            safeSet('medico', data.medico);
            safeSet('indicacao', data.indicacao);
            safeSet('meta', data.meta);

            // Atualiza título
            const titulo = document.getElementById('modalTitulo');
            if(titulo) titulo.innerText = 'Editar: ' + data.nome;

            // Abre o modal
            abrirModal();
        })
        .catch(e => alert('Erro: ' + e));
}

function novoPaciente() {
    const form = document.getElementById('formPaciente');
    if (form) form.reset();
    safeSet('paciente_id', '');

    // Define a data de hoje automaticamente para novos pacientes
    const hoje = new Date().toISOString().split('T')[0];
    safeSet('data_insercao', hoje);

    document.getElementById('modalTitulo').innerText = 'Novo Paciente';
    abrirModal();
}

// FUNÇÃO DE SEGURANÇA
function safeSet(elementId, value) {
    const el = document.getElementById(elementId);
    if (el) {
        el.value = value;
    } else {
        console.warn(`ATENÇÃO: Campo com id '${elementId}' não encontrado no HTML.`);
    }
}

function abrirModal() {
    const modalEl = document.getElementById('modalPaciente');
    if (modalEl) {
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
    } else {
        console.error("Modal #modalPaciente não encontrado!");
    }
}