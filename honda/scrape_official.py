import requests

models = {
    "Accord": "bd4c8223339741248442409c845041bf?v=d79d57b5&_gl=1*151prcg*_gcl_au*ODYyNTEwNDgzLjE2OTA3OTExMDM.",
    "Civic": "83907bb1a00b4d3b847418db88b5a802?_gl=1*bmysen*_gcl_au*ODYyNTEwNDgzLjE2OTA3OTExMDM.",
    "HR-V": "31a3e0d0b3fa41b598aecf3bc36f264f?_gl=1*c8hjy1*_gcl_au*ODYyNTEwNDgzLjE2OTA3OTExMDM.",
    "CR-V": "aed82176bdc045e9b875c9e22870e1eb?v=980c3292&_gl=1*1dfazr5*_gcl_au*ODYyNTEwNDgzLjE2OTA3OTExMDM.",
    "ZR-V": "3b38b025cb6f4c7c9c0314bc9e473131?v=3d7729fb&_gl=1*hnwb4z*_gcl_au*ODYyNTEwNDgzLjE2OTA3OTExMDM.   ",
    "Civic Type-R": "5b65dc7c943042fd8ebc175314259c06?v=5416e894&_gl=1*1to0bkj*_gcl_au*ODYyNTEwNDgzLjE2OTA3OTExMDM.",
}

for model, model_num in models.items():
    url = f"https://delivery.contenthub.honda.com.au/api/public/content/{model_num}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"2023-Test/Honda-{model}-2023.pdf", "wb") as f:
            f.write(response.content)
        print("PDF Downloaded successfully.")
    else:
        print(f"Failed to download the PDF. Status Code: {response.status_code}")
