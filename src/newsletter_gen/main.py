#!/usr/bin/env python
from newsletter_gen.crew import NewsletterGenCrew

import os
from pathlib import Path

def load_html_template(): 
    # Get the absolute path to the template
    template_path = Path(__file__).parent / 'config' / 'newsletter_template.html'
    
    # If the template doesn't exist, use test.html as fallback
    if not template_path.exists():
        template_path = Path(os.getcwd()) / 'test.html'
    
    with open(template_path, 'r') as file:
        html_template = file.read()
        
    return html_template


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': input('Enter the topic for your newsletter: '),
        'personal_message': input('Enter a personal message for your newsletter: '),
        'html_template': load_html_template()
    }
    NewsletterGenCrew().crew().kickoff(inputs=inputs)