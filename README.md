# 🥦 Sistema de Avaliação Nutricional - Idosos

Este é um sistema interativo e completo para **avaliação nutricional de idosos**, desenvolvido com `Python`, `Tkinter`, `matplotlib`, `reportlab`, entre outros. A aplicação permite registrar, analisar e gerar relatórios em PDF de diversos dados clínicos, antropométricos, alimentares e de intervenção nutricional.

## ✨ Funcionalidades

-   📋 Cadastro completo do paciente
-   🧠 Anamnese e histórico de saúde
-   📏 Avaliação antropométrica com cálculo de IMC, RCQ, perda de peso, CMB e AMB
-   💊 Avaliação clínica: doenças, medicamentos e exames laboratoriais
-   🥗 Avaliação alimentar: recordatório 24h, frequência alimentar e hábitos
-   🎯 Plano de intervenção nutricional
-   📊 Dashboard com gráficos dinâmicos de evolução do peso, macronutrientes e indicadores
-   📄 Geração de relatórios em PDF (com gráficos e análises integradas)

## 💻 Captura de Tela

> Exemplo do dashboard com indicadores e gráficos:
> ![exemplo_dashboard](https://via.placeholder.com/800x400?text=Captura+do+Dashboard)

## 🛠️ Instalação

1. Clone o repositório ou baixe o arquivo `app.py`.
2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

> **Dica:** Se você não tiver o `requirements.txt`, use o comando abaixo para instalar as principais dependências:

```bash
pip install matplotlib numpy reportlab pillow
```

4. Execute o sistema:

```bash
python app.py
```

## 📁 Estrutura do Projeto

```
app.py                  # Código principal da aplicação
avaliacao_<nome>.json    # Arquivos salvos com dados do paciente
relatorio_<nome>.pdf     # Relatórios gerados em PDF
```

## 📌 Requisitos

-   Python 3.8 ou superior
-   Sistema operacional: Windows, Linux ou MacOS
-   Recomendado: resolução mínima de 1366x768 para melhor visualização

## 👨‍💻 Autor

Desenvolvido por **Jhonny Silva - jnslnutridev**  
💻🔗 https://github.com/jnslnutridev  
📅 2025

---

Este projeto é ideal para **nutricionistas, estagiários e profissionais da saúde** que trabalham com o cuidado nutricional de idosos. Se desejar expandir a aplicação ou integrá-la com bancos de dados ou sistemas web, sinta-se à vontade para adaptar!
