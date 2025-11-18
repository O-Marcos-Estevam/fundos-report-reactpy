# Como Configurar Banco SQLite no Railway

O Railway não suporta Git LFS para arquivos grandes (408 MB). Você precisa hospedar o banco SQLite externamente e configurar download automático.

## Opção 1: GitHub Releases (Recomendado - Gratuito)

1. **Criar uma Release no GitHub:**
   ```bash
   cd c:\bloko\...\fundos_report_reactpy

   # Criar tag
   git tag v1.0-database
   git push origin v1.0-database
   ```

2. **Upload do arquivo:**
   - Acesse: https://github.com/SEU-USER/fundos-report-reactpy/releases/new
   - Tag: `v1.0-database`
   - Title: `Database v1.0 - Dados Reais`
   - Arrastar arquivo: `data/fundos_v2.db` (408 MB)
   - Publish release

3. **Copiar URL do arquivo:**
   - Após publicar, clique direito no link do arquivo
   - Copiar endereço (exemplo):
     ```
     https://github.com/SEU-USER/fundos-report-reactpy/releases/download/v1.0-database/fundos_v2.db
     ```

4. **Configurar no Railway:**
   - Railway Dashboard → Seu Projeto → Variables
   - Adicionar: `DATABASE_URL` = `https://github.com/.../fundos_v2.db`
   - Redeploy

## Opção 2: Dropbox

1. Upload do arquivo para Dropbox
2. Gerar link compartilhado
3. Modificar URL: `www.dropbox.com` → `dl.dropboxusercontent.com`
4. Configurar `DATABASE_URL` no Railway

## Opção 3: Google Drive

1. Upload do arquivo
2. Tornar público
3. Usar link direto (não o de compartilhamento)
4. Configurar `DATABASE_URL` no Railway

## Verificar se funcionou

Após configurar, os logs do build devem mostrar:
```
[1] Baixando banco de dados de: https://...
[DOWNLOAD] 100% (408.2 MB)
[3] Download concluído: 408.18 MB
[4] Banco válido com 39 tabelas
[OK] Banco de dados funcionando com dados REAIS!
```

## Modo Fallback

Se não configurar `DATABASE_URL`, o sistema automaticamente usa **modo DEMO** com dados de exemplo.
