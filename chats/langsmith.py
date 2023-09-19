from langchain.callbacks import LangChainTracer
from langchain.chat_models import ChatOpenAI
from langsmith import Client
from langchain import hub

obj = hub.pull("homanp/superagent")


callbacks = [
  LangChainTracer(
    project_name="Bookchat",
    client=Client(
      api_url="https://api.smith.langchain.com",
      api_key="ls__05051edd570f4bd38a3e08cb578a0ba8"
    )
  )
]

llm = ChatOpenAI(callbacks=callbacks)
llm.invoke("Hello, world!")