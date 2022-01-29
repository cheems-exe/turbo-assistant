import os
import zipfile
from glob import glob

import torch
from django.http.response import JsonResponse
from django.shortcuts import render


def text_summarizer(text):
    # do something
    return text


def speech_to_text(request):
    if request.method == 'POST':
        print(request.POST)
        device = torch.device('cpu')
        model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_stt', language='en', device=device)
        (read_batch, split_into_batches, read_audio, prepare_model_input) = utils
        # os.save()

        test_file = glob(request.FILES['sound'])  # path/name of the audio file should be there!
        print(request.FILES, request.FILES['sound'])

        batches = split_into_batches(test_file, batch_size=10)

        input_to_the_model = prepare_model_input(read_batch(batches[0]), device=device)

        output = model(input)
        transcribed_text = ""
        for example in output:
            transcribed_text = decoder(example.cpu())

        print("transcribed_text: ", transcribed_text)

        summarized_text = text_summarizer(transcribed_text)

        return JsonResponse({"summarized_text": summarized_text})

    return render(request, "app/text_summarizing.html")
