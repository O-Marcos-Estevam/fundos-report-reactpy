# Script para copiar módulos V4/V5/V6 para o projeto ReactPy

$origem = "c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\0. Python"
$destino = "c:\bloko\Fundos - Documentos\00. Monitoramento\01. Rotinas\02. Dev\fundos_report_reactpy\modules"

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host " Copiando Módulos V4/V5/V6" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# V4
Write-Host "V4 - Copiando arquivos..." -ForegroundColor Green
Copy-Item "$origem\Relatório_Fundos_V4.py" -Destination "$destino\v4\" -Force
Write-Host "  ✓ Relatório_Fundos_V4.py" -ForegroundColor Gray

# V5
Write-Host "V5 - Copiando arquivos..." -ForegroundColor Green
Copy-Item "$origem\Relatório_Fundos_V5_Enhanced.py" -Destination "$destino\v5\" -Force
Write-Host "  ✓ Relatório_Fundos_V5_Enhanced.py" -ForegroundColor Gray

# V6
Write-Host "V6 - Copiando arquivos..." -ForegroundColor Green
Copy-Item "$origem\Relatório_Fundos_V6_Optimized.py" -Destination "$destino\v6\" -Force
Copy-Item "$origem\database_manager_v6.py" -Destination "$destino\v6\" -Force
Copy-Item "$origem\analytics_engine_v6.py" -Destination "$destino\v6\" -Force
Write-Host "  ✓ Relatório_Fundos_V6_Optimized.py" -ForegroundColor Gray
Write-Host "  ✓ database_manager_v6.py" -ForegroundColor Gray
Write-Host "  ✓ analytics_engine_v6.py" -ForegroundColor Gray

# Verificar
Write-Host ""
Write-Host "Verificando arquivos copiados:" -ForegroundColor Yellow
Write-Host ""
Write-Host "V4:" -ForegroundColor Cyan
Get-ChildItem "$destino\v4\*.py" | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Gray }
Write-Host ""
Write-Host "V5:" -ForegroundColor Cyan
Get-ChildItem "$destino\v5\*.py" | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Gray }
Write-Host ""
Write-Host "V6:" -ForegroundColor Cyan
Get-ChildItem "$destino\v6\*.py" | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Gray }

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host " ✓ Cópia concluída com sucesso!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Yellow
Write-Host "  1. git add modules/" -ForegroundColor Gray
Write-Host "  2. git commit -m 'Add real V4/V5/V6 modules'" -ForegroundColor Gray
Write-Host "  3. git push" -ForegroundColor Gray
Write-Host ""
