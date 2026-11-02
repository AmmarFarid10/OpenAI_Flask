# Credential remediation
A credential-shaped literal was removed from app.py. Treat the previously published value as compromised: revoke it in the provider console and inspect usage. No credential was tested. History still contains the old value; coordinate history remediation separately. This application also uses a legacy completions integration and is not deployment-ready.
