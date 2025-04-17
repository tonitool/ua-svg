from openai import OpenAI

# Replace with your actual API key
client = OpenAI(
    base_url='https://external.api.recraft.ai/v1',
    api_key="UzW7cFWdN3fNPk6nk7Wd3kaBrpPCASpctU6PpYkxiIX4Fo1aayhEBhzsA1iScXDo",
)

# Upload and convert image
response = client.post(
    path='/images/vectorize',
    cast_to=object,
    options={'headers': {'Content-Type': 'multipart/form-data'}},
    files={'file': open('your-image.png', 'rb')}
)

print("SVG URL:", response['image']['url'])

