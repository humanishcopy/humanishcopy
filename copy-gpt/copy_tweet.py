import openai

def generate_company_tweets(client_name, client_info, model='text-davinci-002', temperature=0.7, n=1):
    filepath = 'examples/company_tweets.txt'
    company_tweets = open(f'{filepath}','r').read()

    promptstring = f"""
    The following is information about {client_name}.

    {client_info}

    think of a tweet that  {client_name} could post on twitter.com.
    """
    resp = openai.Completion.create(model=model, temperature=temperature, prompt=promptstring, n=n)
    choices = []
    for choice in resp['choices']:
        tweet = choice['text']
        if choice['finish_reason'] == 'length':
            tweet = finish_thought(promptstring + tweet, len(promptstring))
        choices.append(tweet.strip())
    return choices

def finish_thought(thought, len_orig_prompt):
    response = openai.Completion.create(model='text-davinci-002', temperature=0.7, prompt=thought, n=1)
    choice = response['choices'][0]
    if choice['finish_reason'] == 'length':
        return finish_thought(thought + choice['text'],len_orig_prompt)
    else:
        full_text = thought+choice['text']
        return full_text[len_orig_prompt-1:]

if __name__ == '__main__':
    client_name = 'pelton-shepherd'
    client_info = open(f'leads/{client_name}.txt','r', encoding='utf8').read()
    choices = generate_company_tweets(client_name, client_info, n=5)
    print(choices)
