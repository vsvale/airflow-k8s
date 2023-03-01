### Update system
    - sudo -- sh -c 'apt-get update; apt-get upgrade -y; apt-get dist-upgrade -y; apt-get autoremove -y; apt-get autoclean -y'

### Install git
    - sudo apt install git

### Install Docker:
    - sudo apt update
    - sudo apt install -y ca-certificates curl gnupg lsb-release apt-transport-https software-properties-common
    - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    - echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    - sudo apt-get update
    - sudo apt install docker-ce docker-ce-cli containerd.io -y
    - sudo chmod 666 /var/run/docker.sock
    - sudo usermod -aG docker $USER && newgrp docker

### Install Helm:
    - curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
    - sudo apt-get install apt-transport-https --yes
    - echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
    - sudo apt-get update
    - sudo apt-get install helm
    - helm repo add argo https://argoproj.github.io/argo-helm && helm repo add bitnami https://charts.bitnami.com/bitnami && helm repo add minio https://operator.min.io/ && helm repo add apache-airflow https://airflow.apache.org/ && helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator 
    - helm repo update

### Install K3d
    - curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

### Install Kubectl
    - sudo apt-get update
    - sudo apt-get install -y ca-certificates curl apt-transport-https
    - sudo curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    - sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

### Install Terraform
    - sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
    - sudo apt update && sudo apt install gpg
    - wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
    - echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    - sudo apt update
    - sudo apt install terraform
    - terraform version

### Create Cluster
    - k3d cluster create airflowk8s --volume $HOME/airflowk8s:/var/lib/rancher/k3s/storage@all -s 1 --servers-memory 12Gb -a 3 --agents-memory 50gb --api-port 6443 -p 8081:80@loadbalancer

### Create namespaces
    - cd ./iac && terraform init && terraform plan && terraform apply -auto-approve && cd .. && kubectl get ns

### Install Argocd
    - helm upgrade --install -f https://raw.githubusercontent.com/vsvale/airflow-k8s/main/repository/argo-cd/values.yaml argocd argo/argo-cd --namespace cicd --debug --timeout 10m0s
    - watch kubectl get all -n cicd
    - App of Apps: kubectl apply -f https://raw.githubusercontent.com/vsvale/airflow-k8s/main/repository/repository.yaml
    - http://127.0.0.1:8081/argocd/login
    - user: admin
    - password: kubectl -n cicd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d  | more

### Install Airflow
    - helm upgrade --install -f https://raw.githubusercontent.com/vsvale/airflow-k8s/main/repository/airflow/values.yaml airflow apache-airflow/airflow --namespace orchestrator --create-namespace --debug --timeout 20m0s
        - Utilizando images.airflow.repository:  vsvale/airflow:2.5.1 para utilizar umaimagem do airflow com os seguintes [requirements](https://raw.githubusercontent.com/vsvale/airflow-k8s/main/repository/image/airflow/requirements.txt)
        - Utilizando dags.gitSync.repo: https://github.com/vsvale/airflow-k8s.git para buscar as dags no git na pasta dags desse repositório


### Install Spark

### Install MiniO
