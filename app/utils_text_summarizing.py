import os
from glob import glob

import torch
from django.http.response import JsonResponse
from django.core.files.storage import default_storage
from django.shortcuts import render
import requests


def text_summarizer(text):
    print(text)

    url = "https://text-analysis12.p.rapidapi.com/summarize-text/api/v1.1"

    payload = "{\r\n    \"language\": \"english\",\r\n    \"summary_percent\": 10,\r\n    \"text\":" + text + "\r\n}"
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': "8e6fb730b6mshd2d435403413191p1f0308jsn3fce5bdcbc52"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text

def speech_to_text(request):
    if request.method == 'POST':
        print(request.POST)
        device = torch.device('cpu')
        model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_stt', language='en', device=device)
        (read_batch, split_into_batches, read_audio, prepare_model_input) = utils
        # os.save()

        file = request.FILES['sound']
        file_name = default_storage.save(file.name, file)
        print("Saved", os.getcwd())
        print("Hellooooo", os.path.join(os.getcwd(), f"media\\{file_name}"))

        file_path = os.path.join(os.getcwd(), f"media\\{file_name}")
        test_file = glob(file_path) 
        print('HERE', test_file)

        batches = split_into_batches(test_file, batch_size=10)

        input_to_the_model = prepare_model_input(read_batch(batches[0]), device=device)

        output = model(input_to_the_model)
        transcribed_text = ""
        for example in output:
            transcribed_text = decoder(example.cpu())

        os.remove(file_path)
        return render(request, "app/text_summarizing.html",{"summarized_text": transcribed_text})

    return render(request, "app/text_summarizing.html",{"summarized_text": ""})
