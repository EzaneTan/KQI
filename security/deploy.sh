KQI/security/deploy.sh
```bash
#!/usr/bin/env bash
set -euo pipefail

# 1) Fetch secrets from Vault
VAULT_ADDR=${VAULT_ADDR:-'http://127.0.0.1:8200'}
VAULT_ROLE=${VAULT_ROLE:-'kqi-deployer'}
VAULT_SECRET_PATH="secret/data/kqi/deployer"
echo "🔐 Authenticating to Vault..."
VAULT_TOKEN=$(vault login -method=approle -role="$VAULT_ROLE" -field=token)
API_KEY=$(vault kv get -field=api_key "$VAULT_SECRET_PATH")
WALLET_KEY=$(vault kv get -field=wallet_key "$VAULT_SECRET_PATH")

export KQI_API_KEY="$API_KEY"
export KQI_WALLET_KEY="$WALLET_KEY"

# 2) OPA policy check
echo "🛡️ Running OPA policy guard..."
echo "{\"user_role\": \"${USER_ROLE:-operator}\", \"action\": \"deploy\"}" > /tmp/opa_input.json
if ! opa eval --data policies/permissions.rego --input /tmp/opa_input.json "data.kqi.security.allow" -q | grep -q "true"; then
  echo "❌ Deployment blocked by policy."
  exit 1
fi

# 3) Perform deployment
echo "🚀 Deploying KQI platform..."
kubectl apply -f ../k8s/deployment.yaml
kubectl rollout status deployment/kqi-platform

echo "✅ Deployment complete!"
