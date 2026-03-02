del /q dist\*.*
uv build
if .%UV_PUBLISH_TOKEN%. == .. ( echo UV_PUBLISH_TOKEN not set, exit. & exit /b 1)
uv publish