FROM hashicorp/terraform:latest   # Usa a imagem oficial do Terraform
WORKDIR /app                      # Define o diretório de trabalho
COPY ./terraform /app            # Copia a pasta local "terraform" para dentro do container
ENTRYPOINT ["terraform"]         # Define o entrypoint como o binário "terraform"
