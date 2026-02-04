# 📖 Guia de Uso da API

Este guia descreve como interagir com os recursos do Holocron Engine.

## 🔐 Autenticação
As rotas protegidas exigem o seguinte cabeçalho HTTP:
- **Header:** `X-API-KEY`
- **Valor:** (Solicite sua chave ao administrador ou use a configurada no ambiente)

## 🏎️ Performance e Cache
- **Cache:** As respostas da SWAPI são cacheadas por 24h para garantir latência baixa.
- **Busca Global:** Utiliza processamento paralelo. O tempo de resposta médio é de ~800ms para varredura completa.

## 🗂️ Exemplos de Requisições

### Listar Personagens (Paginado)
`GET /personagens?page=1`

### Busca Global (Protegida)
`GET /busca?q=Skywalker`
*Requer Header de Autenticação.*

---
*Dica: Você pode importar o arquivo `HolocronEngine.postman_collection.json` desta pasta diretamente no seu Postman para testar imediatamente.*