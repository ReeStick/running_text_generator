from pyngrok import ngrok

ngrok.kill()

# ngrok config add-authtoken <token> 
# https://dashboard.ngrok.com/get-started/your-authtoken

print(ngrok.connect(7000))