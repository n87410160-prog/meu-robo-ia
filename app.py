import streamlit as st
from google import genai
from google.genai import types

# Configuração da página da Web
st.set_page_config(page_title="Super Robô IA", page_icon="🤖", layout="centered")

# ==========================================
# 1. ARQUITETURA DE SEGURANÇA E CHAVES
# ==========================================
CHAVE_MESTRA = st.secrets["CHAVE_MESTRA"]
chave_api = st.secrets["GEMINI_API_KEY"]

# Inicializa a senha do cliente na memória estável do servidor
if "senha_cliente_atual" not in st.session_state:
    st.session_state["senha_cliente_atual"] = st.secrets["SENHA_CLIENTE_PADRAO"]

# Menu de navegação limpo
menu = st.sidebar.selectbox("Navegação", ["🤖 Robô Organizador", "⚙️ Painel do Dono (Secreto)"])

# ==========================================
# SEÇÃO 1: PAINEL DO DONO (SECRETO)
# ==========================================
if menu == "⚙️ Painel do Dono (Secreto)":
    st.subheader("⚙️ Painel Administrativo Secreto")
    st.write("Gerencie o acesso dos seus clientes por aqui.")
    
    autenticado = st.text_input("Digite sua Chave Mestra:", type="password")
    
    if autenticado == CHAVE_MESTRA:
        st.success("Acesso administrativo liberado!")
        st.write(f"🔑 A senha atual do cliente é: **{st.session_state['senha_cliente_atual']}**")
        
        nova_senha = st.text_input("Digite a nova senha que deseja definir para os clientes:")
        if st.button("Mudar Senha dos Clientes"):
            if nova_senha.strip() != "":
                st.session_state["senha_cliente_atual"] = nova_senha.strip()
                st.success(f"Sucesso! A nova senha dos clientes agora é: {nova_senha}")
            else:
                st.error("A senha não pode ser vazia.")
    elif autenticado != "":
        st.error("Chave Mestra incorreta!")

# ==========================================
# SEÇÃO 2: O ROBÔ (O QUE O CLIENTE VÊ)
# ==========================================
elif menu == "🤖 Robô Organizador":
    st.title("🤖 O Robô Faz-Tudo com IA")
    st.write("A inteligência artificial definitiva para organizar seus arquivos e mídias.")

    senha_usuario = st.text_input("🔑 Digite sua senha de assinante para liberar o robô:", type="password")

    if senha_usuario == st.session_state["senha_cliente_atual"]:
        st.sidebar.success("Acesso Liberado!")
        st.sidebar.info("Status: Assinatura Ativa via BTG Pactual.")
        
        # Inicializa o motor do Gemini de última geração
        client = genai.Client(api_key=chave_api)
        
        arquivo_enviado = st.file_uploader("📂 Escolha ou arraste qualquer arquivo para o robô analisar:")

        if arquivo_enviado is not None:
            st.write("🧠 Analisando o conteúdo com Gemini 3.8 Flash...")
            nome_arquivo = arquivo_enviado.name
            extensao = nome_arquivo.split(".")[-1].lower() if "." in nome_arquivo else ""
            
            instrucao = (
                "Você é o motor de um robô organizador de arquivos supremo. "
                "Analise o arquivo enviado (seja por nome, metadados ou conteúdo) e me diga "
                "em APENAS UMA frase curta e direta em qual dessas pastas ele deve ser guardado e o motivo técnico: "
                "[Fotos, Documentos, Jogos, Musicas, Outros]."
            )
            
            try:
                if extensao in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                    bytes_arquivo = arquivo_enviado.getvalue()
                    resposta = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=[
                            types.Part.from_bytes(data=bytes_arquivo, mime_type=f"image/{extensao}"),
                            instrucao
                        ]
                    )
                else:
                    bytes_arquivo = arquivo_enviado.getvalue()
                    snippet_texto = bytes_arquivo[:2000].decode('utf-8', errors='ignore')
                    
                    resposta = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=[
                            f"Nome do arquivo: {nome_arquivo}\nConteúdo interno do arquivo:\n{snippet_texto}", 
                            instrucao
                        ]
                    )
                
                st.success(f"🤖 Resultado da IA: {resposta.text.strip()}")
                
            except Exception as e:
                st.error(f"Erro na execução da IA: {e}")
                
    else:
        if senha_usuario != "":
            st.error("❌ Senha inválida ou expirada!")
        
        st.markdown("---")
        st.subheader("👋 Quer liberar o acesso ilimitado ao Super Robô?")
        st.write("Assine agora por apenas **R$ 9,90/mês** e receba sua chave de acesso!")
        
        with st.expander("💸 Clique aqui para pagar via PIX (Conta BTG)", expanded=True):
            st.write("1. Abra o app do seu banco e escolha **Pagar via Pix**.")
            st.write("2. Envie o valor de **R$ 9,90** para a chave Pix do BTG abaixo:")
            
            # 🔥 SUA CHAVE FIXA BLINDADA AGORA ESTÁ NO LUGAR CERTO!
            sua_chave_pix_fixa = "b835daa9-7fc1-4966-a4c2-4e8a1aa0c762" 
            
            st.code(sua_chave_pix_fixa, language="text")
            st.caption("Após realizar o pagamento de R$ 9,90, envie o comprovante por um dos canais abaixo.")
            
            st.markdown("---")
            st.write("3. **Libere seu acesso instantaneamente:**")
            st.write("Escolha por onde você prefere enviar o comprovante para receber sua senha:")
            
            # --- Configuração Automatizada do WhatsApp ---
            seu_numero_whatsapp = "5545999153564" 
            mensagem_whatsapp = "Oi! Acabei de fazer o Pix de R$ 9,90 para o Super Robô. Aqui está o meu comprovante para liberar minha senha de acesso!"
            link_whatsapp = f"https://wa.me{seu_numero_whatsapp}?text={mensagem_whatsapp.replace(' ', '%20')}"
            
            # --- Configuração Automatizada do E-mail ---
            seu_email = "bernardocountryballs207@gmail.com" 
            assunto_email = "Comprovante de Pagamento - Super Robô IA"
            corpo_email = "Oi! Segue em anexo o meu comprovante de R$ 9,90 referente à assinatura do robô. Aguardo minha senha!"
            link_email = f"mailto:{seu_email}?subject={assunto_email.replace(' ', '%20')}&body={corpo_email.replace(' ', '%20')}"
            
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("🟢 Enviar via WhatsApp", link_whatsapp, use_container_width=True)
            with col2:
                st.link_button("🔵 Enviar via E-mail", link_email, use_container_width=True)