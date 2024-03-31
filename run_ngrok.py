from pyngrok import ngrok

ngrok.kill()
auth_token = '2eKiVWV4iCYpqt1kM1Ln8R79t8N_3VptBx7rCdpgsZg6sihWA' # https://dashboard.ngrok.com/get-started/your-authtoken
ngrok.set_auth_token(auth_token)

ngrok.connect(7000)