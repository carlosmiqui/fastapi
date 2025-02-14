from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from enum import Enum
import logging
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s: %(message)s"
)
logger = logging.getLogger("fastapi")

# logger.info('Mensagem informativa')
# logger.warning('Mensagem de alerta')
# logger.error('Mensagem de erro')
# logger.critical('Mensagem crítica')


API_TOKEN = 123
def commom_verificacao_api_token(api_token: int):
    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
        
    return {"api_token": api_token} #Aparentemente o return nao eh necessario, mas eh bom para documentacao

app = FastAPI(
    title="API da Aula 2",
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


# Definindo os grupos de tags -> opcao 1
NOME_GRUPO_OPERACOES = "Operações matemáticas simples"
NOME_GRUPO_TESTE = "Teste"


# Definindo os grupos de tags -> opcao 2
class NomeGrupo(str, Enum):
    operacoes = "Operações matemáticas simples"
    teste = "Teste"





 
#1o endpoint
@app.get("/teste", 
        summary="Retorna mensagem de teste",
        description="Retorna uma mensagem de exemplo para testar e verificar se deu certo",
        tags=[NomeGrupo.teste, NomeGrupo.operacoes],
        dependencies=[Depends(commom_verificacao_api_token)])
    
def hello_world(): 
    return {"mensagem": " Hello World, mudei minha mensagem"}


#a. Formato 1
# Passando o número 1 e 2 na URL  
@app.post("/V1/soma/{numero1}/{numero2}/{api_token}", tags=[NomeGrupo.operacoes], status_code=status.HTTP_202_ACCEPTED)
def soma(numero1: int, numero2: int, api_token: int):
    
    print(f"Requisição recebida, parâmetros numero1={numero1}, numero2={numero2}") #log 
    logger.info(f"Requisição recebida, parâmetros numero1={numero1}, numero2={numero2}") #log 
    
    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="API Token inválido")
    total = numero1 + numero2

    logger.info("Verificando se algum dos números é negativo") #log
    if numero1 < 0 or numero2 < 0:
        print("Erro: Não é permitido números negativos") #log
        logger.error("Erro: Não é permitido números negativos") #log


        raise HTTPException(status_code=400, detail="Não é permitido números negativos")
    if total < 0:
        print("Erro: Resultado negativo")
        logger.error("Erro: Resultado negativo")
        raise HTTPException(status_code=400, detail="Resultado negativo")
    
    print(f"Requisição processada com sucesso. Resultado: {total}") #log
    logger.info(f"Requisição processada com sucesso. Resultado: {total}") #log
    
    return {"resultado": total, "warning": "Esta versão será descontinuada em 30 dias"}


#a. Formato 2
# Passando o número 1 e 2 no corpo da requisição
@app.post("/V2/soma_formato2", 
        tags=[NomeGrupo.operacoes],
        dependencies=[Depends(commom_verificacao_api_token)])
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


#a. Formato 3
# Passando o número 1 e 2 no corpo da requisição
from pydantic import BaseModel
class Numeros(BaseModel):
    numero1: int
    numero2: int
    numero3: int = 0 # valor default, torna o campo opcional

class Resultado(BaseModel):
    resultado: int
@app.post("/V3/soma_formato3", 
        response_model=Resultado, 
        tags=[NomeGrupo.operacoes],
        dependencies=[Depends(commom_verificacao_api_token)])
def soma_formato3(numeros: Numeros):
    total = numeros.numero1 + numeros.numero2+ numeros.numero3
    return {"resultado": total}

#a. Formato 4
# Passando o número 1 e 2 no corpo da requisição
from pydantic import BaseModel
class Numeros(BaseModel):
    numero1: int
    numero2: int
    #numero3: int = 0 # valor default, torna o campo opcional

class Resultado(BaseModel):
    resultado: int
# para versao apos ja ter publicado um endpoint, acrescentar ao final do endpoint o numero da versao
@app.post("/soma_formato4/V4", 
        tags=[NomeGrupo.operacoes],
        dependencies=[Depends(commom_verificacao_api_token)]) 
def soma_formato4(numeros: Numeros) -> Resultado:
    total = numeros.numero1 + numeros.numero2+ numeros.numero3
    return {"resultado": total}
 

@app.post("/V1/divisao/{numero1}/{numero2}", 
        #dependencies=[Depends(commom_verificacao_api_token)], 
        tags=[NomeGrupo.operacoes])
def divisao(numero1: int, numero2: int, titulo: str):
    if titulo in palavras_proibidas:
        raise HTTPException(status_code=400, detail="Palavra proibida")
    if numero2 == 0 or numero1 == 0:
        raise HTTPException(status_code=400, detail="Não é permitido divisão por zero")

    total = numero1 / numero2

    return {"resultado": total}



class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


@app.post("/V1/operacao", 
        tags=[NomeGrupo.operacoes])
def operacao(numero: Numeros, tipo: TipoOperacao):
    if tipo == TipoOperacao.soma:
        total = numero.numero1 + numero.numero2

    elif tipo == TipoOperacao.subtracao:
        total = numero.numero1 - numero.numero2

    elif tipo == TipoOperacao.multiplicacao:
        total = numero.numero1 * numero.numero2

    elif tipo == TipoOperacao.divisao:
        total = numero.numero1 / numero.numero2

    return {"resultado": total}






# description = """
#     API desenvolvida durante a aula 2, contendo endpoints de exemplo e soma
    
#     - /teste: retorna uma mensagem de sucesso
#     - /soma/numero1/numero2: recebe dois números e retorna a soma
# """

#


# @app.get(
#     "/teste",
#     summary="Retorna mensagem de teste",
#     description="Retorna uma mensagem de exemplo para testar e verificar se deu certo",
#     tags=[NomeGrupo.teste],
# )
# def hello_world():
#     return {"mensagem": "Deu certo"}


# Criando um endpoint para receber dois números e retornar a soma
# @app.post("/soma/{numero1}/{numero2}")#, tags=[NomeGrupo.operacoes])
# def soma(numero1: int, numero2: int):
#     #logger.info(f"Requisição recebida, parâmetros numero1={numero1}, numero2={numero2}")

#     if numero1 < 0 or numero2 < 0:
#         logger.error("Não é permitido números negativos")
#         raise HTTPException(status_code=400, detail="Não é permitido números negativos")

#     total = numero1 + numero2

    # if total < 0:
    #     logger.error("Resultado negativo")
    #     raise HTTPException(status_code=400, detail="Resultado negativo")

    # logger.info(f"Requisição processada com sucesso. Resultado: {total}")

    # return {"resultado": total, "warning": "Esta versão será descontinuada em 30 dias"}


# # Formato 2: recebendo os números no corpor da requisição
# @app.post("/soma/v2", tags=[NomeGrupo.operacoes])
# def soma_formato2(numero1: int, numero2: int):
#     total = numero1 + numero2
#     return {"resultado": total}


# class Numero(BaseModel):
#     numero1: int
#     numero2: int
  

# class Resultado(BaseModel):
#     resultado: int


# @app.post(
#     "/soma/v3",
#     response_model=Resultado,
#     tags=[NomeGrupo.operacoes],
#     status_code=status.HTTP_200_OK,
# )
# def soma_formato3(numero: Numero):
#     total = numero.numero1 + numero.numero2 + numero.numero3
#     return {"resultado": total}


# @app.post("/divisao/{numero1}/{numero2}", tags=[NomeGrupo.operacoes])
# def divisao(numero1: int, numero2: int):
#     if numero2 == 0:
#         raise HTTPException(status_code=400, detail="Não é permitido divisão por zero")

#     total = numero1 / numero2

#     return {"resultado": total}


# # Receber por parâmetro um “tema” de uma história
# # Montar um prompt para que seja gerada uma história com base no tema informado pelo usuário
# # Execute o prompt na OpenAI ou Groq
# # Retorne a resposta para o usuário



def executar_prompt(tema: str):
    """
    Gera uma história em português brasileiro sobre um tema específico usando a API Groq.
    Args:
        tema (str): O tema sobre o qual a história será escrita.
    Returns:
        str: O conteúdo da história gerada pela API Groq.
    """
    prompt = f"Escreva uma história em pt-br sobre o {tema}"

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70B-versatile",
    )

    return chat_completion.choices[0].message.content


@app.post("/gerar_historia")
def gerar_historia(tema: str):
    historia = executar_prompt(tema)

    return {"historia": historia}