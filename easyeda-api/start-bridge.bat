@echo off
title EasyEDA Bridge Server
cd /d "%~dp0"
echo 正在启动 EasyEDA Bridge 服务...
node scripts/bridge-server.mjs
pause
