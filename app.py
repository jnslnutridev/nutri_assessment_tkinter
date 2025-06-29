import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime # Caso necessário importar também: timedelta
import json
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from PIL import Image as PILImage # Caso necessário importar também: ImageDraw, ImageFont
import io

class AvaliacaoNutricionalIdosos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Avaliação Nutricional - Idosos")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f2f5')
        
        # Cores da paleta moderna
        self.cores = {
            'primaria': '#2c3e50',
            'secundaria': '#3498db',
            'sucesso': '#27ae60',
            'alerta': '#f39c12',
            'perigo': '#e74c3c',
            'info': '#17a2b8',
            'fundo': '#f8f9fa',
            'card': '#ffffff',
            'texto': '#2c3e50',
            'texto_secundario': '#6c757d'
        }
        
        # Dados do paciente
        self.dados_paciente = {}
        self.dados_antropometricos = {}
        self.dados_clinicos = {}
        self.dados_alimentares = {}
        self.historico_consultas = []
        self.dados_intervencao = {}
        self.dados_evolucao = {}

        
        self.setup_interface()
        
    def setup_interface(self):
        # Estilo personalizado
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos personalizados
        self.style.configure('Header.TLabel', 
                           font=('Arial', 16, 'bold'),
                           background=self.cores['fundo'],
                           foreground=self.cores['primaria'])
        
        self.style.configure('Card.TFrame',
                           background=self.cores['card'],
                           relief='flat',
                           borderwidth=1)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.cores['fundo'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.cores['primaria'], height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)

        # Footer
        footer_frame = tk.Frame(main_frame, bg=self.cores['primaria'], height=40)
        footer_frame.pack(side=tk.BOTTOM, fill='x', pady=(0, 10))
        footer_frame.pack_propagate(False)

        
        title_label = tk.Label(header_frame, 
                              text="Sistema de Avaliação Nutricional - Idosos",
                              font=('Arial', 20, 'bold'),
                              bg=self.cores['primaria'],
                              fg='white')
        title_label.pack(expand=True)

        footer_label = tk.Label(footer_frame, 
                              text="2025 - jnslnutridev",
                              font=('Arial', 14, 'bold'),
                              bg=self.cores['primaria'],
                              fg='white')
        footer_label.pack(expand=True)

        # ───> Aqui, logo abaixo do título, adicionamos o botão:
        btn_carregar = ttk.Button(header_frame, 
                                  text="Carregar Avaliação", 
                                  command=self.carregar_dados)
        btn_carregar.place(relx=0.98, rely=0.5, anchor='e')  # ajusta posição no header
        
        # Notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Criar abas
        self.criar_aba_identificacao()
        self.criar_aba_anamnese()
        self.criar_aba_antropometria()
        self.criar_aba_clinica()
        self.criar_aba_alimentar()
        self.criar_aba_intervencao()
        self.criar_aba_evolucao()
        self.criar_aba_dashboard()
        self.criar_aba_relatorios()
        
        # Bind para atualizar dashboard quando trocar de aba
        self.notebook.bind('<<NotebookTabChanged>>', self.atualizar_dashboard)
        
    def criar_aba_identificacao(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Identificação')
        
        # Scroll
        canvas = tk.Canvas(frame, bg=self.cores['fundo'])
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cores['fundo'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Card de identificação
        card_frame = tk.Frame(scrollable_frame, bg=self.cores['card'], relief='solid', bd=1)
        card_frame.pack(fill='x', padx=20, pady=20)
        
        # Título do card
        title_frame = tk.Frame(card_frame, bg=self.cores['secundaria'], height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Dados Pessoais", 
                font=('Arial', 14, 'bold'),
                bg=self.cores['secundaria'], fg='white').pack(expand=True)
        
        # Campos do formulário
        form_frame = tk.Frame(card_frame, bg=self.cores['card'])
        form_frame.pack(fill='x', padx=20, pady=20)
        
        # Grid de campos
        campos = [
            ('Nome Completo:', 'nome'),
            ('Data de Nascimento:', 'data_nascimento'),
            ('Idade:', 'idade'),
            ('Sexo:', 'sexo'),
            ('Nº de Registro:', 'registro'),
            ('Telefone:', 'telefone'),
            ('Email:', 'email'),
            ('Endereço:', 'endereco'),
            ('Profissão:', 'profissao'),
            ('Contato de Emergência :', 'contato_emergencia'),
            ('Telefone de Emergência :', 'telefone_emergencia'),
            ('Estado Civil:', 'estado_civil'),
            ('Escolaridade:', 'escolaridade'),
            ('Data da Admissão:', 'data_admissao'),
        ]
        
        self.campos_identificacao = {}
        
        for i, (label, campo) in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(form_frame, text=label, 
                    font=('Arial', 10, 'bold'),
                    bg=self.cores['card']).grid(row=row, column=col, 
                                              sticky='w', padx=(0, 10), pady=5)
            
            if campo == 'sexo':
                self.campos_identificacao[campo] = ttk.Combobox(form_frame, 
                                                              values=['Masculino', 'Feminino'],
                                                              width=25)
            elif campo == 'estado_civil':
                self.campos_identificacao[campo] = ttk.Combobox(form_frame,
                                                              values=['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)'],
                                                              width=25)
            elif campo == 'escolaridade':
                self.campos_identificacao[campo] = ttk.Combobox(form_frame,
                                                              values=['Analfabeto', 'Fundamental Incompleto', 
                                                                     'Fundamental Completo', 'Médio Incompleto',
                                                                     'Médio Completo', 'Superior Incompleto',
                                                                     'Superior Completo', 'Pós-graduação'],
                                                              width=25)
            else:
                self.campos_identificacao[campo] = tk.Entry(form_frame, width=30)
            
            self.campos_identificacao[campo].grid(row=row, column=col+1, 
                                                sticky='w', padx=(0, 20), pady=5)
        
        # Botões
        btn_frame = tk.Frame(card_frame, bg=self.cores['card'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(btn_frame, text="Salvar Dados",
                 bg=self.cores['sucesso'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.salvar_identificacao).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="Limpar Campos",
                 bg=self.cores['alerta'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.limpar_identificacao).pack(side='left')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def criar_aba_anamnese(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Anamnese')
        
        # Scroll
        canvas = tk.Canvas(frame, bg=self.cores['fundo'])
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cores['fundo'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Card de anamnese
        card_frame = tk.Frame(scrollable_frame, bg=self.cores['card'], relief='solid', bd=1)
        card_frame.pack(fill='x', padx=20, pady=20)
        
        # Título do card
        title_frame = tk.Frame(card_frame, bg=self.cores['secundaria'], height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Anamnese", 
                font=('Arial', 14, 'bold'),
                bg=self.cores['secundaria'], fg='white').pack(expand=True)
        
        # Campos do formulário
        form_frame = tk.Frame(card_frame, bg=self.cores['card'])
        form_frame.pack(fill='x', padx=20, pady=20)
        
        # Grid de campos
        campos_anamnese = [
            ('Queixa Principal:', 'queixa_principal'),
            ('História Médica Pregressa:', 'historia_medica_pregressa'),
            ('Medicamentos em Uso:', 'medicamentos_uso'),
            ('Alergias:', 'alergias'),
            ('Histórico Familiar:', 'historico_familiar'),
            ('Histórico Social:', 'historico_social'),
            ('Hábitos Alimentares:', 'habitos_alimentares'),
            ('Intolerâncias Alimentares:', 'intolerancias'),
            ('Mudanças no Apetite:', 'mudancas_apetite'),
            ('Mudanças de Peso Recente:', 'mudancas_peso'),
            ('Sintomas Gastrointestinais:', 'sintomas_gastrointestinais'),
            ('Capacidades Funcionais:', 'capacidades_funcionais'),
            ('Atividade Física:', 'atividade_fisica'),
            ('Suplementos Utilizados:', 'suplementos_utilizados'),
            ('Objetivos Nutricionais:', 'objetivos_nutricionais')
        ]
        
        self.campos_anamnese = {}
        
        for i, (label, campo) in enumerate(campos_anamnese):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(form_frame, text=label, 
                    font=('Arial', 10, 'bold'),
                    bg=self.cores['card']).grid(row=row, column=col,
                                                sticky='w', padx=(0, 10), pady=5)
            if campo in ['historico_familiar', 'historico_pessoal', 'habitos_vida',
                            'alergias', 'intolerancias', 'suplementos_utilizados', 
                            'objetivos_nutricionais']:
                    self.campos_anamnese[campo] = tk.Text(form_frame, height=4, width=50)
                    self.campos_anamnese[campo].grid(row=row, column=col+1, 
                                                    sticky='w', padx=(0, 20), pady=5)
            else:
                self.campos_anamnese[campo] = tk.Entry(form_frame, width=30)
                self.campos_anamnese[campo].grid(row=row, column=col+1, 
                                                sticky='w', padx=(0, 20), pady=5)
        # Botões
        btn_frame = tk.Frame(card_frame, bg=self.cores['card'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        tk.Button(btn_frame, text="Salvar Anamnese",
                    bg=self.cores['sucesso'], fg='white',
                    font=('Arial', 10, 'bold'),
                    command=self.salvar_anamnese).pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="Limpar Campos",
                    bg=self.cores['alerta'], fg='white',
                    font=('Arial', 10, 'bold'),
                    command=self.limpar_anamnese).pack(side='left')
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        

        
    def criar_aba_antropometria(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Antropometria')
        
        # Scroll
        canvas = tk.Canvas(frame, bg=self.cores['fundo'])
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cores['fundo'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Card de medidas antropométricas
        card_frame = tk.Frame(scrollable_frame, bg=self.cores['card'], relief='solid', bd=1)
        card_frame.pack(fill='x', padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(card_frame, bg=self.cores['secundaria'], height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Avaliação Antropométrica", 
                font=('Arial', 14, 'bold'),
                bg=self.cores['secundaria'], fg='white').pack(expand=True)
        
        # Campos antropométricos
        form_frame = tk.Frame(card_frame, bg=self.cores['card'])
        form_frame.pack(fill='x', padx=20, pady=20)
        
        campos_antropo = [
            ('Peso Atual (kg):', 'peso_atual'),
            ('Altura (cm):', 'altura'),
            ('Peso Habitual (kg):', 'peso_habitual'),
            ('Peso Estimado (kg):', 'peso_estimado'),
            ('Peso Ideal (kg):', 'peso_ideal'),
            ('Altura Estimada (cm):', 'altura_estimada'),
            ('Altura do Joelho (cm):', 'altura_joelho'),
            ('Circunferência do Braço (cm):', 'circ_braco'),
            ('Circunferência Muscular do Braço (cm):', 'circ_musc_braco'),
            ('Circunferência da Panturrilha (cm):', 'circ_panturrilha'),
            ('Circunferência da Cintura (cm):', 'circ_cintura'),
            ('Circunferência do Quadril (cm):', 'circ_quadril'),
            ('Circunferência Abdominal (cm):', 'circ_abdominal'),
            ('Dobra Cutânea Tricipital (mm):', 'dobra_triceps'),
            ('Dobra Cutânea Bicipital (mm):', 'dobra_biceps'),
            ('Dobra Cutânea Subescapular (mm):', 'dobra_subescapular'),
            ('Dobra Cutânea Suprailiaca (mm):', 'dobra_suprailiaca'),
            ('Dobra Cutânea Abdominal (mm):', 'dobra_abdominal'),
            ('Dobra Cutânea Peitoral (mm):', 'dobra_peitoral'),
            ('Dobra Cutânea Axilar (mm):', 'dobra_axilar'),
            ('Percentual de Gordura (%):', 'percentual_gordura'),
            ('Data da Medição:', 'data_medicao')
        ]
        
        self.campos_antropometria = {}
        
        for i, (label, campo) in enumerate(campos_antropo):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(form_frame, text=label, 
                    font=('Arial', 10, 'bold'),
                    bg=self.cores['card']).grid(row=row, column=col, 
                                              sticky='w', padx=(0, 10), pady=5)
            
            self.campos_antropometria[campo] = tk.Entry(form_frame, width=15)
            self.campos_antropometria[campo].grid(row=row, column=col+1, 
                                                sticky='w', padx=(0, 20), pady=5)
        
        # Frame para resultados calculados
        result_frame = tk.Frame(card_frame, bg=self.cores['info'], relief='solid', bd=1)
        result_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(result_frame, text="Resultados Calculados", 
                font=('Arial', 12, 'bold'),
                bg=self.cores['info'], fg='white').pack(pady=5)
        
        self.labels_resultados = {}
        resultados = ['IMC', 'Classificação IMC', 'RCQ', 'Classificação RCQ', 
                     'Perda de Peso (%)', 'CMB (cm)', 'AMB (cm²)']
        
        result_grid = tk.Frame(result_frame, bg=self.cores['info'])
        result_grid.pack(padx=10, pady=10)
        
        for i, resultado in enumerate(resultados):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(result_grid, text=f"{resultado}:", 
                    font=('Arial', 9, 'bold'),
                    bg=self.cores['info'], fg='white').grid(row=row, column=col, 
                                                           sticky='w', padx=(0, 10), pady=2)
            
            self.labels_resultados[resultado] = tk.Label(result_grid, text="--", 
                                                       font=('Arial', 9),
                                                       bg=self.cores['info'], fg='white')
            self.labels_resultados[resultado].grid(row=row, column=col+1, 
                                                 sticky='w', padx=(0, 20), pady=2)
        
        # Botões
        btn_frame = tk.Frame(card_frame, bg=self.cores['card'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(btn_frame, text="Calcular",
                 bg=self.cores['secundaria'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.calcular_antropometria).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="Salvar Dados",
                 bg=self.cores['sucesso'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.salvar_antropometria).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="Limpar Campos",
                 bg=self.cores['alerta'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.limpar_antropometria).pack(side='left')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def criar_aba_clinica(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Avaliação Clínica')
        
        # Scroll
        canvas = tk.Canvas(frame, bg=self.cores['fundo'])
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cores['fundo'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Card de histórico clínico
        card_frame = tk.Frame(scrollable_frame, bg=self.cores['card'], relief='solid', bd=1)
        card_frame.pack(fill='x', padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(card_frame, bg=self.cores['secundaria'], height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Avaliação Clínica", 
                font=('Arial', 14, 'bold'),
                bg=self.cores['secundaria'], fg='white').pack(expand=True)
        
        # Seção de doenças
        doencas_frame = tk.LabelFrame(card_frame, text="Doenças e Condições", 
                                     font=('Arial', 11, 'bold'),
                                     bg=self.cores['card'])
        doencas_frame.pack(fill='x', padx=20, pady=10)
        
        # Checkboxes para doenças comuns em idosos
        self.doencas_vars = {}
        doencas_comuns = [
            'Hipertensão Arterial', 'Diabetes Mellitus', 'Dislipidemia',
            'Osteoporose', 'Artrite/Artrose', 'Doença Cardíaca',
            'Doença Renal', 'Doença Hepática', 'Câncer',
            'Depressão', 'Demência', 'Parkinson',
            'DPOC', 'Hipotireoidismo', 'Anemia'
        ]
        
        doencas_grid = tk.Frame(doencas_frame, bg=self.cores['card'])
        doencas_grid.pack(fill='x', padx=10, pady=10)
        
        for i, doenca in enumerate(doencas_comuns):
            row = i // 3
            col = i % 3
            
            self.doencas_vars[doenca] = tk.BooleanVar()
            tk.Checkbutton(doencas_grid, text=doenca,
                          variable=self.doencas_vars[doenca],
                          bg=self.cores['card'],
                          font=('Arial', 9)).grid(row=row, column=col, 
                                                 sticky='w', padx=10, pady=2)
        
        # Medicamentos
        med_frame = tk.LabelFrame(card_frame, text="Medicamentos em Uso", 
                                 font=('Arial', 11, 'bold'),
                                 bg=self.cores['card'])
        med_frame.pack(fill='x', padx=20, pady=10)
        
        self.medicamentos_text = tk.Text(med_frame, height=4, width=80)
        self.medicamentos_text.pack(padx=10, pady=10)
        
        # Exames laboratoriais
        exames_frame = tk.LabelFrame(card_frame, text="Exames Laboratoriais", 
                                    font=('Arial', 11, 'bold'),
                                    bg=self.cores['card'])
        exames_frame.pack(fill='x', padx=20, pady=10)
        
        exames_grid = tk.Frame(exames_frame, bg=self.cores['card'])
        exames_grid.pack(fill='x', padx=10, pady=10)
        
        exames_campos = [
            ('Glicemia (mg/dL):', 'glicemia'),
            ('Hemoglobina (g/dL):', 'hemoglobina'),
            ('Colesterol Total (mg/dL):', 'colesterol_total'),
            ('HDL (mg/dL):', 'hdl'),
            ('LDL (mg/dL):', 'ldl'),
            ('Triglicerídeos (mg/dL):', 'triglicerideos'),
            ('Ureia (mg/dL):', 'ureia'),
            ('Creatinina (mg/dL):', 'creatinina'),
            ('Albumina (g/dL):', 'albumina'),
            ('Proteínas Totais (g/dL):', 'proteinas_totais'),
            ('Pré-albumina (mg/dL):', 'pre_albumina'),
            ('Ferro (µg/dL):', 'ferro'),
            ('Transferrina (mg/dL):', 'transferrina'),
            ('Ferritina (ng/mL):', 'ferritina'),
            ('Vitamina B12 (pg/mL):', 'vitamin_b12'),
            ('Folato (ng/mL):', 'folato'),
        ]
        
        self.campos_exames = {}
        
        for i, (label, campo) in enumerate(exames_campos):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(exames_grid, text=label, 
                    font=('Arial', 9, 'bold'),
                    bg=self.cores['card']).grid(row=row, column=col, 
                                              sticky='w', padx=(0, 10), pady=5)
            
            self.campos_exames[campo] = tk.Entry(exames_grid, width=15)
            self.campos_exames[campo].grid(row=row, column=col+1, 
                                         sticky='w', padx=(0, 20), pady=5)
        
        # Botões
        btn_frame = tk.Frame(card_frame, bg=self.cores['card'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(btn_frame, text="Salvar Avaliação",
                 bg=self.cores['sucesso'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.salvar_clinica).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="Limpar Campos",
                 bg=self.cores['alerta'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.limpar_clinica).pack(side='left')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def criar_aba_alimentar(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Avaliação Alimentar')
        
        # Scroll
        canvas = tk.Canvas(frame, bg=self.cores['fundo'])
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cores['fundo'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Card de avaliação alimentar
        card_frame = tk.Frame(scrollable_frame, bg=self.cores['card'], relief='solid', bd=1)
        card_frame.pack(fill='x', padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(card_frame, bg=self.cores['secundaria'], height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Avaliação Alimentar", 
                font=('Arial', 14, 'bold'),
                bg=self.cores['secundaria'], fg='white').pack(expand=True)
        
        # Recordatório 24h
        r24h_frame = tk.LabelFrame(card_frame, text="Recordatório Alimentar 24h", 
                                  font=('Arial', 11, 'bold'),
                                  bg=self.cores['card'])
        r24h_frame.pack(fill='x', padx=20, pady=10)
        
        # Refeições
        self.refeicoes = {}
        refeicoes_nomes = ['Café da Manhã', 'Lanche da Manhã', 'Almoço', 
                          'Lanche da Tarde', 'Jantar', 'Ceia']
        
        for refeicao in refeicoes_nomes:
            ref_frame = tk.LabelFrame(r24h_frame, text=refeicao, 
                                     font=('Arial', 10, 'bold'),
                                     bg=self.cores['card'])
            ref_frame.pack(fill='x', padx=10, pady=5)
            
            self.refeicoes[refeicao] = tk.Text(ref_frame, height=3, width=80)
            self.refeicoes[refeicao].pack(padx=5, pady=5)
        
        # Frequência alimentar
        freq_frame = tk.LabelFrame(card_frame, text="Frequência Alimentar Semanal", 
                                  font=('Arial', 11, 'bold'),
                                  bg=self.cores['card'])
        freq_frame.pack(fill='x', padx=20, pady=10)
        
        freq_grid = tk.Frame(freq_frame, bg=self.cores['card'])
        freq_grid.pack(fill='x', padx=10, pady=10)
        
        grupos_alimentos = [
            'Cereais/Pães', 'Frutas', 'Vegetais/Legumes', 'Carnes/Ovos',
            'Leite/Derivados', 'Leguminosas', 'Óleos/Gorduras', 'Doces',
            'Refrigerantes', 'Bebidas Alcoólicas'
        ]
        
        self.frequencia_vars = {}
        opcoes_freq = ['Nunca', '1-2x/sem', '3-4x/sem', '5-6x/sem', 'Diário', '2-3x/dia']
        
        # Cabeçalho
        tk.Label(freq_grid, text="Grupo Alimentar", 
                font=('Arial', 10, 'bold'),
                bg=self.cores['card']).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(freq_grid, text="Frequência", 
                font=('Arial', 10, 'bold'),
                bg=self.cores['card']).grid(row=0, column=1, padx=10, pady=5)
        
        for i, grupo in enumerate(grupos_alimentos):
            tk.Label(freq_grid, text=grupo, 
                    font=('Arial', 9),
                    bg=self.cores['card']).grid(row=i+1, column=0, 
                                              sticky='w', padx=10, pady=2)
            
            self.frequencia_vars[grupo] = ttk.Combobox(freq_grid, 
                                                      values=opcoes_freq,
                                                      width=15)
            self.frequencia_vars[grupo].grid(row=i+1, column=1, 
                                           padx=10, pady=2)
        
        # Hábitos alimentares
        habitos_frame = tk.LabelFrame(card_frame, text="Hábitos e Preferências", 
                                     font=('Arial', 11, 'bold'),
                                     bg=self.cores['card'])
        habitos_frame.pack(fill='x', padx=20, pady=10)
        
        habitos_grid = tk.Frame(habitos_frame, bg=self.cores['card'])
        habitos_grid.pack(fill='x', padx=10, pady=10)
        
        # Campos de hábitos
        habitos_campos = [
            ('Apetite:', 'apetite', ['Bom', 'Regular', 'Ruim']),
            ('Mastigação:', 'mastigacao', ['Normal', 'Dificuldade', 'Prótese']),
            ('Deglutição:', 'degluticao', ['Normal', 'Dificuldade']),
            ('Intestino:', 'intestino', ['Normal', 'Constipação', 'Diarreia']),
            ('Ingestão de Água (L/dia):', 'agua', None),
            ('Suplementação:', 'suplementacao', ['Não', 'Vitaminas', 'Proteínas', 'Outros'])
        ]
        
        self.campos_habitos = {}
        
        for i, (label, campo, opcoes) in enumerate(habitos_campos):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(habitos_grid, text=label, 
                    font=('Arial', 9, 'bold'),
                    bg=self.cores['card']).grid(row=row, column=col, 
                                              sticky='w', padx=(0, 10), pady=5)
            
            if opcoes:
                self.campos_habitos[campo] = ttk.Combobox(habitos_grid, 
                                                         values=opcoes,
                                                         width=20)
            else:
                self.campos_habitos[campo] = tk.Entry(habitos_grid, width=25)
            
            self.campos_habitos[campo].grid(row=row, column=col+1, 
                                          sticky='w', padx=(0, 20), pady=5)
        
        # Botões
        btn_frame = tk.Frame(card_frame, bg=self.cores['card'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(btn_frame, text="Salvar Avaliação",
                 bg=self.cores['sucesso'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.salvar_alimentar).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="Limpar Campos",
                 bg=self.cores['alerta'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.limpar_alimentar).pack(side='left')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def criar_aba_intervencao(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Intervenção Nutricional')
        
        # Scroll
        canvas = tk.Canvas(frame, bg=self.cores['fundo'])
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cores['fundo'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Card de intervenção nutricional
        card_frame = tk.Frame(scrollable_frame, bg=self.cores['card'], relief='solid', bd=1)
        card_frame.pack(fill='x', padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(card_frame, bg=self.cores['secundaria'], height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Plano de Intervenção Nutricional", 
                font=('Arial', 14, 'bold'),
                bg=self.cores['secundaria'], fg='white').pack(expand=True)
        
        # Objetivos nutricionais
        objetivos_frame = tk.LabelFrame(card_frame, text="Objetivos Nutricionais", 
                                       font=('Arial', 11, 'bold'),
                                       bg=self.cores['card'])
        objetivos_frame.pack(fill='x', padx=20, pady=10)
        
        self.objetivos_text = tk.Text(objetivos_frame, height=4, width=80)
        self.objetivos_text.pack(padx=10, pady=10)
        
        # Prescrição dietética
        dieta_frame = tk.LabelFrame(card_frame, text="Prescrição Dietética", 
                                   font=('Arial', 11, 'bold'),
                                   bg=self.cores['card'])
        dieta_frame.pack(fill='x', padx=20, pady=10)
        
        self.dieta_text = tk.Text(dieta_frame, height=6, width=80)
        self.dieta_text.pack(padx=10, pady=10)
        
        # Suplementação
        suplemento_frame = tk.LabelFrame(card_frame, text="Suplementação Nutricional", 
                                       font=('Arial', 11, 'bold'),
                                        bg=self.cores['card'])
        suplemento_frame.pack(fill='x', padx=20, pady=10)
        self.suplemento_text = tk.Text(suplemento_frame, height=4, width=80)
        self.suplemento_text.pack(padx=10, pady=10)
        # Recomendações gerais
        recomendacoes_frame = tk.LabelFrame(card_frame, text="Recomendações Gerais",
                                             font=('Arial', 11, 'bold'),
                                                bg=self.cores['card'])
        recomendacoes_frame.pack(fill='x', padx=20, pady=10)
        self.recomendacoes_text = tk.Text(recomendacoes_frame, height=4, width=80)
        self.recomendacoes_text.pack(padx=10, pady=10)
        # Botões
        btn_frame = tk.Frame(card_frame, bg=self.cores['card'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        tk.Button(btn_frame, text="Salvar Intervenção",
                    bg=self.cores['sucesso'], fg='white',
                    font=('Arial', 10, 'bold'),
                    command=self.salvar_intervencao).pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="Limpar Campos",
                    bg=self.cores['alerta'], fg='white',
                    font=('Arial', 10, 'bold'),
                    command=self.limpar_intervencao).pack(side='left')
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def criar_aba_evolucao(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Evolução Nutricional')

        # Scroll interno (igual às outras abas)
        canvas = tk.Canvas(frame, bg=self.cores['fundo'])
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.cores['fundo'])
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Card
        card = tk.Frame(scrollable, bg=self.cores['card'], relief='solid', bd=1)
        card.pack(fill='x', padx=20, pady=20)

        # Título
        titulo = tk.Frame(card, bg=self.cores['secundaria'], height=40)
        titulo.pack(fill='x'); titulo.pack_propagate(False)
        tk.Label(titulo, text="Evolução Nutricional",
                font=('Arial', 14, 'bold'),
                bg=self.cores['secundaria'], fg='white').pack(expand=True)

        # Campos
        campos = [
            ('Peso (kg):', 'peso_evo'),
            ('IMC (kg/m²):', 'imc_evo'),
            ('Estado Nutricional:', 'estado_nutri_evo'),
            ('Adesão à Dieta:', 'adesao_dieta_evo'),
            ('Apetite:', 'apetite_evo'),
            ('Evolução Clínica:', 'evolucao_clinica_evo'),
            ('Circunferência do Braço (cm):', 'circ_braco_evo'),
            ('Circunferência Muscular do Braço (cm):', 'circ_musc_braco_evo'),
            ('Circunferência da Panturrilha (cm):', 'circ_panturrilha_evo'),
            ('Circunferência da Cintura (cm):', 'circ_cintura_evo'),
            ('Circunferência do Quadril (cm):', 'circ_quadril_evo'),
            ('Circunferência Abdominal (cm):', 'circ_abdominal_evo'),
            ('Dobra Cutânea Tricipital (mm):', 'dobra_triceps_evo'),
            ('Dobra Cutânea Bicipital (mm):', 'dobra_biceps_evo'),
            ('Dobra Cutânea Subescapular (mm):', 'dobra_subescapular_evo'),
            ('Dobra Cutânea Suprailiaca (mm):', 'dobra_suprailiaca_evo'),
            ('Dobra Cutânea Abdominal (mm):', 'dobra_abdominal_evo'),
            ('Dobra Cutânea Peitoral (mm):', 'dobra_peitoral_evo'),
            ('Dobra Cutânea Axilar (mm):', 'dobra_axilar_evo'),
            ('Avaliador (nome):', 'nome_avaliador_evo')
        ]

        self.campos_evolucao = {}
        form = tk.Frame(card, bg=self.cores['card'])
        form.pack(fill='x', padx=20, pady=20)

        for i, (rotulo, chave) in enumerate(campos):
            row, col = divmod(i, 2)
            tk.Label(form, text=rotulo, font=('Arial', 10, 'bold'),
                    bg=self.cores['card']).grid(row=row, column=col*2,
                                                sticky='w', padx=5, pady=3)
            entry = tk.Entry(form, width=25)
            entry.grid(row=row, column=col*2+1, sticky='w', padx=5, pady=3)
            self.campos_evolucao[chave] = entry

        # Botões Salvar / Limpar
        btnf = tk.Frame(card, bg=self.cores['card'])
        btnf.pack(fill='x', padx=20, pady=(0,20))
        tk.Button(btnf, text="Salvar Evolução",
                bg=self.cores['sucesso'], fg='white',
                font=('Arial', 10, 'bold'),
                command=self.salvar_evolucao).pack(side='left', padx=10)
        tk.Button(btnf, text="Limpar Campos",
                bg=self.cores['alerta'], fg='white',
                font=('Arial', 10, 'bold'),
                command=self.limpar_evolucao).pack(side='left')

        # — novos botões —
        tk.Button(btnf, text="Nova Evolução",
                bg=self.cores['info'], fg='white',
                font=('Arial', 10, 'bold'),
                command=self.nova_evolucao).pack(side='left', padx=5)
        tk.Button(btnf, text="Carregar Evolução",
                bg=self.cores['primaria'], fg='white',
                font=('Arial', 10, 'bold'),
                command=self.carregar_evolucao).pack(side='left', padx=5)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    
    def criar_aba_dashboard(self):
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text='Dashboard')
        
        # Frame principal do dashboard
        main_dash = tk.Frame(self.dashboard_frame, bg=self.cores['fundo'])
        main_dash.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title_frame = tk.Frame(main_dash, bg=self.cores['primaria'], height=50)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Dashboard Nutricional", 
                font=('Arial', 16, 'bold'),
                bg=self.cores['primaria'], fg='white').pack(expand=True)
        
        # Frame para cards de resumo
        cards_frame = tk.Frame(main_dash, bg=self.cores['fundo'])
        cards_frame.pack(fill='x', pady=(0, 20))
        
        # Cards de estatísticas
        self.criar_cards_estatisticas(cards_frame)
        
        # Frame para gráficos
        graficos_frame = tk.Frame(main_dash, bg=self.cores['fundo'])
        graficos_frame.pack(fill='both', expand=True)
        
        # Criar gráficos
        self.criar_graficos_dashboard(graficos_frame)
        
    def criar_cards_estatisticas(self, parent):
        # IMC Card
        imc_card = tk.Frame(parent, bg=self.cores['card'], relief='solid', bd=1)
        imc_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(imc_card, text="IMC", 
                font=('Arial', 12, 'bold'),
                bg=self.cores['secundaria'], fg='white').pack(fill='x', pady=(0, 5))
        
        self.imc_valor = tk.Label(imc_card, text="--", 
                                 font=('Arial', 20, 'bold'),
                                 bg=self.cores['card'], fg=self.cores['primaria'])
        self.imc_valor.pack(pady=10)
        
        self.imc_classificacao = tk.Label(imc_card, text="--", 
                                         font=('Arial', 10),
                                         bg=self.cores['card'], fg=self.cores['texto_secundario'])
        self.imc_classificacao.pack(pady=(0, 10))
        
        # Status Nutricional Card
        status_card = tk.Frame(parent, bg=self.cores['card'], relief='solid', bd=1)
        status_card.pack(side='left', fill='both', expand=True, padx=10)
        
        tk.Label(status_card, text="Status Nutricional", 
                font=('Arial', 12, 'bold'),
                bg=self.cores['info'], fg='white').pack(fill='x', pady=(0, 5))
        
        self.status_nutricional = tk.Label(status_card, text="--", 
                                          font=('Arial', 14, 'bold'),
                                          bg=self.cores['card'], fg=self.cores['primaria'])
        self.status_nutricional.pack(pady=20)
        
        # Risco Card
        risco_card = tk.Frame(parent, bg=self.cores['card'], relief='solid', bd=1)
        risco_card.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(risco_card, text="Risco Nutricional", 
                font=('Arial', 12, 'bold'),
                bg=self.cores['alerta'], fg='white').pack(fill='x', pady=(0, 5))
        
        self.risco_nutricional = tk.Label(risco_card, text="--", 
                                         font=('Arial', 14, 'bold'),
                                         bg=self.cores['card'], fg=self.cores['primaria'])
        self.risco_nutricional.pack(pady=20)
        
    def criar_graficos_dashboard(self, parent):
        # Frame para gráficos
        graph_frame = tk.Frame(parent, bg=self.cores['fundo'])
        graph_frame.pack(fill='both', expand=True)
        
        # Configurar matplotlib
        plt.style.use('seaborn-v0_8')
        
        # Gráfico de evolução do peso
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.patch.set_facecolor(self.cores['fundo'])
        
        # Canvas para matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Atualizar gráficos iniciais
        self.atualizar_graficos_dashboard()
        
    def atualizar_graficos_dashboard(self):
        # Limpar gráficos
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        
        # Gráfico 1: Evolução do Peso
        if self.historico_consultas:
            datas = [consulta.get('data', datetime.now()) for consulta in self.historico_consultas]
            pesos = [consulta.get('peso', 0) for consulta in self.historico_consultas]
            
            self.ax1.plot(datas, pesos, marker='o', color=self.cores['secundaria'], linewidth=2)
            self.ax1.set_title('Evolução do Peso', fontweight='bold')
            self.ax1.set_ylabel('Peso (kg)')
            self.ax1.grid(True, alpha=0.3)
        else:
            self.ax1.text(0.5, 0.5, 'Sem dados históricos', 
                         ha='center', va='center', transform=self.ax1.transAxes)
            self.ax1.set_title('Evolução do Peso', fontweight='bold')
        
        # Gráfico 2: Distribuição de Macronutrientes
        macros = ['Carboidratos', 'Proteínas', 'Lipídios']
        valores = [50, 20, 30]  # Valores exemplo
        cores_macro = [self.cores['sucesso'], self.cores['info'], self.cores['alerta']]
        
        self.ax2.pie(valores, labels=macros, colors=cores_macro, autopct='%1.1f%%', startangle=90)
        self.ax2.set_title('Distribuição de Macronutrientes', fontweight='bold')
        
        # Gráfico 3: Frequência Alimentar
        if hasattr(self, 'frequencia_vars') and any(var.get() for var in self.frequencia_vars.values()):
            grupos = list(self.frequencia_vars.keys())[:5]  # Primeiros 5 grupos
            frequencias = [3, 5, 4, 2, 6]  # Valores exemplo convertidos para números
            
            bars = self.ax3.bar(grupos, frequencias, color=self.cores['secundaria'], alpha=0.7)
            self.ax3.set_title('Frequência de Consumo por Grupo', fontweight='bold')
            self.ax3.set_ylabel('Frequência Semanal')
            self.ax3.tick_params(axis='x', rotation=45)
            
            # Adicionar valores nas barras
            for bar, freq in zip(bars, frequencias):
                height = bar.get_height()
                self.ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                             f'{freq}x', ha='center', va='bottom')
        else:
            self.ax3.text(0.5, 0.5, 'Preencha a avaliação\nalimentar', 
                         ha='center', va='center', transform=self.ax3.transAxes)
            self.ax3.set_title('Frequência de Consumo por Grupo', fontweight='bold')
        
        # Gráfico 4: Indicadores Antropométricos
        if self.dados_antropometricos:
            indicadores = ['IMC', 'RCQ', 'Perda Peso %']
            valores_atuais = [
                self.dados_antropometricos.get('imc', 0),
                self.dados_antropometricos.get('rcq', 0),
                self.dados_antropometricos.get('perda_peso_perc', 0)
            ]
            valores_ideais = [25, 0.85, 0]  # Valores de referência
            
            x = np.arange(len(indicadores))
            width = 0.35
            
            bars1 = self.ax4.bar(x - width/2, valores_atuais, width, 
                               label='Atual', color=self.cores['secundaria'], alpha=0.7)
            bars2 = self.ax4.bar(x + width/2, valores_ideais, width, 
                               label='Referência', color=self.cores['sucesso'], alpha=0.7)
            
            self.ax4.set_title('Indicadores Antropométricos', fontweight='bold')
            self.ax4.set_ylabel('Valores')
            self.ax4.set_xticks(x)
            self.ax4.set_xticklabels(indicadores)
            self.ax4.legend()
            
            # Adicionar valores nas barras
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        self.ax4.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                                     f'{height:.1f}', ha='center', va='bottom')
        else:
            self.ax4.text(0.5, 0.5, 'Preencha a avaliação\nantropométrica', 
                         ha='center', va='center', transform=self.ax4.transAxes)
            self.ax4.set_title('Indicadores Antropométricos', fontweight='bold')
        
        # Ajustar layout
        self.fig.tight_layout()
        self.canvas.draw()
        
    def criar_aba_relatorios(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Relatórios')
        
        # Frame principal
        main_frame = tk.Frame(frame, bg=self.cores['fundo'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(main_frame, bg=self.cores['primaria'], height=50)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Relatórios e Impressão", 
                font=('Arial', 16, 'bold'),
                bg=self.cores['primaria'], fg='white').pack(expand=True)
        
        # Cards de relatórios
        reports_frame = tk.Frame(main_frame, bg=self.cores['fundo'])
        reports_frame.pack(fill='both', expand=True)
        
        # Relatório Completo
        card1 = tk.Frame(reports_frame, bg=self.cores['card'], relief='solid', bd=1)
        card1.pack(fill='x', pady=(0, 20))
        
        tk.Label(card1, text="Relatório Completo", 
                font=('Arial', 14, 'bold'),
                bg=self.cores['secundaria'], fg='white').pack(fill='x', pady=(0, 10))
        
        tk.Label(card1, text="Inclui todas as avaliações: identificação, antropometria, clínica e alimentar", 
                font=('Arial', 10),
                bg=self.cores['card']).pack(pady=(0, 10))
        
        btn_frame1 = tk.Frame(card1, bg=self.cores['card'])
        btn_frame1.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(btn_frame1, text="Gerar PDF Completo",
                 bg=self.cores['sucesso'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.gerar_relatorio_completo).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame1, text="Visualizar",
                 bg=self.cores['info'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.visualizar_relatorio).pack(side='left')
        
        # Relatórios Específicos
        card2 = tk.Frame(reports_frame, bg=self.cores['card'], relief='solid', bd=1)
        card2.pack(fill='x', pady=(0, 20))
        
        tk.Label(card2, text="Relatórios Específicos", 
                font=('Arial', 14, 'bold'),
                bg=self.cores['info'], fg='white').pack(fill='x', pady=(0, 10))
        
        btn_frame2 = tk.Frame(card2, bg=self.cores['card'])
        btn_frame2.pack(fill='x', padx=20, pady=20)
        
        tk.Button(btn_frame2, text="Relatório Antropométrico",
                 bg=self.cores['secundaria'], fg='white',
                 font=('Arial', 9, 'bold'),
                 command=lambda: self.gerar_relatorio_especifico('antropometrico')).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame2, text="Relatório Clínico",
                 bg=self.cores['secundaria'], fg='white',
                 font=('Arial', 9, 'bold'),
                 command=lambda: self.gerar_relatorio_especifico('clinico')).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame2, text="Relatório Alimentar",
                 bg=self.cores['secundaria'], fg='white',
                 font=('Arial', 9, 'bold'),
                 command=lambda: self.gerar_relatorio_especifico('alimentar')).pack(side='left')
        
        # Dashboard em PDF
        card3 = tk.Frame(reports_frame, bg=self.cores['card'], relief='solid', bd=1)
        card3.pack(fill='x')
        
        tk.Label(card3, text="Dashboard Gráfico", 
                font=('Arial', 14, 'bold'),
                bg=self.cores['alerta'], fg='white').pack(fill='x', pady=(0, 10))
        
        tk.Label(card3, text="Exporta o dashboard com gráficos e indicadores visuais", 
                font=('Arial', 10),
                bg=self.cores['card']).pack(pady=(0, 10))
        
        btn_frame3 = tk.Frame(card3, bg=self.cores['card'])
        btn_frame3.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(btn_frame3, text="Exportar Dashboard",
                 bg=self.cores['alerta'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.exportar_dashboard).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame3, text="Salvar Gráficos",
                 bg=self.cores['perigo'], fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.salvar_graficos).pack(side='left')
    
    # Métodos de cálculo e validação
    def calcular_antropometria(self):
        try:
            # Obter valores dos campos
            peso = float(self.campos_antropometria['peso_atual'].get() or 0)
            altura = float(self.campos_antropometria['altura'].get() or 0) / 100  # Converter para metros
            peso_habitual = float(self.campos_antropometria['peso_habitual'].get() or peso)
            circ_cintura = float(self.campos_antropometria['circ_cintura'].get() or 0)
            circ_quadril = float(self.campos_antropometria['circ_quadril'].get() or 0)
            circ_braco = float(self.campos_antropometria['circ_braco'].get() or 0)
            dobra_triceps = float(self.campos_antropometria['dobra_triceps'].get() or 0)
            
            # Calcular IMC
            if altura > 0:
                imc = peso / (altura ** 2)
                self.labels_resultados['IMC'].config(text=f"{imc:.1f}")
                
                # Classificar IMC para idosos (pontos de corte específicos)
                if imc < 22:
                    classificacao_imc = "Baixo peso"
                elif imc <= 27:
                    classificacao_imc = "Adequado"
                else:
                    classificacao_imc = "Sobrepeso"
                
                self.labels_resultados['Classificação IMC'].config(text=classificacao_imc)
                
                # Salvar no dados
                self.dados_antropometricos['imc'] = imc
                self.dados_antropometricos['classificacao_imc'] = classificacao_imc
            
            # Calcular RCQ (Relação Cintura-Quadril)
            if circ_cintura > 0 and circ_quadril > 0:
                rcq = circ_cintura / circ_quadril
                self.labels_resultados['RCQ'].config(text=f"{rcq:.2f}")
                
                # Classificar RCQ
                sexo = self.campos_identificacao.get('sexo', ttk.Combobox()).get()
                if sexo == "Masculino":
                    classificacao_rcq = "Baixo risco" if rcq <= 0.95 else "Alto risco"
                else:
                    classificacao_rcq = "Baixo risco" if rcq <= 0.80 else "Alto risco"
                
                self.labels_resultados['Classificação RCQ'].config(text=classificacao_rcq)
                self.dados_antropometricos['rcq'] = rcq
                self.dados_antropometricos['classificacao_rcq'] = classificacao_rcq
            
            # Calcular perda de peso
            if peso_habitual > 0:
                perda_peso = ((peso_habitual - peso) / peso_habitual) * 100
                self.labels_resultados['Perda de Peso (%)'].config(text=f"{perda_peso:.1f}%")
                self.dados_antropometricos['perda_peso_perc'] = perda_peso
            
            # Calcular CMB (Circunferência Muscular do Braço)
            if circ_braco > 0 and dobra_triceps > 0:
                cmb = circ_braco - (3.1416 * dobra_triceps / 10)
                self.labels_resultados['CMB (cm)'].config(text=f"{cmb:.1f}")
                self.dados_antropometricos['cmb'] = cmb
                
                # Calcular AMB (Área Muscular do Braço)
                amb = (cmb ** 2) / (4 * 3.1416)
                self.labels_resultados['AMB (cm²)'].config(text=f"{amb:.1f}")
                self.dados_antropometricos['amb'] = amb
            
            messagebox.showinfo("Sucesso", "Cálculos realizados com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    # Métodos de salvamento
    def salvar_identificacao(self):
        try:
            for campo, widget in self.campos_identificacao.items():
                self.dados_paciente[campo] = widget.get()
            
            self.dados_paciente['data_cadastro'] = datetime.now().strftime("%d/%m/%Y %H:%M")
            messagebox.showinfo("Sucesso", "Dados de identificação salvos!")
            self.salvar_arquivo()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def salvar_anamnese(self):
        try:
            self.dados_paciente['anamnese'] = {}
            for campo, widget in self.campos_anamnese.items():
                if isinstance(widget, tk.Text):
                    # Texto: pega do início ao fim
                    valor = widget.get("1.0", tk.END).strip()
                else:
                    # Entry/Combobox: pega o valor normal
                    valor = widget.get().strip()
                if valor:
                    self.dados_paciente['anamnese'][campo] = valor

            messagebox.showinfo("Sucesso", "Dados de anamnese salvos!")
            self.salvar_arquivo()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar anamnese: {e}")
    
    def salvar_antropometria(self):
        try:
            for campo, widget in self.campos_antropometria.items():
                valor = widget.get()
                if valor:
                    self.dados_antropometricos[campo] = float(valor)
            
            registro = {
                'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'peso': self.dados_antropometricos.get('peso_atual', 0)
            }
            self.historico_consultas.append(registro)

            messagebox.showinfo("Sucesso", "Dados antropométricos salvos!")
            self.salvar_arquivo()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def salvar_clinica(self):
        try:
            # Salvar doenças selecionadas
            doencas_selecionadas = []
            for doenca, var in self.doencas_vars.items():
                if var.get():
                    doencas_selecionadas.append(doenca)
            
            self.dados_clinicos['doencas'] = doencas_selecionadas
            self.dados_clinicos['medicamentos'] = self.medicamentos_text.get(1.0, tk.END).strip()
            
            # Salvar exames
            for campo, widget in self.campos_exames.items():
                valor = widget.get()
                if valor:
                    self.dados_clinicos[campo] = valor
            
            messagebox.showinfo("Sucesso", "Dados clínicos salvos!")
            self.salvar_arquivo()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def salvar_alimentar(self):
        try:
            # Salvar recordatório 24h
            self.dados_alimentares['recordatorio'] = {}
            for refeicao, widget in self.refeicoes.items():
                self.dados_alimentares['recordatorio'][refeicao] = widget.get(1.0, tk.END).strip()
            
            # Salvar frequência alimentar
            self.dados_alimentares['frequencia'] = {}
            for grupo, widget in self.frequencia_vars.items():
                self.dados_alimentares['frequencia'][grupo] = widget.get()
            
            # Salvar hábitos
            self.dados_alimentares['habitos'] = {}
            for campo, widget in self.campos_habitos.items():
                self.dados_alimentares['habitos'][campo] = widget.get()
            
            messagebox.showinfo("Sucesso", "Dados alimentares salvos!")
            self.salvar_arquivo()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def salvar_intervencao(self):
        try:
            self.dados_intervencao = {
                'objetivos': self.objetivos_text.get(1.0, tk.END).strip(),
                'dieta': self.dieta_text.get(1.0, tk.END).strip(),
                'suplementacao': self.suplemento_text.get(1.0, tk.END).strip(),
                'recomendacoes': self.recomendacoes_text.get(1.0, tk.END).strip()
            }
            messagebox.showinfo("Sucesso", "Dados de intervenção salvos!")
            self.salvar_arquivo()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def salvar_evolucao(self):
        try:
            # 1) coleta valores atuais nos campos
            for chave, widget in self.campos_evolucao.items():
                valor = widget.get().strip()
                if valor:
                    self.dados_evolucao[chave] = valor

            # 2) salva no JSON geral do paciente
            self.salvar_arquivo()

            # 3) salva num JSON separado
            evol_dir = os.path.join(os.getcwd(), "evoluções")
            os.makedirs(evol_dir, exist_ok=True)

            # sugestão de nome: evolucao_<nome>_YYYYMMDD_HHMMSS.json
            nome = self.dados_paciente.get('nome', 'paciente').replace(' ', '_')
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"evolucao_{nome}_{ts}.json"
            fname = os.path.join(evol_dir, f"evolucao_{nome}_{ts}.json")

            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(self.dados_evolucao, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("Sucesso",
                f"Evolução salva com sucesso em:\n{fname.split(os.sep)[-2]}/{fname.split(os.sep)[-1]}"
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar evolução: {e}")
    
    def salvar_arquivo(self):
        try:
            dados_completos = {
                'paciente': self.dados_paciente,
                'antropometricos': self.dados_antropometricos,
                'clinicos': self.dados_clinicos,
                'alimentares': self.dados_alimentares,
                'intervencao': self.dados_intervencao,
                'evolucao': self.dados_evolucao,
                'historico': self.historico_consultas,
                'ultima_atualizacao': datetime.now().isoformat()
            }
            
            nome_arquivo = f"avaliacao_{self.dados_paciente.get('nome', 'paciente').replace(' ', '_')}"
            pacientes_dir = os.path.join(os.getcwd(), "pacientes")
            os.makedirs(pacientes_dir, exist_ok=True)

            file_path = os.path.join(pacientes_dir, f"{nome_arquivo}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(dados_completos, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")
    
    # Métodos de limpeza
    def limpar_identificacao(self):
        for widget in self.campos_identificacao.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
    
    def limpar_anamnese(self):
        for widget in self.campos_anamnese.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete(1.0, tk.END)

    def limpar_antropometria(self):
        for widget in self.campos_antropometria.values():
            widget.delete(0, tk.END)
        
        for label in self.labels_resultados.values():
            label.config(text="--")
    
    def limpar_clinica(self):
        for var in self.doencas_vars.values():
            var.set(False)
        
        self.medicamentos_text.delete(1.0, tk.END)
        
        for widget in self.campos_exames.values():
            widget.delete(0, tk.END)
        
    def limpar_alimentar(self):
        for widget in self.refeicoes.values():
            widget.delete(1.0, tk.END)
        
        for widget in self.frequencia_vars.values():
            widget.set('')
        
        for widget in self.campos_habitos.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
    
    def limpar_intervencao(self):
        self.objetivos_text.delete(1.0, tk.END)
        self.dieta_text.delete(1.0, tk.END)
        self.suplemento_text.delete(1.0, tk.END)
        self.recomendacoes_text.delete(1.0, tk.END)
        # self.dados_intervencao.clear()
    
    def limpar_evolucao(self):
        for widget in self.campos_evolucao.values():
            widget.delete(0, tk.END)
        # self.dados_evolucao.clear()  # se quiser também esvaziar o dicionário
    
    # Adicionar ou carregar uma evolução nutricional
    def nova_evolucao(self):
        """Reseta a tela para cadastrar uma nova evolução."""
        self.dados_evolucao = {}
        self.limpar_evolucao()

    def carregar_evolucao(self):
        """Carrega um .json de evolução previamente salvo e preenche os campos."""
        path = filedialog.askopenfilename(
            title="Selecione arquivo de evolução",
            filetypes=[("JSON", "*.json")]
        )
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.dados_evolucao = data
            # preenche cada campo
            for chave, entry in self.campos_evolucao.items():
                entry.delete(0, tk.END)
                if chave in data:
                    entry.insert(0, data[chave])
            messagebox.showinfo("Sucesso", "Evolução carregada!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar: {e}")
    
    # Métodos do dashboard
    def atualizar_dashboard(self, event=None):
        # Atualizar cards de estatísticas
        if self.dados_antropometricos.get('imc'):
            self.imc_valor.config(text=f"{self.dados_antropometricos['imc']:.1f}")
            self.imc_classificacao.config(text=self.dados_antropometricos.get('classificacao_imc', '--'))
        
        # Determinar status nutricional
        status = self.determinar_status_nutricional()
        self.status_nutricional.config(text=status)
        
        # Determinar risco nutricional
        risco = self.determinar_risco_nutricional()
        self.risco_nutricional.config(text=risco)
        
        # Atualizar gráficos
        if hasattr(self, 'canvas'):
            self.atualizar_graficos_dashboard()
    
    def determinar_status_nutricional(self):
        imc = self.dados_antropometricos.get('imc', 0)
        perda_peso = self.dados_antropometricos.get('perda_peso_perc', 0)
        
        if imc < 22 or perda_peso > 10:
            return "Desnutrição"
        elif imc > 27:
            return "Sobrepeso"
        else:
            return "Adequado"
    
    def determinar_risco_nutricional(self):
        # Lógica simplificada de risco nutricional
        fatores_risco = 0
        
        # Idade avançada (assumindo > 80 anos)
        if self.dados_paciente.get('data_nascimento'):
            # Aqui deveria calcular a idade real
            fatores_risco += 1
        
        # Doenças crônicas
        if len(self.dados_clinicos.get('doencas', [])) > 2:
            fatores_risco += 1
        
        # Perda de peso
        if self.dados_antropometricos.get('perda_peso_perc', 0) > 5:
            fatores_risco += 1
        
        # Problemas alimentares
        if self.dados_alimentares.get('habitos', {}).get('apetite') in ['Regular', 'Ruim']:
            fatores_risco += 1
        
        if fatores_risco >= 3:
            return "Alto Risco"
        elif fatores_risco >= 1:
            return "Risco Moderado"
        else:
            return "Baixo Risco"
    
    # Métodos de relatórios
    def gerar_relatorio_completo(self):
        try:
            nome_paciente = self.dados_paciente.get('nome', 'paciente').replace(' ', '_')
            nome_arquivo = filedialog.asksaveasfilename(
                initialfile=f"relatorio_{nome_paciente}.pdf",         # nome já preenchido
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Salvar Relatório Completo"
            )
            
            if nome_arquivo:
                self.criar_pdf_completo(nome_arquivo)
                messagebox.showinfo("Sucesso", f"Relatório salvo em: {nome_arquivo}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def criar_pdf_completo(self, nome_arquivo):
        """
        Gera o PDF completo com todas as avaliações: identificação, antropometria, clínica e alimentar.
        """
        doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=1  # Centralizado
        )
        story.append(Paragraph("RELATÓRIO DE AVALIAÇÃO NUTRICIONAL - IDOSOS", title_style))
        story.append(Spacer(1, 12))
        
        # Seção: Dados Pessoais
        if self.dados_paciente:
            story.append(Paragraph("DADOS PESSOAIS", styles['Heading2']))
            dados_table = []
            for rotulo, key in [
                ("Nome:", 'nome'),
                ("Data de Nascimento:", 'data_nascimento'),
                ("Idade:", 'idade'),
                ("Sexo:", 'sexo'),
                ("Nº de Registro:", 'registro'),
                ("Telefone:", 'telefone'),
                ("Email:", 'email'),
                ("Endereço:", 'endereco'),
                ("Contato de Emergência:", 'contato_emergencia'),
                ("Telefone de Emergência:", 'telefone_emergencia'),
                ("Data da Admissão:", 'data_admissao'),
            ]:
                dados_table.append([rotulo, self.dados_paciente.get(key, '')])
            table = Table(dados_table, colWidths=[2*inch, 4*inch], hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BOX', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE')
            ]))
            story.append(table)
            story.append(Spacer(1, 12))
        
        # Seção: Avaliação Antropométrica
        if self.dados_antropometricos:
            story.append(Paragraph("AVALIAÇÃO ANTROPOMÉTRICA", styles['Heading2']))
            antro_table = []
            for rotulo, key in [
                ("IMC:", 'imc'),
                ("Classificação IMC:", 'classificacao_imc'),
                ("RCQ:", 'rcq'),
                ("Classificação RCQ:", 'classificacao_rcq'),
                ("Perda de Peso (%):", 'perda_peso_perc'),
                ("CMB (cm):", 'cmb'),
                ("AMB (cm²):", 'amb')
            ]:
                antro_table.append([rotulo, f"{self.dados_antropometricos.get(key, '')}"])
            table2 = Table(antro_table, colWidths=[2*inch, 4*inch], hAlign='LEFT')
            table2.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BOX', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE')
            ]))
            story.append(table2)
            story.append(Spacer(1, 12))
        
        # Seção: Avaliação Clínica
        if self.dados_clinicos:
            story.append(Paragraph("AVALIAÇÃO CLÍNICA", styles['Heading2']))
            # Doenças e condições
            doencas = self.dados_clinicos.get('doencas', [])
            story.append(Paragraph(f"<b>Doenças/Condições:</b> {', '.join(doencas)}", styles['Normal']))
            story.append(Spacer(1, 6))
            # Medicamentos
            meds = self.dados_clinicos.get('medicamentos', '')
            story.append(Paragraph(f"<b>Medicamentos:</b> {meds}", styles['Normal']))
            story.append(Spacer(1, 6))
            # Exames laboratoriais
            lab_items = []
            for rotulo, key in [
                ("Glicemia (mg/dL):", 'glicemia'),
                ("Hemoglobina (g/dL):", 'hemoglobina'),
                ("Colesterol Total (mg/dL):", 'colesterol_total'),
                ("HDL (mg/dL):", 'hdl'),
                ("LDL (mg/dL):", 'ldl'),
                ("Triglicerídeos (mg/dL):", 'triglicerideos')
            ]:
                val = self.dados_clinicos.get(key, '')
                lab_items.append([rotulo, val])
            table3 = Table(lab_items, colWidths=[2*inch, 4*inch], hAlign='LEFT')
            table3.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BOX', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE')
            ]))
            story.append(table3)
            story.append(Spacer(1, 12))
        
        # Seção: Avaliação Alimentar
        if self.dados_alimentares:
            story.append(Paragraph("AVALIAÇÃO ALIMENTAR", styles['Heading2']))
            # Recordatório
            record = self.dados_alimentares.get('recordatorio', {})
            for refeicao, texto in record.items():
                story.append(Paragraph(f"<b>{refeicao}:</b> {texto}", styles['Normal']))
                story.append(Spacer(1, 4))
            story.append(Spacer(1, 6))
            # Frequência alimentar
            freq = self.dados_alimentares.get('frequencia', {})
            freq_table = [[rotulo, freq.get(rotulo, '')] for rotulo in freq]
            if freq_table:
                table4 = Table(freq_table, colWidths=[3*inch, 3*inch], hAlign='LEFT')
                table4.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('BOX', (0,0), (-1,-1), 1, colors.black),
                    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE')
                ]))
                story.append(table4)
                story.append(Spacer(1, 12))
        
        # Seção: Intervenção Nutricional
        if self.dados_intervencao:
            story.append(Paragraph("INTERVENÇÃO NUTRICIONAL", styles['Heading2']))
            story.append(Spacer(1, 12))

            interven = self.dados_intervencao
            # Objetivos
            story.append(Paragraph(f"<b>Objetivos:</b> {interven.get('objetivos', '')}", styles['Normal']))
            story.append(Spacer(1, 6))
            # Dieta
            story.append(Paragraph(f"<b>Dieta:</b> {interven.get('dieta', '')}", styles['Normal']))
            story.append(Spacer(1, 6))
            # Suplementação
            story.append(Paragraph(f"<b>Suplementação:</b> {interven.get('suplementacao', '')}", styles['Normal']))
            story.append(Spacer(1, 6))
            # Recomendações
            story.append(Paragraph(f"<b>Recomendações:</b> {interven.get('recomendacoes', '')}", styles['Normal']))
            story.append(Spacer(1, 12))

        # Seção: Evolução Nutricional
        if self.dados_evolucao:
            story.append(Paragraph("EVOLUÇÃO NUTRICIONAL", styles['Heading2']))
            evo_table = []
            for rotulo, chave in [
                ("Peso (kg):", 'peso_evo'),
                ("IMC (kg/m²):", 'imc_evo'),
                ('Estado Nutricional:', 'estado_nutri_evo'),
                ('Adesão à Dieta:', 'adesao_dieta_evo'),
                ('Apetite:', 'apetite_evo'),
                ('Evolução Clínica:', 'evolucao_clinica_evo'),
                ('Circunferência do Braço (cm):', 'circ_braco_evo'),
                ('Circunferência Muscular do Braço (cm):', 'circ_musc_braco_evo'),
                ('Circunferência da Panturrilha (cm):', 'circ_panturrilha_evo'),
                ('Circunferência da Cintura (cm):', 'circ_cintura_evo'),
                ('Circunferência do Quadril (cm):', 'circ_quadril_evo'),
                ('Circunferência Abdominal (cm):', 'circ_abdominal_evo'),
                ('Dobra Cutânea Tricipital (mm):', 'dobra_triceps_evo'),
                ('Dobra Cutânea Bicipital (mm):', 'dobra_biceps_evo'),
                ('Dobra Cutânea Subescapular (mm):', 'dobra_subescapular_evo'),
                ('Dobra Cutânea Suprailiaca (mm):', 'dobra_suprailiaca_evo'),
                ('Dobra Cutânea Abdominal (mm):', 'dobra_abdominal_evo'),
                ('Dobra Cutânea Peitoral (mm):', 'dobra_peitoral_evo'),
                ('Dobra Cutânea Axilar (mm):', 'dobra_axilar_evo'),
                ("Avaliador:", 'nome_avaliador_evo')
            ]:
                evo_table.append([rotulo, self.dados_evolucao.get(chave, '')])
            table_evo = Table(evo_table, colWidths=[3*inch, 4*inch], hAlign='LEFT')
            table_evo.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
                ('BOX', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
            ]))
            story.append(table_evo)
            story.append(Spacer(1, 12))
        
        # --- Nova seção: Dashboard Nutricional ---
        story.append(Paragraph("DASHBOARD NUTRICIONAL", styles['Heading2']))
        story.append(Spacer(1, 12))

        status = self.determinar_status_nutricional()
        risco  = self.determinar_risco_nutricional()
        story.append(Paragraph(f"<b>Status Nutricional:</b> {status}", styles['Normal']))
        story.append(Paragraph(f"<b>Risco Nutricional:</b> {risco}", styles['Normal']))
        story.append(Spacer(1, 12))

        # Salva o gráfico em buffer
        buf = io.BytesIO()
        self.fig.savefig(buf, format='PNG', dpi=150, bbox_inches='tight')
        buf.seek(0)

        # Abre a imagem com PIL para calcular proporções reais
        pil_img = PILImage.open(buf)
        img_width, img_height = pil_img.size

        # Define a largura no PDF (ex: 6.5 polegadas) e calcula altura proporcional
        max_width = 6.5 * inch
        scale = max_width / img_width
        pdf_width = img_width * scale
        pdf_height = img_height * scale

        # Reposiciona o ponteiro e cria imagem no PDF com proporção preservada
        buf.seek(0)
        img = Image(buf, width=pdf_width, height=pdf_height)
        story.append(img)
        story.append(Spacer(1, 12))

        # Histórico de Consultas
        if self.historico_consultas:
            story.append(Paragraph("HISTÓRICO DE CONSULTAS", styles['Heading2']))
            hist_table = [[consulta.get('data', ''), consulta.get('peso', '')] for consulta in self.historico_consultas]
            if hist_table:
                table5 = Table([["Data", "Peso (kg)"]] + hist_table, colWidths=[3*inch, 3*inch], hAlign='LEFT')
                table5.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0,0),(-1,0), colors.whitesmoke),
                    ('BOX', (0,0), (-1,-1), 1, colors.black),
                    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE')
                ]))
                story.append(table5)
                story.append(Spacer(1, 12))

        # Construir documento
        doc.build(story)

    def carregar_dados(self):
        """
        Abre um diálogo para o usuário selecionar o arquivo JSON salvo
        e popula todos os campos da interface com os dados carregados.
        """
        nome_arquivo = filedialog.askopenfilename(
            title="Abrir avaliação",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        if not nome_arquivo:
            return

        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            # Carrega dicionários internos
            self.dados_paciente       = dados.get('paciente', {})
            self.dados_antropometricos = dados.get('antropometricos', {})
            self.dados_clinicos       = dados.get('clinicos', {})
            self.dados_alimentares    = dados.get('alimentares', {})
            self.dados_intervencao    = dados.get('intervencao', {})
            self.dados_evolucao    = dados.get('evolucao', {})
            self.historico_consultas  = dados.get('historico', [])

            # Preenche aba Identificação
            for campo, widget in self.campos_identificacao.items():
                valor = self.dados_paciente.get(campo, '')
                widget.delete(0, tk.END)
                widget.insert(0, valor)

            # Preenche aba Anamnese
            for campo, widget in self.campos_anamnese.items():
                valor = self.dados_paciente.get('anamnese', {}).get(campo, '')
                if isinstance(widget, tk.Text):
                    widget.delete(1.0, tk.END)
                    widget.insert(tk.END, valor)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, valor)

            # Preenche aba Antropometria (e já dispara cálculo para sincronizar labels)
            for campo, widget in self.campos_antropometria.items():
                valor = self.dados_antropometricos.get(campo, '')
                widget.delete(0, tk.END)
                widget.insert(0, valor)
            self.calcular_antropometria()

            # Preenche aba Clínica
            for doenca, var in self.doencas_vars.items():
                var.set(doenca in self.dados_clinicos.get('doencas', []))
            self.medicamentos_text.delete(1.0, tk.END)
            self.medicamentos_text.insert(tk.END, self.dados_clinicos.get('medicamentos', ''))
            for campo, widget in self.campos_exames.items():
                valor = self.dados_clinicos.get(campo, '')
                widget.delete(0, tk.END)
                widget.insert(0, valor)

            # Preenche aba Alimentar
            for refeicao, widget in self.refeicoes.items():
                texto = self.dados_alimentares.get('recordatorio', {}).get(refeicao, '')
                widget.delete(1.0, tk.END)
                widget.insert(tk.END, texto)
            for grupo, widget in self.frequencia_vars.items():
                widget.set(self.dados_alimentares.get('frequencia', {}).get(grupo, ''))
            for campo, widget in self.campos_habitos.items():
                widget_val = self.dados_alimentares.get('habitos', {}).get(campo, '')
                if isinstance(widget, ttk.Combobox):
                    widget.set(widget_val)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, widget_val)

            # Preenche aba Intervenção
            self.objetivos_text.delete(1.0, tk.END)
            self.objetivos_text.insert(tk.END, self.dados_intervencao.get('objetivos', ''))
            self.dieta_text.delete(1.0, tk.END)
            self.dieta_text.insert(tk.END, self.dados_intervencao.get('dieta', ''))
            self.suplemento_text.delete(1.0, tk.END)
            self.suplemento_text.insert(tk.END, self.dados_intervencao.get('suplementacao', ''))
            self.recomendacoes_text.delete(1.0, tk.END)
            self.recomendacoes_text.insert(tk.END, self.dados_intervencao.get('recomendacoes', ''))

            # Preenche aba Evolução
            for chave, entry in self.campos_evolucao.items():
                valor = self.dados_evolucao.get(chave, '')
                entry.delete(0, tk.END)
                entry.insert(0, valor)

            # Atualiza dashboard
            self.atualizar_dashboard()

            messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {e}")

    # Stubs para outras funções de relatório
    def gerar_relatorio_especifico(self, tipo):
        messagebox.showinfo("Info", f"Função de relatório específico ({tipo}) em desenvolvimento.")

    def visualizar_relatorio(self):
        messagebox.showinfo("Info", "Visualização de PDF não implementada.")

    def exportar_dashboard(self):
        messagebox.showinfo("Info", "Exportação do dashboard em desenvolvimento.")

    def salvar_graficos(self):
        messagebox.showinfo("Info", "Salvar gráficos em desenvolvimento.")


def on_closing(root):
    if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
        root.destroy()
        sys.exit(0)  # Garante que o programa encerre completamente

if __name__ == "__main__":
    root = tk.Tk()
    app = AvaliacaoNutricionalIdosos(root)
    # Aqui vinculamos o fechamento à janela principal:
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()
