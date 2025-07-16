aws cloudformation deploy \
    --template-file full-env.yaml \
    --stack-name production-env \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
    --parameter-overrides \
    KeyName=my-key \
    CertificateArn=arn:aws:acm:... \
    DomainName=app.example.com
