#!/usr/bin/env python

import requests
import json
import sys
from process import json2tab


def get_keywords_stream(auth, keywords, config, output_format, output_file):
    # POST data: list of keywords to search
    data = {
        'track': keywords,
        "language": config['language'],
        'tweet_mode': 'extended'
    }
    response = requests.post(
        config['url_filter'], data=data, auth=auth, stream=True)
    process_response(config, response, output_format, output_file)


def get_sample_stream(auth, config, output_format, output_file):
    response = requests.post(config['url_sample'], auth=auth, stream=True)
    process_response(config, response, output_format, output_file)


def process_response(config, response, output_format, output_file):
    for line in response.iter_lines():
        if line:
            try:
                tweet = json.loads(line)
                if output_format == 'tsv':
                    tweet_tab, _ = json2tab(tweet, config['retweets'])
                    output_file.write(tweet_tab)
                else:
                    output_file.write(json.dumps(tweet))
                    output_file.write('\n')
            except Exception as e:
                sys.stderr.write('error parsing tweet\n\n' + str(e))
