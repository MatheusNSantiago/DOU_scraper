#! usr/bin/bash

find . -type f \
    ! -path "./.*/**" \
    ! -path "*/__pycache__/**" \
    ! -path "./tmp/**" \
    ! -path "./lambda_func.zip" \
    ! -path "./main.py" \
    ! -path "./to_lambda.sh" \
    ! -path "./.gitignore" \
    ! -path "./src/database/local_db.py" \
    -print | zip lambda_func.zip -@

aws lambda update-function-code --function-name dou-scraper --region sa-east-1 --zip-file fileb://lambda_func.zip

rm lambda_func.zip

# aws lambda invoke \
#     --function-name dou-scraper \
#     --cli-binary-format raw-in-base64-out \
#     --region sa-east-1 \
#     --payload '{}' output.txt
