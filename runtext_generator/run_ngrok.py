from pyngrok import ngrok

ngrok.kill()
# получаем токен https://dashboard.ngrok.com/get-started/your-authtoken
auth_token = "2eYFitCm5eCjF2yuZXvhLq3PX5B_4uUfZ7CaLs78pARJ3kkUh"
ngrok.set_auth_token(auth_token)
ngstart = ngrok.connect(7000)
print(ngstart)