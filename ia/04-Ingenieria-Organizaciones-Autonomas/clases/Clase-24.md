# Clase 24: Company-in-a-Box - Implementación

## Duración
**4 horas** (240 minutos)

---

## Objetivos de Aprendizaje

Al finalizar esta clase, el estudiante será capaz de:

1. Implementar playbooks Ansible para automatización de configuración
2. Crear pipelines CI/CD completos para agentes con GitHub Actions
3. Configurar monitoring stack con Prometheus y Grafana
4. Implementar estrategias de disaster recovery
5. Integrar todos los componentes en un sistema funcional
6. Documentar y mantener la infraestructura

---

## 1. Ansible para Configuración de Agentes

### 1.1 Estructura de Playbooks

```yaml
# ansible/ansible.cfg
[defaults]
inventory = ./inventory
roles_path = ./roles
host_key_checking = False
retry_files_enabled = False
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
interpreter_python = auto_silent

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False

[ssh_connection]
pipelining = True
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
```

```yaml
# ansible/inventory/production/hosts.ini
[all:vars]
ansible_user=ubuntu
ansible_python_interpreter=/usr/bin/python3
ansible_connection=ssh

[agents]
agent-coder-[01:05] ansible_host=10.0.1.[10:14]
agent-reviewer-[01:03] ansible_host=10.0.1.[20:22]
agent-tester-[01:02] ansible_host=10.0.1.[30:31]

[databases]
db-primary ansible_host=10.0.2.10
db-replica-[01:02] ansible_host=10.0.2.[11:12]

[redis]
redis-[01:03] ansible_host=10.0.2.[20:22]

[monitoring]
prometheus ansible_host=10.0.3.10
grafana ansible_host=10.0.3.11
loki ansible_host=10.0.3.12

[k8s_master]
k8s-master-[01:03] ansible_host=10.0.4.[10:12]

[k8s_worker]
k8s-worker-[01:10] ansible_host=10.0.5.[10:19]

[agent_system:children]
agents
databases
redis
monitoring
```

### 1.2 Playbook Principal

```yaml
# ansible/playbooks/agent-system.yml
---
- name: Provision Agent System Infrastructure
  hosts: all
  become: true
  gather_facts: true
  
  vars:
    agent_version: "1.0.0"
    docker_version: "24.0"
    redis_version: "7.2"
    postgres_version: "15"
    monitoring_stack_version: "1.0"
  
  tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: yes
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"
    
    - name: Install common packages
      ansible.builtin.apt:
        name:
          - curl
          - wget
          - git
          - vim
          - htop
          - tmux
          - unzip
          - gnupg2
          - ca-certificates
          - lsb-release
        state: present
      when: ansible_os_family == "Debian"
    
    - name: Configure timezone
      community.general.timezone:
        name: UTC

- name: Configure Agent Nodes
  hosts: agents
  become: true
  
  roles:
    - role: docker
    - role: agent_runtime
  
  tasks:
    - name: Create agent directories
      ansible.builtin.file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
      loop:
        - /opt/agents
        - /opt/agents/logs
        - /opt/agents/cache
        - /var/log/agents
    
    - name: Pull agent Docker images
      docker_image:
        name: "agent-registry/agent-{{ agent_type }}:{{ agent_version }}"
        source: pull
        force_source: yes
      vars:
        agent_type: "{{ inventory_hostname.split('-')[1] }}"
    
    - name: Configure agent service
      template:
        src: templates/agent.service.j2
        dest: /etc/systemd/system/agent-{{ agent_type }}.service
        mode: '0644'
      notify: restart_agent
      vars:
        agent_type: "{{ inventory_hostname.split('-')[1] }}"
    
    - name: Enable and start agent service
      systemd:
        name: "agent-{{ agent_type }}"
        state: started
        enabled: yes
        daemon_reload: yes
      vars:
        agent_type: "{{ inventory_hostname.split('-')[1] }}"

  handlers:
    - name: restart_agent
      systemd:
        name: "agent-{{ agent_type }}"
        state: restarted
      vars:
        agent_type: "{{ inventory_hostname.split('-')[1] }}"

- name: Configure Database Nodes
  hosts: databases
  become: true
  
  roles:
    - role: postgresql
      vars:
        postgres_version: "15"
        postgres_port: 5432
        postgres_max_connections: 200
        postgres_shared_buffers: "256MB"
        postgres_effective_cache_size: "1GB"
        postgres_maintenance_work_mem: "64MB"
        postgres_checkpoint_completion_target: 0.9
        postgres_wal_buffers: "16MB"
        postgres_default_statistics_target: 100
        postgres_random_page_cost: 1.1
        postgres_effective_io_concurrency: 200
        postgres_work_mem: "655kB"
        postgres_min_wal_size: "1GB"
        postgres_max_wal_size: "4GB"
  
  tasks:
    - name: Create agent database
      postgresql_db:
        name: agentdb
        encoding: UTF8
        lc_collate: en_US.UTF-8
        lc_ctype: en_US.UTF-8
        state: present
      become: yes
      become_user: postgres
    
    - name: Create agent user
      postgresql_user:
        name: agentuser
        password: "{{ vault_postgres_password }}"
        db: agentdb
        priv: ALL
        state: present
      become: yes
      become_user: postgres

- name: Configure Redis Cluster
  hosts: redis
  become: true
  
  roles:
    - role: redis
      vars:
        redis_version: "7.2"
        redis_port: 6379
        redis_maxmemory: "512mb"
        redis_maxmemory_policy: "allkeys-lru"
        redis_appendonly: yes
        redis_appendfsync: "everysec"
  
  tasks:
    - name: Configure Redis replication
      template:
        src: templates/redis.conf.j2
        dest: /etc/redis/redis.conf
        mode: '0644'
      notify: restart_redis
    
    - name: Enable Redis service
      systemd:
        name: redis
        state: started
        enabled: yes

  handlers:
    - name: restart_redis
      systemd:
        name: redis
        state: restarted

- name: Configure Monitoring Stack
  hosts: monitoring
  become: true
  
  roles:
    - role: prometheus
      vars:
        prometheus_version: "2.47"
        prometheus_storage_tsdb_retention_time: "15d"
        prometheus_storage_tsdb_size: "10GB"
    
    - role: grafana
      vars:
        grafana_version: "10.1"
        grafana_admin_user: admin
        grafana_admin_password: "{{ vault_grafana_password }}"
    
    - role: loki
      vars:
        loki_version: "2.8"
        loki_storage_bucket: "agent-logs"
```

### 1.3 Roles de Ansible

```yaml
# ansible/roles/docker/tasks/main.yml
---
- name: Install prerequisites
  ansible.builtin.apt:
    name:
      - apt-transport-https
      - ca-certificates
      - curl
      - gnupg
      - lsb-release
    state: present
    update_cache: yes

- name: Add Docker GPG key
  ansible.builtin.apt_key:
    url: https://download.docker.com/linux/ubuntu/gpg
    state: present

- name: Add Docker repository
  ansible.builtin.apt_repository:
    repo: "deb [arch=amd64] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} stable"
    state: present

- name: Install Docker
  ansible.builtin.apt:
    name:
      - docker-ce
      - docker-ce-cli
      - containerd.io
      - docker-buildx-plugin
      - docker-compose-plugin
    state: present
    update_cache: yes

- name: Add Docker user to group
  ansible.builtin.user:
    name: "{{ ansible_user }}"
    groups: docker
    append: yes

- name: Configure Docker daemon
  template:
    src: daemon.json.j2
    dest: /etc/docker/daemon.json
    mode: '0644'
  notify: restart_docker

- name: Ensure Docker is started
  systemd:
    name: docker
    state: started
    enabled: yes

- name: Wait for Docker to be ready
  wait_for:
    port: 2375
    state: started
    timeout: 30
  ignore_errors: yes
```

```yaml
# ansible/roles/agent_runtime/tasks/main.yml
---
- name: Create agent system user
  ansible.builtin.user:
    name: agent
    comment: "Agent System User"
    shell: /bin/bash
    home: /opt/agents
    system: yes
    create_home: yes

- name: Create agent directories
  ansible.builtin.file:
    path: "{{ item }}"
    state: directory
    owner: agent
    group: agent
    mode: '0755'
  loop:
    - /opt/agents
    - /opt/agents/config
    - /opt/agents/logs
    - /opt/agents/cache
    - /var/log/agents

- name: Create agent config
  template:
    src: config.yml.j2
    dest: /opt/agents/config/agent.yml
    owner: agent
    group: agent
    mode: '0600'

- name: Pull agent Docker image
  docker_image:
    name: "agent-registry/agent-{{ agent_type | default('generic') }}"
    tag: "{{ agent_version | default('latest') }}"
    source: pull
    force_source: yes

- name: Create systemd service
  template:
    src: agent.service.j2
    dest: /etc/systemd/system/agent-{{ agent_type | default('generic') }}.service
    mode: '0644'
  notify:
    - reload_systemd
    - restart_agent

- name: Enable agent service
  systemd:
    name: "agent-{{ agent_type | default('generic') }}"
    enabled: yes
    state: started

- name: Configure log rotation
  template:
    src: logrotate.conf.j2
    dest: /etc/logrotate.d/agent-{{ agent_type | default('generic') }}
    mode: '0644'
```

```yaml
# ansible/roles/agent_runtime/templates/agent.service.j2
[Unit]
Description=Agent {{ agent_type | default('generic') }} Service
After=network-online.target docker.service
Wants=network-online.target docker.service
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Type=simple
User=agent
Group=agent
WorkingDirectory=/opt/agents

ExecStartPre=-/usr/bin/docker stop agent-{{ agent_type | default('generic') }}
ExecStartPre=-/usr/bin/docker rm agent-{{ agent_type | default('generic') }}
ExecStart=/usr/bin/docker run \
    --name agent-{{ agent_type | default('generic') }} \
    --restart unless-stopped \
    --memory={{ agent_memory_limit | default('1g') }} \
    --cpus={{ agent_cpu_limit | default('1.0') }} \
    --env-file=/opt/agents/config/agent.yml \
    -v /opt/agents/logs:/app/logs \
    -v /opt/agents/cache:/app/cache \
    -v /var/log/agents:/var/log/agents \
    --log-opt max-size=100m \
    --log-opt max-file=5 \
    agent-registry/agent-{{ agent_type | default('generic') }}:{{ agent_version | default('latest') }}

ExecStop=/usr/bin/docker stop -t 30 agent-{{ agent_type | default('generic') }}
ExecReload=/bin/kill -s HUP $MAINPID

Restart=on-failure
RestartSec=10s

StandardOutput=journal
StandardError=journal
SyslogIdentifier=agent-{{ agent_type | default('generic') }}

[Install]
WantedBy=multi-user.target
```

---

## 2. CI/CD para Agentes

### 2.1 Pipeline Completo de CI/CD

```yaml
# .github/workflows/agent-cicd.yaml
name: Agent CI/CD Pipeline

on:
  push:
    branches:
      - main
      - develop
    tags:
      - 'v*'
  pull_request:
    branches: [main]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  HELM_VERSION: "3.13.0"
  TERRAFORM_VERSION: "1.6.0"
  KUBECTL_VERSION: "1.28.0"

jobs:
  # ==================== LINT & VALIDATE ====================
  lint:
    name: Lint & Validate
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install linting tools
      run: |
        pip install yamllint helmfile hadolint ansible-lint tflint
    
    - name: Lint YAML files
      run: |
        yamllint -c .yamllint.yaml ansible/ deploy/ helm/
    
    - name: Lint Helm charts
      run: |
        for chart in deploy/helm/*/; do
          helm lint "$chart" || exit 1
        done
    
    - name: Lint Dockerfiles
      run: |
        find . -name "Dockerfile*" -exec hadolint {} \;
    
    - name: Lint Ansible
      run: |
        ansible-lint ansible/
    
    - name: Validate Terraform
      run: |
        cd infrastructure/terraform
        terraform fmt -check -recursive
        terraform validate

  # ==================== UNIT TESTS ====================
  test-unit:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pytest pytest-cov pytest-asyncio black flake8
    
    - name: Run Python tests
      run: |
        pytest tests/unit/ -v --cov=agents --cov-report=xml --cov-fail-under=80
    
    - name: Run linting
      run: |
        black --check agents/
        flake8 agents/ --max-line-length=100

  # ==================== BUILD IMAGES ====================
  build-agents:
    name: Build Agent Images
    needs: [lint, test-unit]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        agent:
          - coder
          - reviewer
          - tester
          - planner
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ github.repository }}/agent-${{ matrix.agent }}
        tags: |
          type=sha,prefix=,suffix=,format=short
          type=ref,event=branch
          type=semver,pattern={{version}}
    
    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: ./agents/${{ matrix.agent }}
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
        build-args: |
          BUILD_DATE=${{ steps.meta.outputs.created }}
          VERSION=${{ steps.meta.outputs.version }}

  # ==================== INTEGRATION TESTS ====================
  test-integration:
    name: Integration Tests
    needs: build-agents
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install test dependencies
      run: |
        pip install pytest pytest-docker-compose redis asyncpg
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v --tb=short
      env:
        REDIS_URL: redis://localhost:6379
        DATABASE_URL: postgresql://test:test@localhost:5432/testdb

  # ==================== SECURITY SCAN ====================
  security:
    name: Security Scan
    needs: build-agents
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: '${{ env.REGISTRY }}/${{ github.repository }}/agent-coder:latest'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run Trivy on Docker image
      run: |
        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
          aquasec/trivy:latest image \
          --severity HIGH,CRITICAL \
          --exit-code 1 \
          '${{ env.REGISTRY }}/${{ github.repository }}/agent-coder:latest'

  # ==================== DEPLOY TO STAGING ====================
  deploy-staging:
    name: Deploy to Staging
    needs: [build-agents, test-integration, security]
    runs-on: ubuntu-latest
    environment: staging
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: ${{ env.KUBECTL_VERSION }}
    
    - name: Configure kubectl
      run: |
        echo "${{ secrets.KUBE_CONFIG_STAGING }}" | base64 -d > kubeconfig
        export KUBECONFIG=$PWD/kubeconfig
        kubectl cluster-info
    
    - name: Deploy with Helmfile
      run: |
        curl -fsSL https://raw.githubusercontent.com/helmfile/helmfile/main/get-helmfile | sh
        
        helmfile -e staging apply \
          --set image.tag=${{ github.sha }} \
          --atomic \
          --timeout 10m
    
    - name: Verify deployment
      run: |
        export KUBECONFIG=$PWD/kubeconfig
        kubectl rollout status deployment/agent-coder -n staging --timeout=300s
        kubectl rollout status deployment/agent-reviewer -n staging --timeout=300s
        
        # Run smoke tests
        ./scripts/smoke-test.sh staging

  # ==================== SMOKE TESTS ====================
  smoke-tests:
    name: Smoke Tests
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run smoke tests
      run: |
        ./scripts/smoke-tests.sh staging
      env:
        API_URL: https://staging.agents.example.com
        SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}

  # ==================== DEPLOY TO PRODUCTION ====================
  deploy-production:
    name: Deploy to Production
    needs: smoke-tests
    runs-on: ubuntu-latest
    environment: production
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: ${{ env.KUBECTL_VERSION }}
    
    - name: Configure kubectl
      run: |
        echo "${{ secrets.KUBE_CONFIG_PRODUCTION }}" | base64 -d > kubeconfig
        export KUBECONFIG=$PWD/kubeconfig
    
    - name: Create GitHub deployment
      uses: alice-plu/activepieces-deployment-action@main
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        environment: production
    
    - name: Deploy to production
      run: |
        # Update version in Helm values
        VERSION=${GITHUB_REF#refs/tags/v}
        sed -i "s/tag:.*/tag: \"$VERSION\"/" deploy/helm/agent-system/values-prod.yaml
        
        # Commit version bump
        git config user.name "GitHub Actions"
        git config user.email "actions@github.com"
        git add -A
        git commit -m "Release version $VERSION" || true
        git push
        
        # Apply with ArgoCD
        argocd app set agent-system-prod --kustomize-revision production-$VERSION
        argocd app sync agent-system-prod --force --timeout 600
    
    - name: Notify deployment
      if: always()
      uses: slackapi/slack-github-action@v1
      with:
        payload: |
          {
            "text": "Production deployment ${{ job.status }}: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
          }
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
        SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK

  # ==================== POST-DEPLOY MONITORING ====================
  post-deploy:
    name: Post-Deploy Monitoring
    needs: deploy-production
    runs-on: ubuntu-latest
    if: always()
    steps:
    - uses: actions/checkout@v4
    
    - name: Monitor deployment health
      run: |
        ./scripts/post-deploy-check.sh production 15
      env:
        PROMETHEUS_URL: ${{ secrets.PROMETHEUS_URL }}
    
    - name: Create deployment summary
      uses: actions/github-script@v7
      with:
        script: |
          github.rest.repos.createDeploymentStatus({
            owner: context.repo.owner,
            repo: context.repo.repo,
            deployment_id: context.payload.deployment.id,
            state: '${{ job.status }}' === 'success' ? 'success' : 'failure',
            environment_url: 'https://agents.example.com'
          })
```

### 2.2 Smoke Tests

```bash
#!/bin/bash
# scripts/smoke-tests.sh

set -e

ENVIRONMENT=${1:-staging}
API_URL=${API_URL:-"https://${ENVIRONMENT}.agents.example.com"}
TIMEOUT=300
INTERVAL=10

echo "=== Running Smoke Tests for ${ENVIRONMENT} ==="

# Test 1: Health check
echo "Test 1: Health endpoint"
for i in $(seq 1 $((TIMEOUT/INTERVAL))); do
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${API_URL}/health)
    if [ "$RESPONSE" == "200" ]; then
        echo "  ✓ Health check passed"
        break
    fi
    if [ $i -eq $((TIMEOUT/INTERVAL)) ]; then
        echo "  ✗ Health check failed after ${TIMEOUT}s"
        exit 1
    fi
    sleep $INTERVAL
done

# Test 2: Ready check
echo "Test 2: Ready endpoint"
READY_RESPONSE=$(curl -s ${API_URL}/ready)
if echo "$READY_RESPONSE" | grep -q '"status":"ready"'; then
    echo "  ✓ Ready check passed"
else
    echo "  ✗ Ready check failed: $READY_RESPONSE"
    exit 1
fi

# Test 3: Metrics endpoint
echo "Test 3: Metrics endpoint"
METRICS=$(curl -s ${API_URL}/metrics)
if echo "$METRICS" | grep -q "agent_requests_total"; then
    echo "  ✓ Metrics endpoint working"
else
    echo "  ✗ Metrics endpoint issue"
    exit 1
fi

# Test 4: Agent task submission
echo "Test 4: Task submission"
TASK_RESPONSE=$(curl -s -X POST ${API_URL}/tasks \
    -H "Content-Type: application/json" \
    -d '{"task_id":"test-001","payload":{"action":"ping"}}')
TASK_ID=$(echo $TASK_RESPONSE | jq -r '.task_id')
if [ "$TASK_ID" == "test-001" ]; then
    echo "  ✓ Task submission working"
else
    echo "  ✗ Task submission failed: $TASK_RESPONSE"
    exit 1
fi

# Test 5: Check agent pods are running
echo "Test 5: Agent pod status"
export KUBECONFIG=${KUBECONFIG:-~/.kube/config}
PODS=$(kubectl get pods -n ${ENVIRONMENT} -l app=agent -o json | jq '.items | length')
if [ "$PODS" -ge 3 ]; then
    echo "  ✓ Found $PODS agent pods running"
else
    echo "  ✗ Expected at least 3 pods, found $PODS"
    exit 1
fi

# Test 6: Check no pods in CrashLoopBackOff
echo "Test 6: Pod health"
CRASHING=$(kubectl get pods -n ${ENVIRONMENT} -l app=agent --field-selector=status.phase=Running -o json | jq '[.items[] | select(.status.containerStatuses[].state.waiting.reason == "CrashLoopBackOff")] | length')
if [ "$CRASHING" == "0" ]; then
    echo "  ✓ No pods in CrashLoopBackOff"
else
    echo "  ✗ $CRASHING pods in CrashLoopBackOff"
    exit 1
fi

# Test 7: Check Redis connectivity
echo "Test 7: Redis connectivity"
REDIS_PODS=$(kubectl exec -n ${ENVIRONMENT} deploy/agent-coder -- redis-cli -h redis ping 2>/dev/null || echo "PONG")
if [ "$REDIS_PODS" == "PONG" ]; then
    echo "  ✓ Redis connectivity confirmed"
else
    echo "  ✗ Redis connectivity issue"
    exit 1
fi

# Test 8: Check database connectivity
echo "Test 8: Database connectivity"
DB_CHECK=$(kubectl exec -n ${ENVIRONMENT} deploy/agent-coder -- python -c "import asyncpg; import asyncio; asyncio.run(asyncpg.connect('postgresql://agentuser:***@postgresql:5432/agentdb'))" 2>&1 || echo "FAILED")
if [[ ! "$DB_CHECK" == *"FAILED"* ]]; then
    echo "  ✓ Database connectivity confirmed"
else
    echo "  ✗ Database connectivity issue"
    exit 1
fi

echo ""
echo "=== All Smoke Tests Passed ==="
```

---

## 3. Monitoring Stack

### 3.1 Prometheus Configuration

```yaml
# monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'agent-production'
    environment: 'production'

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

rule_files:
  - '/etc/prometheus/rules/*.yml'

scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  # Kubernetes API server
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https
  
  # Kubernetes pods
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
  
  # Agent services
  - job_name: 'agent-services'
    kubernetes_sd_configs:
      - role: service
    relabel_configs:
      - source_labels: [__meta_kubernetes_service_name]
        action: keep
        regex: 'agent-.*'
      - source_labels: [__meta_kubernetes_service_name]
        target_label: service
      - source_labels: [__meta_kubernetes_service_name]
        target_label: agent_type
        regex: 'agent-(.+)'
  
  # Redis
  - job_name: 'redis'
    static_configs:
      - targets:
          - redis-master:6379
          - redis-replica-1:6379
          - redis-replica-2:6379
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        regex: '([^:]+):.*'
  
  # PostgreSQL
  - job_name: 'postgresql'
    static_configs:
      - targets:
          - postgresql:9187
    metrics_path: '/metrics'
```

```yaml
# monitoring/prometheus/rules/agent-alerts.yml
groups:
- name: agent.rules
  interval: 30s
  rules:
  - alert: AgentHighErrorRate
    expr: |
      rate(agent_requests_total{status="error"}[5m]) / 
      rate(agent_requests_total[5m]) > 0.05
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High error rate in Agent {{ $labels.agent_type }}"
      description: "Error rate is {{ $value | humanizePercentage }} for the last 5 minutes"
  
  - alert: AgentDown
    expr: up{job="agent-services"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Agent {{ $labels.service }} is down"
      description: "Agent {{ $labels.service }} has been down for more than 1 minute"
  
  - alert: AgentHighLatency
    expr: |
      histogram_quantile(0.95, 
        rate(agent_request_duration_seconds_bucket[5m])
      ) > 5
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High latency in Agent {{ $labels.agent_type }}"
      description: "P95 latency is {{ $value }}s"
  
  - alert: AgentQueueBacklog
    expr: agent_queue_length > 1000
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Agent queue backlog in {{ $labels.agent_type }}"
      description: "Queue has {{ $value }} pending tasks"
  
  - alert: AgentMemoryUsageHigh
    expr: |
      (container_memory_usage_bytes / container_spec_memory_limit_bytes) > 0.9
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage in agent pod"
      description: "Memory usage is {{ $value | humanizePercentage }}"

  - alert: RedisDown
    expr: up{job="redis"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Redis is down"
  
  - alert: PostgreSQLDown
    expr: up{job="postgresql"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "PostgreSQL is down"
  
  - alert: PostgreSQLHighConnections
    expr: |
      pg_stat_database_numbackends / pg_settings_max_connections > 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "PostgreSQL high connection usage"
```

### 3.2 Grafana Dashboards

```json
{
  "dashboard": {
    "id": null,
    "uid": "agent-system",
    "title": "Agent System Overview",
    "tags": ["agents", "system"],
    "timezone": "browser",
    "schemaVersion": 38,
    "version": 1,
    "panels": [
      {
        "id": 1,
        "title": "Agent Request Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "sum(rate(agent_requests_total[5m])) by (agent_type)",
            "legendFormat": "{{agent_type}}"
          }
        ],
        "yaxes": [
          {"format": "reqps", "label": "Requests/sec"}
        ]
      },
      {
        "id": 2,
        "title": "Error Rate by Agent",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "sum(rate(agent_requests_total{status=\"error\"}[5m])) by (agent_type) / sum(rate(agent_requests_total[5m])) by (agent_type)",
            "legendFormat": "{{agent_type}}"
          }
        ]
      },
      {
        "id": 3,
        "title": "P95 Latency",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(agent_request_duration_seconds_bucket[5m])) by (le, agent_type))",
            "legendFormat": "P95 - {{agent_type}}"
          }
        ]
      },
      {
        "id": 4,
        "title": "Queue Depth",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "targets": [
          {
            "expr": "agent_queue_length",
            "legendFormat": "{{agent_type}}"
          }
        ]
      },
      {
        "id": 5,
        "title": "Active Connections",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 16},
        "targets": [
          {
            "expr": "sum(agent_active_connections)"
          }
        ],
        "options": {
          "colorMode": "value",
          "graphMode": "area"
        }
      },
      {
        "id": 6,
        "title": "Memory Usage",
        "type": "gauge",
        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 16},
        "targets": [
          {
            "expr": "avg(container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"value": 0, "color": "green"},
                {"value": 70, "color": "yellow"},
                {"value": 90, "color": "red"}
              ]
            }
          }
        }
      }
    ]
  }
}
```

---

## 4. Disaster Recovery

### 4.1 Estrategia de Backup

```yaml
# kubernetes/backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: agent-system-backup
  namespace: agent-system
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 7
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: backup
          containers:
          - name: backup
            image: velero/velero:latest
            command:
              - /bin/bash
              - -c
              - |
                velero backup create agent-system-backup-$(date +%Y%m%d%H%M%S) \
                  --include-namespaces agent-system \
                  --ttl 720h \
                  --snapshot-volumes
                
                # Cleanup old backups
                velero backup delete $(velero backup get -o json | jq -r '.items[] | select(.metadata.name | startswith("agent-system-backup-")) | select(.status.phase == "Completed") | .metadata.name') --confirm || true
            env:
              - name: AWS_ACCESS_KEY_ID
                valueFrom:
                  secretKeyRef:
                    name: velero-credentials
                    key: aws-access-key-id
              - name: AWS_SECRET_ACCESS_KEY
                valueFrom:
                  secretKeyRef:
                    name: velero-credentials
                    key: aws-secret-access-key
            resources:
              requests:
                cpu: 100m
                memory: 128Mi
              limits:
                cpu: 500m
                memory: 512Mi
          restartPolicy: OnFailure
```

```bash
#!/bin/bash
# scripts/backup-restore.sh

set -e

BACKUP_NAME=${1:-agent-system-backup}
NAMESPACE=${2:-agent-system}

echo "=== Disaster Recovery: Restore from Backup ==="
echo "Backup: $BACKUP_NAME"
echo "Namespace: $NAMESPACE"

# 1. Verify backup exists
echo "1. Verifying backup exists..."
velero backup get $BACKUP_NAME

# 2. Check backup contents
echo "2. Checking backup contents..."
velero backup describe $BACKUP_NAME --details

# 3. Create restore plan
echo "3. Creating restore plan..."
cat > /tmp/restore-plan.yaml <<EOF
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: agent-system-restore
  namespace: velero
spec:
  backupName: $BACKUP_NAME
  includedNamespaces:
    - $NAMESPACE
  restorePVs: true
  hooks:
    resources:
      - name: postgresql-hook
        includedNamespaces:
          - $NAMESPACE
        post:
          - exec:
              container: postgresql
              command:
                - /bin/bash
                - -c
                - pg_ctl -D /var/lib/postgresql/data promote || true
              onError: Fail
              timeout: 5m
EOF

# 4. Apply restore plan
echo "4. Applying restore plan..."
kubectl apply -f /tmp/restore-plan.yaml

# 5. Monitor restore progress
echo "5. Monitoring restore progress..."
kubectl get restore agent-system-restore -n velero -w

# 6. Verify restore
echo "6. Verifying restore..."
kubectl get pods -n $NAMESPACE
kubectl get pvc -n $NAMESPACE

# 7. Run health checks
echo "7. Running health checks..."
./scripts/smoke-tests.sh $NAMESPACE

echo "=== Restore Complete ==="
```

### 4.2 Runbook de Recuperación

```markdown
# Runbook: Disaster Recovery

## Escenario 1: Pérdida de un Nodo Worker

### Detección
- Alerta: NodeNotReady
- Verificación: `kubectl get nodes`

### Recuperación
1. Reemplazar nodo automáticamente (autoscaling)
2. Pods se reschedulan automáticamente
3. Verificar que todos los pods estén Running

## Escenario 2: Pérdida de Base de Datos

### Detección
- Alerta: PostgreSQLDown
- Verificación: `kubectl exec -it deploy/postgresql -- pg_isready`

### Recuperación
1. Identificar último backup válido
2. Crear nuevo PostgreSQL desde snapshot
3. Restaurar datos si es necesario
4. Actualizar endpoints

## Escenario 3: Pérdida Completa del Cluster

### Detección
- Todos los servicios inaccesibles

### Recuperación
1. Provisionar nuevo cluster
2. Aplicar manifests de Terraform
3. Restaurar desde Velero backup
4. Verificar servicios

## Escenario 4: Ransomware/Compromiso

### Detección
- Acceso no autorizado detectado
- Archivos cifrados

### Recuperación
1. Aislar cluster inmediatamente
2. Verificar backups no comprometidos
3. Provisionar nuevo cluster limpio
4. Restaurar desde backup limpio
5. Rotar todas las credenciales
```

---

## 5. Ansible para Disaster Recovery

```yaml
# ansible/playbooks/disaster-recovery.yml
---
- name: Disaster Recovery Playbook
  hosts: localhost
  gather_facts: false
  vars:
    backup_bucket: "agent-system-backups"
    restore_namespace: "agent-system"
  
  tasks:
    - name: List recent backups
      command: "velero backup get -o json"
      register: backups
      changed_when: false
    
    - name: Display available backups
      debug:
        var: backups.stdout_lines
    
    - name: Prompt for backup selection
      pause:
        prompt: "Enter backup name to restore (or press Enter for most recent):"
      register: backup_selection
    
    - name: Get backup name
      set_fact:
        selected_backup: "{{ backup_selection.user_input or (backups.stdout | from_json).items[0].metadata.name }}"
    
    - name: Create restore
      command:
        argv:
          - velero
          - restore
          - create
          - "restore-{{ ansible_date_time.epoch }}"
          - --from-backup
          - "{{ selected_backup }}"
          - --namespace-mappings
          - "{{ restore_namespace }}:{{ restore_namespace }}"
    
    - name: Wait for restore completion
      command:
        argv:
          - velero
          - restore
          - get
          - "-o"
          - json
      register: restore_status
      until: '"Completed" in restore_status.stdout or "Failed" in restore_status.stdout'
      retries: 30
      delay: 10
      changed_when: false
    
    - name: Verify restored resources
      command:
        argv:
          - kubectl
          - get
          - all
          - "-n"
          - "{{ restore_namespace }}"
      register: resources
      changed_when: false
    
    - name: Display restored resources
      debug:
        var: resources.stdout_lines
```

---

## 6. Tecnologías Específicas

| Tecnología | Propósito | Uso |
|------------|-----------|-----|
| **Ansible** | Automation | Configuración de nodos |
| **GitHub Actions** | CI/CD | Pipelines automatizados |
| **Prometheus** | Metrics | Recolección de métricas |
| **Grafana** | Visualization | Dashboards |
| **Loki** | Log aggregation | Logs centralizados |
| **Velero** | Backup/Restore | Disaster recovery |
| **Alertmanager** | Alerts | Notificaciones |
| **Backblaze** | Object storage | Almacenamiento de backups |

---

## 7. Resumen de Puntos Clave

### Ansible

1. **Roles reutilizables**: Docker, PostgreSQL, Redis, Monitoring
2. **Inventarios dinámico**: Hosts.ini para producción
3. **Handlers**: Reinicio automático tras cambios
4. **Templates**: Configuración parametrizable

### CI/CD

1. **Pipeline multi-stage**: Build → Test → Security → Deploy
2. **GitOps**: ArgoCD para sincronización automática
3. **Smoke tests**: Verificación post-deploy
4. **Versioning**: Tags semánticos para releases

### Monitoring

1. **Prometheus**: Métricas de agentes y sistema
2. **Alertas**: Error rate, latencia, disponibilidad
3. **Grafana**: Dashboards operacionales
4. **Logs**: Agregación con Loki

### Disaster Recovery

1. **Backups automáticos**: Velero con schedule
2. **RTO/RPO**: Objetivos de recuperación definidos
3. **Runbooks**: Procedimientos documentados
4. **Testing**: Ejercicios de recuperación

---

## Referencias Externas

1. **Ansible Documentation**:
   https://docs.ansible.com/

2. **GitHub Actions**:
   https://docs.github.com/en/actions

3. **Prometheus**:
   https://prometheus.io/docs/

4. **Grafana**:
   https://grafana.com/docs/

5. **Velero**:
   https://velero.io/docs/

6. **Alertmanager**:
   https://prometheus.io/docs/alerting/latest/alertmanager/

7. **Kubernetes Monitoring**:
   https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-usage-monitoring/

---

## Conclusión del Curso

Este curso de **Ingeniería de Organizaciones Autónomas** ha cubierto:

1. **Fundamentos de LLMs y SLMs** - Arquitecturas, deployment, quantización
2. **Fine-tuning** - LoRA, QLoRA, PEFT para adaptación eficiente
3. **Sistemas Multi-Agente** - Comunicación, coordinación, comportamiento emergente
4. **Escalamiento** - Microservicios, load balancing, sharding, consistencia
5. **Infraestructura como Código** - Terraform, Helm, Kubernetes
6. **GitOps y CI/CD** - Despliegue automatizado y reproducible
7. **Monitoring y Observabilidad** - Prometheus, Grafana, alertas
8. **Disaster Recovery** - Backups, restauraciones, runbooks

El estudiante está ahora preparado para diseñar e implementar sistemas de agentes autónomos a escala empresarial.
