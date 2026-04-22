# README Auto-Update System

## 🚀 Overview

Este sistema automatiza completamente a atualização das seções **Techs** e **Contact-me** no README.md.

- **Seção Techs**: Sincroniza com as linguagens dos seus repositórios públicos no GitHub
- **Seção Contact-me**: Sincroniza com seu arquivo JSON do portfolio

## 📋 Como Funciona

### Seção Techs

1. O script busca todos os seus repositórios públicos via API do GitHub
2. Para cada repositório (excluindo forks), obtém as linguagens usadas
3. Calcula o peso de cada linguagem baseado na quantidade de código
4. Seleciona as 12 linguagens mais usadas
5. Gera badges ordenadas alfabeticamente

### Seção Contact-me

1. O script busca o arquivo JSON do seu portfolio: `https://raw.githubusercontent.com/JLBBARCO/portfolio/main/src/json/areas/contact.json`
2. Para cada contato, extrai: `iconName`, `url`, `name`
3. Mapeia o `iconName` para dados de shield (label, logo, cor)
4. Gera badges com img.shields.io

## ⏰ Atualizações Automáticas

O GitHub Actions irá atualizar automaticamente em:

### 1. **Diariamente** (00:00 UTC)

- Executa automaticamente a cada dia
- Sincroniza novas linguagens usadas
- Atualiza contatos do portfolio

### 2. **Manualmente** (On-Demand)

- Acesse a aba **Actions** do seu repositório
- Clique em "Update README Sections"
- Clique em "Run workflow"

### 3. **Ao fazer push do script** (Trigger)

- Qualquer alteração em `scripts/update_readme_sections.py`
- O workflow executa automaticamente

## 🔧 Script Local

Para executar manualmente no seu computador:

```bash
python scripts/update_readme_sections.py
```

O script irá:

- Buscar dados das APIs
- Atualizar o README.md
- NÃO faz commit automaticamente (você faz via git)

## 📝 Estrutura do JSON de Contato

O arquivo `src/json/areas/contact.json` do seu portfolio deve ter esta estrutura:

```json
{
  "cards": [
    {
      "iconName": "email",
      "url": "mailto:seu-email@example.com",
      "name": "seu-email@example.com"
    },
    {
      "iconName": "github",
      "url": "https://github.com/seu-usuario",
      "name": "GitHub.com/seu-usuario"
    }
  ]
}
```

**Icons suportados:**

- `email` → Gmail
- `github` → GitHub
- `linkedin` → LinkedIn
- `instagram` → Instagram
- `youtube` → YouTube
- `discord` → Discord
- `whatsapp` → WhatsApp

## 🛠️ Personalizando Linguagens

Para adicionar mais linguagens com cores customizadas, edite `LANGUAGE_BADGE_META` em `scripts/update_readme_sections.py`:

```python
LANGUAGE_BADGE_META: Dict[str, Tuple[str, str]] = {
    "YourLanguage": ("logo-name", "HEXCOLOR"),
}
```

## 🛠️ Personalizando Contatos

Para adicionar mais ícones, edite `CONTACT_ICON_TO_SHIELD` em `scripts/update_readme_sections.py`:

```python
CONTACT_ICON_TO_SHIELD = {
    "seu-icon": ("Label", "logo-name", "HEXCOLOR"),
}
```

## ✅ Verificar Status

- Acesse a aba **Actions** do seu repositório
- Veja o histórico de execuções
- Clique em uma execução para ver os logs

## 🔐 Permissões Necessárias

O GitHub Actions precisa de permissão para fazer commit e push. Verifique:

1. Settings > Actions > General
2. Certifique que "Workflow permissions" está com "Read and write permissions"

## 📊 Resultado Final

```markdown
## Techs
<!-- TECHS:START -->
![Language1](...)
![Language2](...)
<!-- TECHS:END -->

## Contact-me
<!-- CONTACT:START -->
[![Gmail](...)](#)
[![GitHub](...)](#)
<!-- CONTACT:END -->
```

Os comentários `<!-- BLOCK:START -->` e `<!-- BLOCK:END -->` marcam as seções gerenciadas automaticamente.

## 🐛 Troubleshooting

**Problema**: Workflow não atualiza

- Solução: Verifique se `permissions.contents` está como `write` em `.github/workflows/update-readme.yml`

**Problema**: Script falha localmente

- Solução: Certifique que tem acesso à API do GitHub (não precisa token para repos públicos)

**Problema**: Linguagens não aparecem

- Solução: Verifique se estão em repositórios públicos e não-forks

**Problema**: Contatos não aparecem

- Solução: Verifique se o JSON do portfolio tem a estrutura correta e o `iconName` está mapeado
