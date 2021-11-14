# docker run -p 9000:8080 -v $(pwd)/$LAMBDA_TASK_ROOT dou-scraper
# curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
#|-----------------------------------------||-----------------------------------------|
FROM amazon/aws-lambda-python

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

WORKDIR ${LAMBDA_TASK_ROOT}

RUN  pip3 install -r requirements.txt --target .


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ] 


