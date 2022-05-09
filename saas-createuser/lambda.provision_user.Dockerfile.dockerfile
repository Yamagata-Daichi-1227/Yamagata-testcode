FROM public.ecr.aws/lambda/python:3.8

COPY ./requirements.txt ${LAMBDA_TASK_ROOT}
COPY ./src ${LAMBDA_TASK_ROOT}/

RUN yum -y update
RUN pip install -r requirements.txt

CMD ["saas/main.provision_user"]