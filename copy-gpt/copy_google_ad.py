import openai

def generate_google_ads(client_name, client_info, model='text-davinci-002', temperature=0.7, n=1):
    filepath = 'examples/google_ad_examples.txt'
    google_ads = open(f'{filepath}','r').read()
    promptstring = f"""
        The following are examples of Google ads.

        {google_ads}

        The following is information about {client_name}.

        {client_info}

        Create a google ad for {client_name}.
    """
    resp = openai.Completion.create(model=model, temperature=temperature, prompt=promptstring, n=n)
    choices = []
    for choice in resp['choices']:
        choices.append(choice['text'].strip().split('\n')[0])
    return choices

if __name__ == '__main__':
    client_name = 'pelton-shepherd'
    client_info = open(f'leads/{client_name}.txt','r', encoding='utf8').read()
    choices = generate_google_ads(client_name, client_info, n=5)
    print(choices)