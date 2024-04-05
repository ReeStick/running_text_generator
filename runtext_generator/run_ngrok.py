from pyngrok import ngrok

ngrok.kill()
# получаем токен https://dashboard.ngrok.com/get-started/your-authtoken
auth_token = ""
ngrok.set_auth_token(auth_token)
ngstart = ngrok.connect(7000)
print(ngstart)