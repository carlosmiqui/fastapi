from fastapi import FastAPI, Depends
from utils import commom_verificacao_api_token
from routers import llm_router, operacoes_router


description = """
    API desenvolvida durante a aula 2, contendo endpoints de exemplo e soma

    - /teste: retorna uma mensagem de sucesso
    - /soma/numero1/numero2: recebe dois números e retorna a soma
"""


app = FastAPI(
    title="API da Aula 3",
    description="API desenvolvida durante a aula 2, contendo endpoints de exemplo e soma",
    version="0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Carlos Miqui",
        "url": "http://github.com/carlosmiqui/",
        "email": "carlosmiqui@discente.ufg.br",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    dependencies=[Depends(commom_verificacao_api_token)]
) #dependencias globais - usar API_TOKEN - para todos os endpoints




app.include_router(llm_router.router, prefix="/llm")
app.include_router(operacoes_router.router, prefix="/operacoes")
