# 1. Initialize
git init

# 2. Configure (first time)
git config --global user.name "Parthiban Kumar"
git config --global user.email "parthiban@email.com"

# 3. Add remote
git remote add origin https://github.com/ParthibanKumar/NYC_TAXI_AZURE_DATABRICKS.git

# 4. Add files
git add .

# 5. Commit
git commit -m "NYC TAXI: Initial upload from Databricks"

# 6. Push
git push -u origin main