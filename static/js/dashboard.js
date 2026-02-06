document.addEventListener('DOMContentLoaded', () => {

    // 1. Auth Check
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/static/login.html';
        return;
    }

    // 2. Decode Token
    let userRole = 'member';
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        document.getElementById('userNameDisplay').textContent = payload.sub || 'Usuário';
        userRole = payload.role || 'member';
        console.log("User Role:", userRole);
    } catch (e) {
        console.error('Invalid token format');
        localStorage.removeItem('access_token');
        window.location.href = '/static/login.html';
    }

    // 3. Logout Logic
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '/static/login.html';
    });

    // 4. Navigation Logic
    const navItems = document.querySelectorAll('.nav-item');
    const pageTitle = document.getElementById('pageTitle');
    const contentArea = document.getElementById('contentArea');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            const target = item.dataset.target;
            handleNavigation(target);
        });
    });

    function handleNavigation(target) {
        let title = 'Busca de Currículos';
        let content = '';

        switch (target) {
            case 'search':
                title = 'Busca Semântica';
                content = `
                    <div class="search-container">
                        <div class="search-bar">
                            <input type="text" id="searchInput" placeholder="Descreva o perfil do candidato (ex: Desenvolvedor Python com experiência em AWS)..." style="flex: 1; padding: 1rem; border: 1px solid #ccc; border-radius: 6px;">
                            <button class="btn-primary" id="btnSearch">Buscar</button>
                        </div>
                        <div id="searchResults">
                            <!-- Results will appear here -->
                            <div class="placeholder-content">
                                <p>Digite uma descrição e clique em buscar.</p>
                            </div>
                        </div>
                    </div>
                `;
                break;
            case 'upload':
                title = 'Upload de Currículos';
                content = `
                    <div class="upload-container">
                        <div class="drop-zone" id="dropZone">
                            <p style="margin-bottom: 1rem;">Arraste arquivos (PDF/DOC/DOCX) aqui ou clique para selecionar</p>
                            <input type="file" id="fileInput" accept=".pdf,.doc,.docx" multiple style="display: none;">
                            <button class="btn-primary" id="btnSelectFile">Selecionar Arquivos</button>
                            <div id="uploadFeedback" style="text-align: left;"></div>
                        </div>
                    </div>
                `;
                break;
            case 'jobs':
                title = 'Gestão de Vagas';
                content = `
                    <div class="jobs-container">
                        <div class="jobs-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                            <p>Gerencie as vagas abertas e seus requisitos.</p>
                            <div style="display: flex; gap: 1rem; align-items: center;">
                                <div class="view-toggle" style="background: #F3F4F6; padding: 0.25rem; border-radius: 6px; display: flex;">
                                    <button id="btnViewGrid" class="active" style="padding: 0.25rem 0.5rem; border: none; background: white; border-radius: 4px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">⊞ Grid</button>
                                    <button id="btnViewList" style="padding: 0.25rem 0.5rem; border: none; background: transparent; border-radius: 4px; cursor: pointer;">☰ Lista</button>
                                </div>
                                <button class="btn-primary" id="btnNewJob" style="${userRole === 'admin' ? '' : 'display:none'}">+ Nova Vaga</button>
                            </div>
                        </div>
                        
                        <div id="jobsContainer">
                            <div id="jobsList" class="jobs-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem;">
                                <div class="loading-spinner"></div>
                            </div>
                            
                            <!-- Table View (Hidden by default) -->
                            <div id="jobsTableContainer" style="display: none; width: 100%; overflow-x: auto;">
                                <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                                    <thead style="background: #F9FAFB; text-align: left; font-size: 0.875rem; color: #6B7280; font-weight: 500;">
                                        <tr>
                                            <th style="padding: 0.75rem 1rem;">ID</th>
                                            <th style="padding: 0.75rem 1rem;">Título</th>
                                            <th style="padding: 0.75rem 1rem;">Localização</th>
                                            <th style="padding: 0.75rem 1rem;">Descrição</th>
                                            <th style="padding: 0.75rem 1rem;">Status</th>
                                            <th style="padding: 0.75rem 1rem; text-align: right;">Ações</th>
                                        </tr>
                                    </thead>
                                    <tbody id="jobsTableBody" style="font-size: 0.9rem; color: #374151;">
                                        <!-- Rows will be injected here -->
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Create/Edit Job Modal -->
                        <div id="jobModal" class="modal-overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center;">
                             <div class="modal-content" style="background: white; padding: 2rem; border-radius: 8px; width: 90%; max-width: 600px; max-height: 90vh; overflow-y: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                <h3 id="jobModalTitle" style="margin-bottom: 1.5rem; font-size: 1.25rem;">Nova Vaga</h3>
                                <form id="jobForm" style="display: grid; gap: 1rem;">
                                    <input type="hidden" id="jobId"> <!-- Hidden ID for updates -->
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                                        <div>
                                            <label style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500;">Título da Vaga</label>
                                            <input type="text" id="jobTitle" required style="width: 100%; padding: 0.5rem; border: 1px solid #D1D5DB; border-radius: 4px;">
                                        </div>
                                        <div>
                                            <label style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500;">Status</label>
                                            <select id="jobStatus" style="width: 100%; padding: 0.5rem; border: 1px solid #D1D5DB; border-radius: 4px;">
                                                <option value="Open">Aberto</option>
                                                <option value="Draft">Rascunho</option>
                                                <option value="Closed">Fechado</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                                        <div>
                                            <label style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500;">Departamento</label>
                                            <input type="text" id="jobDepartment" style="width: 100%; padding: 0.5rem; border: 1px solid #D1D5DB; border-radius: 4px;">
                                        </div>
                                    </div>
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                                        <div>
                                            <label style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500;">Localização</label>
                                            <input type="text" id="jobLocation" style="width: 100%; padding: 0.5rem; border: 1px solid #D1D5DB; border-radius: 4px;">
                                        </div>
                                        <div>
                                            <label style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500;">Tipo de Contrato</label>
                                            <select id="jobContract" style="width: 100%; padding: 0.5rem; border: 1px solid #D1D5DB; border-radius: 4px;">
                                                <option value="CLT">CLT</option>
                                                <option value="PJ">PJ</option>
                                                <option value="Estágio">Estágio</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div>
                                        <label style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500;">Descrição</label>
                                        <textarea id="jobDescription" rows="4" style="width: 100%; padding: 0.5rem; border: 1px solid #D1D5DB; border-radius: 4px;"></textarea>
                                    </div>
                                    <div>
                                        <label style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500;">Requisitos</label>
                                        <textarea id="jobRequirements" rows="4" style="width: 100%; padding: 0.5rem; border: 1px solid #D1D5DB; border-radius: 4px;"></textarea>
                                    </div>
                                    <div style="display: flex; gap: 1rem; justify-content: flex-end; margin-top: 1rem;">
                                        <button type="button" id="btnCancelJob" style="padding: 0.5rem 1rem; background: transparent; border: 1px solid #D1D5DB; border-radius: 4px; cursor: pointer;">Cancelar</button>
                                        <button type="submit" class="btn-primary">Salvar Vaga</button>
                                    </div>
                                </form>
                             </div>
                        </div>

                        <!-- Candidates Modal -->
                        <div id="candidatesModal" class="modal-overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center;">
                            <div class="modal-content" style="background: white; padding: 2rem; border-radius: 8px; width: 90%; max-width: 800px; max-height: 90vh; overflow-y: auto;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                                    <h3 id="modalTitle">Candidatos Sugeridos</h3>
                                    <button id="btnCloseModal" style="background: none; border: none; font-size: 1.5rem; cursor: pointer;">&times;</button>
                                </div>
                                <div id="modalBody">
                                    <div class="loading-spinner"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                break;
            case 'history':
                title = 'Histórico';
                content = `
                    <div class="history-container">
                        <div class="tabs" style="display: flex; gap: 1rem; margin-bottom: 1.5rem; border-bottom: 1px solid #E5E7EB;">
                            <button id="tabSearchHistory" class="tab-btn active" style="padding: 0.75rem 1rem; border: none; background: none; border-bottom: 2px solid #4F46E5; color: #4F46E5; font-weight: 500; cursor: pointer;">Buscas</button>
                            <button id="tabChatHistory" class="tab-btn" style="padding: 0.75rem 1rem; border: none; background: none; border-bottom: 2px solid transparent; color: #6B7280; font-weight: 500; cursor: pointer;">Chat Assistente</button>
                        </div>
                        <div id="historyContent">
                            <div class="loading-spinner"></div>
                        </div>
                    </div>
                `;
                break;
            case 'settings':
                title = 'Configurações';
                content = '<div class="placeholder-content"><p>Configurações do Sistema (Em breve)</p></div>';
                break;
        }

        pageTitle.textContent = title;
        contentArea.innerHTML = content;

        // Attach event listeners after content injection
        if (target === 'search') {
            document.getElementById('btnSearch').addEventListener('click', performSearch);
            document.getElementById('searchInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') performSearch();
            });
        } else if (target === 'upload') {
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            const btnSelect = document.getElementById('btnSelectFile');

            btnSelect.addEventListener('click', () => fileInput.click());

            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) handleFiles(e.target.files);
            });

            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.style.borderColor = '#4F46E5';
                dropZone.style.backgroundColor = '#EEF2FF';
            });

            dropZone.addEventListener('dragleave', (e) => {
                e.preventDefault();
                dropZone.style.borderColor = '#E5E7EB';
                dropZone.style.backgroundColor = 'white';
            });

            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.style.borderColor = '#E5E7EB';
                dropZone.style.backgroundColor = 'white';
                if (e.dataTransfer.files.length > 0) handleFiles(e.dataTransfer.files);
            });
        } else if (target === 'jobs') {
            // View Toggle Logic
            const btnGrid = document.getElementById('btnViewGrid');
            const btnList = document.getElementById('btnViewList');

            // Set initial state from global or default logic
            updateView(window.jobsViewMode || 'grid');

            btnGrid.addEventListener('click', () => updateView('grid'));
            btnList.addEventListener('click', () => updateView('list'));

            function updateView(mode) {
                window.jobsViewMode = mode;

                // Update Button Styles
                if (mode === 'grid') {
                    btnGrid.style.background = 'white';
                    btnGrid.style.boxShadow = '0 1px 2px rgba(0,0,0,0.1)';
                    btnList.style.background = 'transparent';
                    btnList.style.boxShadow = 'none';

                    document.getElementById('jobsList').style.display = 'flex';
                    document.getElementById('jobsTableContainer').style.display = 'none';
                } else {
                    btnList.style.background = 'white';
                    btnList.style.boxShadow = '0 1px 2px rgba(0,0,0,0.1)';
                    btnGrid.style.background = 'transparent';
                    btnGrid.style.boxShadow = 'none';

                    document.getElementById('jobsList').style.display = 'none';
                    document.getElementById('jobsTableContainer').style.display = 'block';
                }
            }



            loadJobs(); // Will now handle both renders

            const btnNewJob = document.getElementById('btnNewJob');
            const jobModal = document.getElementById('jobModal');
            const btnCancelJob = document.getElementById('btnCancelJob');
            const form = document.getElementById('jobForm');
            const candidatesModal = document.getElementById('candidatesModal');
            const btnCloseCandidatesModal = document.getElementById('btnCloseModal');

            // Open Create Modal
            btnNewJob.addEventListener('click', () => {
                document.getElementById('jobModalTitle').textContent = 'Nova Vaga';
                document.getElementById('jobId').value = '';
                document.getElementById('jobStatus').value = 'Open';
                form.reset();
                jobModal.style.display = 'flex';
            });

            // Close Job Modal
            btnCancelJob.addEventListener('click', () => {
                jobModal.style.display = 'none';
                form.reset();
            });

            // Handle Job Form Submit
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                await saveJob();
            });


            // Close Job Modal on click outside
            jobModal.addEventListener('click', (e) => {
                if (e.target === jobModal) jobModal.style.display = 'none';
            });


            // Close Candidates Modal
            btnCloseCandidatesModal.addEventListener('click', () => {
                candidatesModal.style.display = 'none';
            });

            // Close Candidates Modal on click outside
            candidatesModal.addEventListener('click', (e) => {
                if (e.target === candidatesModal) candidatesModal.style.display = 'none';
            });
        } else if (target === 'history') {
            loadSearchHistory();

            const tabSearch = document.getElementById('tabSearchHistory');
            const tabChat = document.getElementById('tabChatHistory');

            tabSearch.addEventListener('click', () => {
                tabSearch.classList.add('active');
                tabSearch.style.borderBottomColor = '#4F46E5';
                tabSearch.style.color = '#4F46E5';

                tabChat.classList.remove('active');
                tabChat.style.borderBottomColor = 'transparent';
                tabChat.style.color = '#6B7280';

                loadSearchHistory();
            });

            tabChat.addEventListener('click', () => {
                tabChat.classList.add('active');
                tabChat.style.borderBottomColor = '#4F46E5';
                tabChat.style.color = '#4F46E5';

                tabSearch.classList.remove('active');
                tabSearch.style.borderBottomColor = 'transparent';
                tabSearch.style.color = '#6B7280';

                loadChatHistory();
            });
        }
    }

    // --- History Logic ---
    async function loadSearchHistory() {
        const container = document.getElementById('historyContent');
        container.innerHTML = '<div class="loading-spinner"></div>';

        try {
            const response = await fetch('/api/history/prompts', {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) throw new Error('Failed to fetch history');

            const history = await response.json();

            if (history.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #6B7280; padding: 2rem;">Nenhuma busca recente.</p>';
                return;
            }

            container.innerHTML = history.map(item => `
                <div class="result-card" style="margin-bottom: 1rem; border-left: 4px solid #4F46E5;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-weight: 500; font-size: 1.1rem;">"${item.prompt}"</span>
                        <span style="font-size: 0.8rem; color: #6B7280;">${new Date(item.created_at).toLocaleString()}</span>
                    </div>
                </div>
            `).join('');

        } catch (error) {
            container.innerHTML = '<p style="color: red; text-align: center;">Erro ao carregar histórico.</p>';
        }
    }

    async function loadChatHistory() {
        const container = document.getElementById('historyContent');
        container.innerHTML = '<div class="loading-spinner"></div>';

        try {
            const response = await fetch('/api/history/chat', {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) throw new Error('Failed to fetch chat history');

            const history = await response.json();

            if (history.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #6B7280; padding: 2rem;">Nenhuma conversa recente.</p>';
                return;
            }

            container.innerHTML = history.map(item => `
                <div class="result-card" style="margin-bottom: 1rem; border-left: 4px solid #10B981;">
                     <div style="margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                        <strong style="color: #374151;">Você:</strong>
                        <span style="font-size: 0.8rem; color: #6B7280;">${new Date(item.created_at).toLocaleString()}</span>
                    </div>
                    <p style="margin-bottom: 1rem; color: #4B5563;">${item.pergunta}</p>
                    <div style="border-top: 1px solid #E5E7EB; padding-top: 0.5rem;">
                        <strong style="color: #059669;">Assistente:</strong>
                        <p style="margin-top: 0.25rem; font-size: 0.9rem; color: #374151; white-space: pre-wrap;">${item.resposta ? item.resposta.substring(0, 300) + (item.resposta.length > 300 ? '...' : '') : '...'}</p>
                    </div>
                </div>
            `).join('');

        } catch (error) {
            container.innerHTML = '<p style="color: red; text-align: center;">Erro ao carregar histórico.</p>';
        }
    }

    // --- Jobs Logic ---
    async function loadJobs() {
        const listDiv = document.getElementById('jobsList');
        const tableBody = document.getElementById('jobsTableBody');

        try {
            const response = await fetch('/api/jobs/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.status === 401) {
                // handle auth
                return;
            }

            const jobs = await response.json();

            if (jobs.length === 0) {
                listDiv.innerHTML = '<p style="text-align: center; color: #6B7280; width: 100%; grid-column: 1 / -1;">Nenhuma vaga cadastrada ainda.</p>';
                tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem; color: #6B7280;">Nenhuma vaga cadastrada.</td></tr>';
                return;
            }

            const getStatusColor = (status) => {
                const s = (status || 'Open').toLowerCase();
                if (s === 'open' || s === 'aberto') return { bg: '#ECFDF5', text: '#047857' };
                if (s === 'closed' || s === 'fechado' || s === 'closed') return { bg: '#F3F4F6', text: '#374151' };
                if (s === 'draft' || s === 'rascunho') return { bg: '#FFFBEB', text: '#B45309' };
                return { bg: '#ECFDF5', text: '#047857' };
            };

            const renderStatusBadge = (status) => {
                const style = getStatusColor(status);
                return `<span style="background: ${style.bg}; color: ${style.text}; padding: 0.1rem 0.4rem; border-radius: 99px; font-size: 0.75rem;">${status}</span>`;
            };

            // --- RENDER GRID (Now Flexbox for Fluid Width) ---
            // Filter: Only show "Open" jobs in Grid View
            const gridJobs = jobs.filter(job => {
                const s = (job.status || 'Open').toLowerCase();
                return s === 'open' || s === 'aberto';
            });

            // Container style: display: flex; flex-wrap: wrap; gap: 1.5rem;
            // Container style: display: flex; flex-wrap: wrap; gap: 1.5rem;
            // Only set display if currently visible (or let updateView handle it)
            if (window.jobsViewMode !== 'list') {
                listDiv.style.display = 'flex';
            }
            listDiv.style.flexWrap = 'wrap';
            listDiv.style.gap = '1.5rem';
            listDiv.style.gridTemplateColumns = ''; // Reset grid style if applied via class

            if (gridJobs.length === 0) {
                listDiv.innerHTML = '<p style="text-align: center; color: #6B7280; width: 100%;">Nenhuma vaga aberta no momento.</p>';
            } else {
                listDiv.innerHTML = gridJobs.map(job => `
                    <div class="result-card" style="flex: 1 1 300px; display: flex; flex-direction: column; justify-content: space-between; min-width: 300px;">
                        <div>
                            <div class="result-header">
                                <div class="result-title" style="word-break: break-word; line-height: 1.2;" title="${job.title}">${job.title}</div>
                                <div class="result-score" style="display: flex; align-items: center; white-space: nowrap; margin-left: 0.5rem;">${renderStatusBadge(job.status)}</div>
                            </div>
                        <div class="result-meta" style="margin-bottom: 0.75rem;">
                            ${job.department || 'Geral'} • ${job.location || 'Remoto'} <br>
                            ${job.contract_type || 'N/A'}
                        </div>
                        <p style="color: #4B5563; font-size: 0.85rem; margin-bottom: 0.5rem; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">
                            ${job.description || 'Sem descrição.'}
                        </p>
                         <p style="color: #6B7280; font-size: 0.8rem; margin-bottom: 1rem;">
                            <strong>Requisitos:</strong> ${(job.requirements || 'N/A').substring(0, 50)}${(job.requirements && job.requirements.length > 50) ? '...' : ''}
                        </p>
                    </div>
                    
                    <div style="border-top: 1px solid #E5E7EB; padding-top: 0.75rem; display: flex; justify-content: space-between; align-items: center;">
                         <div style="display: flex; gap: 0.5rem; ${userRole === 'admin' ? '' : 'visibility: hidden;'}">
                             <button class="btn-action" onclick="editJob(${job.id})" title="Editar" aria-label="Editar" style="color: #4B5563; background: #F3F4F6; border: none; border-radius: 4px; padding: 0.4rem; cursor: pointer; transition: background 0.2s;">✏️</button>
                             <button class="btn-action" onclick="deleteJob(${job.id})" title="Excluir" aria-label="Excluir" style="color: #DC2626; background: #FEE2E2; border: none; border-radius: 4px; padding: 0.4rem; cursor: pointer; transition: background 0.2s;">🗑️</button>
                         </div>
                         <button class="btn-view-candidates" data-id="${job.id}" onclick="viewCandidates(${job.id}, '${job.title}')" style="color: #4F46E5; background: none; border: none; font-weight: 500; cursor: pointer; font-size: 0.85rem;">Ver Candidatos ✨</button>
                    </div>
                </div>
            `).join('');
            }

            // --- RENDER TABLE ---
            tableBody.innerHTML = jobs.map(job => `
                <tr style="border-bottom: 1px solid #E5E7EB; transition: background 0.1s;" onmouseover="this.style.background='#F9FAFB'" onmouseout="this.style.background='white'">
                    <td style="padding: 0.75rem 1rem; color: #6B7280;">#${job.id}</td>
                    <td style="padding: 0.75rem 1rem; font-weight: 500; color: #111827;">${job.title}</td>
                    <td style="padding: 0.75rem 1rem; color: #4B5563;">${job.location || '-'}</td>
                    <td style="padding: 0.75rem 1rem; color: #4B5563; max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${job.description || ''}">
                        ${job.description || '-'}
                    </td>
                    <td style="padding: 0.75rem 1rem;">
                        ${renderStatusBadge(job.status)}
                    </td>
                    <td style="padding: 0.75rem 1rem; text-align: right; white-space: nowrap;">
                        <div style="display: inline-flex; gap: 0.5rem; ${userRole === 'admin' ? '' : 'visibility: hidden;'}">
                            <button onclick="editJob(${job.id})" title="Editar" style="color: #4B5563; background: none; border: none; cursor: pointer;">✏️</button>
                            <button onclick="deleteJob(${job.id})" title="Excluir" style="color: #DC2626; background: none; border: none; cursor: pointer;">🗑️</button>
                        </div>
                    </td>
                </tr>
            `).join('');

        } catch (error) {
            console.error(error);
            listDiv.innerHTML = '<p style="color: red;">Erro ao carregar vagas.</p>';
            tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: red;">Erro ao carregar dados.</td></tr>';
        }
    }

    // Expose to global scope for onclick or attach safely
    window.viewCandidates = async (jobId, jobTitle) => {
        const modal = document.getElementById('candidatesModal');
        const modalBody = document.getElementById('modalBody');
        const modalTitle = document.getElementById('modalTitle');

        modalTitle.textContent = `Candidatos para: ${jobTitle}`;
        modal.style.display = 'flex';
        modalBody.innerHTML = '<div class="loading-spinner"></div>';

        try {
            const response = await fetch(`/api/jobs/${jobId}/matches`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) throw new Error('Failed to fetch matches');

            const matches = await response.json();
            renderResults(matches, modalBody); // Reuse existing render logic

        } catch (error) {
            modalBody.innerHTML = `<p style="color: red;">Erro ao buscar candidatos: ${error.message}</p>`;
        }
    };

    // --- CRUD Logic ---

    // Expose functions globally
    window.deleteJob = async (id) => {
        if (!confirm('Tem certeza que deseja excluir esta vaga?')) return;

        try {
            const response = await fetch(`/api/jobs/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                loadJobs();
            } else {
                alert('Erro ao excluir vaga');
            }
        } catch (e) {
            console.error(e);
            alert('Erro ao excluir vaga');
        }
    };

    window.editJob = async (id) => {
        try {
            const response = await fetch(`/api/jobs/${id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) throw new Error('Erro ao buscar detalhes');
            const job = await response.json();

            // Populate Form
            document.getElementById('jobId').value = job.id;
            document.getElementById('jobTitle').value = job.title;
            document.getElementById('jobStatus').value = job.status || 'Open';
            document.getElementById('jobDepartment').value = job.department || '';
            document.getElementById('jobLocation').value = job.location || '';
            document.getElementById('jobContract').value = job.contract_type || 'CLT';
            document.getElementById('jobDescription').value = job.description || '';
            document.getElementById('jobRequirements').value = job.requirements || '';

            // Update Modal Title
            document.getElementById('jobModalTitle').textContent = 'Editar Vaga';

            // Show Modal
            document.getElementById('jobModal').style.display = 'flex';

        } catch (e) {
            console.error(e);
            alert('Erro ao carregar dados da vaga');
        }
    };

    async function saveJob() {
        const title = document.getElementById('jobTitle').value;
        const status = document.getElementById('jobStatus').value;
        const department = document.getElementById('jobDepartment').value;
        const location = document.getElementById('jobLocation').value;
        const contract = document.getElementById('jobContract').value;
        const description = document.getElementById('jobDescription').value;
        const requirements = document.getElementById('jobRequirements').value;

        const jobData = {
            title,
            status,
            department,
            location,
            contract_type: contract,
            description,
            requirements
        };

        const jobId = document.getElementById('jobId').value;
        const method = jobId ? 'PUT' : 'POST';
        const url = jobId ? `/api/jobs/${jobId}` : '/api/jobs/';

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jobData)
            });

            if (!response.ok) throw new Error('Failed to save job');

            // Reset and Close Modal
            document.getElementById('jobForm').reset();
            document.getElementById('jobId').value = '';
            document.getElementById('jobModal').style.display = 'none';
            loadJobs();

        } catch (error) {
            alert('Erro ao criar vaga: ' + error.message);
        }
    }

    // --- Search Logic ---
    async function performSearch() {
        const query = document.getElementById('searchInput').value;
        const resultsDiv = document.getElementById('searchResults');

        if (!query.trim()) return;

        resultsDiv.innerHTML = '<div class="loading-spinner"></div>';

        try {
            const response = await fetch(`/api/query/simples?search=${encodeURIComponent(query)}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 401) {
                alert('Sessão expirada. Faça login novamente.');
                localStorage.removeItem('access_token');
                window.location.href = '/static/login.html';
                return;
            }

            if (!response.ok) throw new Error('Falha na busca');

            const data = await response.json();
            renderResults(data, resultsDiv);
        } catch (error) {
            console.error(error);
            resultsDiv.innerHTML = '<p style="color: red; text-align: center;">Erro ao realizar busca.</p>';
        }
    }

    function renderResults(data, container) {
        // Handle both Array (direct matches) and Object (job + matches)
        let results = [];
        if (Array.isArray(data)) {
            results = data;
        } else if (data && data.matches && Array.isArray(data.matches)) {
            results = data.matches;
        }

        if (!results || results.length === 0) {
            container.innerHTML = '<div class="placeholder-content"><p>Nenhum resultado encontrado.</p></div>';
            return;
        }

        const html = results.map((item, index) => {
            const meta = item.metadata || {};
            const score = (item.score * 100).toFixed(1);

            // Parse nested JSON if it exists as string OR use object if already parsed
            let enriched = {};
            if (meta.full_enriched_json) {
                enriched = meta.full_enriched_json;
                if (typeof enriched === 'string') {
                    try {
                        enriched = JSON.parse(enriched);
                    } catch (e) {
                        console.error("Error parsing full_enriched_json", e);
                    }
                }
            }

            // Extract fields for display
            const skills = enriched.perfil_profissional?.habilidades_tecnicas ||
                (Array.isArray(meta.skills) ? meta.skills : []) || [];

            const commonSkills = item.common_skills || []; // Explainability

            const education = enriched.formacao_academica || [];
            const experience = enriched.experiencia_profissional || [];
            const summary = enriched.contexto?.resumo_profissional || "";
            const phones = enriched.candidato?.telefones || [];
            const linkedin = enriched.candidato?.linkedin_url || "";
            const github = enriched.candidato?.github_url || "";
            const city = enriched.candidato?.cidade || "";
            const state = enriched.candidato?.estado || "";
            const location = [city, state].filter(Boolean).join(' - ');

            const skillsHtml = skills.slice(0, 5).map(s => `<span class="skill-tag">${s}</span>`).join('');
            const allSkillsHtml = skills.map(s => `<span class="skill-tag" style="background: #E0E7FF; color: #3730A3;">${s}</span>`).join('');

            // Render Common Skills (Explainability)
            const commonSkillsHtml = commonSkills.length > 0
                ? `<div style="margin-bottom: 0.5rem;">
                     <strong style="font-size: 0.85rem; color: #047857;">Skills em Comum:</strong>
                     <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.25rem;">
                        ${commonSkills.map(s => `<span class="skill-tag" style="background: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0;">${s}</span>`).join('')}
                     </div>
                   </div>`
                : '';

            // Generate Education HTML
            const eduHtml = education.map(edu => `
                <div style="margin-bottom: 0.5rem; font-size: 0.9rem;">
                    <strong>${edu.curso || 'Curso'}</strong> - ${edu.instituicao || ''} <br>
                    <span style="color: #6B7280; font-size: 0.85rem;">${edu.ano_conclusao || ''}</span>
                </div>
            `).join('');

            // Generate Experience HTML
            const expHtml = experience.map(exp => `
                <div style="margin-bottom: 0.8rem; font-size: 0.9rem; border-left: 2px solid #E5E7EB; padding-left: 0.5rem;">
                    <strong>${exp.cargo || 'Cargo'}</strong> na ${exp.empresa || 'Empresa'} <br>
                    <span style="color: #6B7280; font-size: 0.85rem;">${exp.periodo || ''}</span>
                    <p style="font-size: 0.85rem; margin-top: 0.25rem;">${exp.descricao || ''}</p>
                </div>
            `).join('');

            const uniqueId = `details-${index}-${Date.now()}`;

            return `
                <div class="result-card" style="margin-bottom: 1rem;">
                    <div class="result-header">
                        <div class="result-title">${meta.candidate_name || 'Candidato Desconhecido'}</div>
                        <div class="result-score">${score}% Match</div>
                    </div>
                    <div class="result-meta">
                        ${meta.education_level || ''} • ${meta.seniority_inferred || ''} ${location ? ' • ' + location : ''} <br>
                        Email: ${meta.email || 'N/A'} ${phones.length ? ' • Tel: ' + phones.join(', ') : ''}
                    </div>
                    
                    ${commonSkillsHtml} <!-- EXPLAINABILITY -->

                    <!-- 
                    <div style="margin-top: 0.5rem; margin-bottom: 0.5rem;">
                        <strong>Principais Habilidades:</strong>
                        <div class="result-skills" style="margin-top: 0.25rem;">
                            ${skillsHtml} ${skills.length > 5 ? `<span style="font-size: 0.8rem; color: #6B7280;">+${skills.length - 5} mais</span>` : ''}
                        </div>
                    </div> -->
                    
                    <button onclick="document.getElementById('${uniqueId}').style.display = document.getElementById('${uniqueId}').style.display === 'none' ? 'block' : 'none'" 
                            style="width: 100%; padding: 0.5rem; background: #F3F4F6; border: none; border-radius: 4px; cursor: pointer; color: #374151; font-weight: 500; margin-top: 0.5rem;">
                        Ver Perfil Completo ▼
                    </button>

                    <div id="${uniqueId}" style="display: none; margin-top: 1rem; border-top: 1px solid #E5E7EB; padding-top: 1rem;">
                        ${summary ? `<div style="margin-bottom: 1rem;"><strong>Resumo:</strong><p style="font-size: 0.9rem; color: #4B5563;">${summary}</p></div>` : ''}
                        
                        <!-- Contact / Social Links -->
                         <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap;">
                            ${linkedin ? `<a href="${linkedin.startsWith('http') ? linkedin : 'https://' + linkedin}" target="_blank" style="color: #0077b5; text-decoration: none; font-weight: 500;">🔗 LinkedIn</a>` : ''}
                            ${github ? `<a href="${github.startsWith('http') ? github : 'https://' + github}" target="_blank" style="color: #333; text-decoration: none; font-weight: 500;">💻 GitHub</a>` : ''}
                         </div>

                        <!-- Extra Context Fields -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; background: #F9FAFB; padding: 0.8rem; border-radius: 6px;">
                            ${enriched.contexto?.objetivo_profissional ? `<div><strong>Objetivo:</strong><p style="font-size: 0.85rem; color: #4B5563;">${enriched.contexto.objetivo_profissional}</p></div>` : ''}
                            ${enriched.contexto?.area_atuacao ? `<div><strong>Área:</strong><p style="font-size: 0.85rem; color: #4B5563;">${enriched.contexto.area_atuacao}</p></div>` : ''}
                            ${enriched.contexto?.anos_experiencia ? `<div><strong>Exp (Anos):</strong><p style="font-size: 0.85rem; color: #4B5563;">${enriched.contexto.anos_experiencia}</p></div>` : ''}
                            ${enriched.contexto?.disponibilidade ? `<div><strong>Disponibilidade:</strong><p style="font-size: 0.85rem; color: #4B5563;">${enriched.contexto.disponibilidade}</p></div>` : ''}
                        </div>

                        <div style="margin-bottom: 1rem;">
                            <h4 style="margin-bottom: 0.5rem;">Habilidades Técnicas (Todas)</h4>
                            <div class="result-skills">${allSkillsHtml}</div>
                        </div>

                        <!-- Soft Skills -->
                         ${enriched.perfil_profissional?.habilidades_comportamentais?.length ? `
                            <div style="margin-bottom: 1rem;">
                                <h4 style="margin-bottom: 0.5rem;">Habilidades Comportamentais</h4>
                                <div class="result-skills">
                                    ${enriched.perfil_profissional.habilidades_comportamentais.map(s => `<span class="skill-tag" style="background: #FFF7ED; color: #C2410C;">${s}</span>`).join('')}
                                </div>
                            </div>` : ''}

                        <!-- Certifications -->
                        ${enriched.perfil_profissional?.certificacoes?.length ? `
                            <div style="margin-bottom: 1rem;">
                                <h4 style="margin-bottom: 0.5rem;">Certificações</h4>
                                <ul style="list-style-type: disc; padding-left: 1.5rem; font-size: 0.9rem; color: #374151;">
                                    ${enriched.perfil_profissional.certificacoes.map(c => `<li>${c}</li>`).join('')}
                                </ul>
                            </div>` : ''}

                        ${expHtml ? `<div style="margin-bottom: 1rem;"><h4 style="margin-bottom: 0.5rem;">Experiência Profissional</h4>${expHtml}</div>` : ''}
                        
                        ${eduHtml ? `<div style="margin-bottom: 1rem;"><h4 style="margin-bottom: 0.5rem;">Formação Acadêmica</h4>${eduHtml}</div>` : ''}
                        
                        <div style="font-size: 0.8rem; color: #9CA3AF; margin-top: 1rem;">
                            Arquivo: ${meta.filename || meta.source_file || 'N/A'} • ID: ${meta.candidate_id || 'N/A'}
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = html;
    }

    // --- Upload Logic (Multi-file) ---
    async function handleFiles(files) {
        const feedback = document.getElementById('uploadFeedback');
        feedback.innerHTML = ''; // Clear previous feedback

        // Create a list container for file statuses
        const statusList = document.createElement('div');
        statusList.className = 'upload-status-list';
        feedback.appendChild(statusList);

        // Convert FileList to Array to iterate easily
        const filesArray = Array.from(files);

        for (const file of filesArray) {
            // Create status item for this file
            const statusItem = document.createElement('div');
            statusItem.className = 'upload-status-item';

            // Initial HTML structure
            statusItem.innerHTML = `
                <div class="upload-header">
                    <span class="upload-filename">${file.name}</span>
                    <span class="status-text status-pending">Aguardando...</span>
                </div>
                <div class="upload-progress-track">
                    <div class="upload-progress-bar"></div>
                </div>
                <div class="upload-result-container"></div>
            `;

            statusList.appendChild(statusItem);

            // Process file sequentially
            await uploadSingleFile(file, statusItem);
        }
    }

    async function uploadSingleFile(file, statusElement) {
        const statusSpan = statusElement.querySelector('.status-text');
        const progressBar = statusElement.querySelector('.upload-progress-bar');
        const resultContainer = statusElement.querySelector('.upload-result-container');

        if (file.type !== 'application/pdf' &&
            file.type !== 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' &&
            file.type !== 'application/msword' &&
            !file.name.toLowerCase().endsWith('.pdf') &&
            !file.name.toLowerCase().endsWith('.docx') &&
            !file.name.toLowerCase().endsWith('.doc')) {

            statusSpan.className = 'status-text status-error';
            statusSpan.textContent = 'Erro: Apenas PDF ou Word (Doc/Docx)';
            progressBar.style.background = '#EF4444';
            progressBar.style.width = '100%';
            return;
        }

        statusSpan.className = 'status-text status-processing';
        statusSpan.textContent = 'Extraindo e processando...';

        // Fake progress animation
        progressBar.style.width = '30%';
        setTimeout(() => { if (progressBar.style.width !== '100%') progressBar.style.width = '60%'; }, 1000);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('metadata', JSON.stringify({
            upload_date: new Date().toISOString(),
            id_candidato: "manual_upload_" + Date.now() + "_" + Math.floor(Math.random() * 1000)
        }));

        try {
            const response = await fetch('/api/ingest', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (response.status === 401) {
                statusSpan.className = 'status-text status-error';
                statusSpan.textContent = 'Não autorizado';
                progressBar.style.background = '#EF4444';
                progressBar.style.width = '100%';
                return;
            }

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Falha no processamento');
            }

            const data = await response.json();

            // Success State
            statusSpan.className = 'status-text status-success';
            statusSpan.innerHTML = '✓ Concluído com Sucesso';
            progressBar.style.width = '100%';
            progressBar.style.background = '#10B981';

            // Render Success Card
            // Card removed as per user request
            resultContainer.innerHTML = '';


            // Clear the file input to allow re-uploading the same file if needed
            document.getElementById('fileInput').value = '';

        } catch (error) {
            console.error(error);
            statusSpan.className = 'status-text status-error';
            statusSpan.textContent = `Erro: ${error.message}`;
            progressBar.style.background = '#EF4444';
            progressBar.style.width = '100%';
        }
    }

    // Initialize with Search view
    handleNavigation('search');
});
