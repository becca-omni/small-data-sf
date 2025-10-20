from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# Configurable placeholder params for OmniApp API
OMNIAPP_PARAMS_1 = {
    "contentPath": "/dashboards/small-data-sf-yelp",
    "externalId": "smalldatasf@omni.co",
    "name": "Small Data SF",
    "secret": os.environ.get("OMNI_EMBED_SECRET", "your_omniapp_embed_secret_here"),  # Fallback for local dev
    # "userAttributes": "%7B%22shop_id%22%3A%22123%22%7D",  # URL-encoded JSON: {"shop_id":"123"}
}

OMNIAPP_PARAMS_2 = {
    "contentPath": "/dashboards/small-data-sf-nyc-taxi",
    "externalId": "smalldatasf@omni.co",
    "name": "Small Data SF",
    "secret": os.environ.get("OMNI_EMBED_SECRET", "your_omniapp_embed_secret_here"),  # Fallback for local dev
    # "userAttributes": "%7B%22shop_id%22%3A%22123%22%7D",  # URL-encoded JSON: {"shop_id":"123"}
}

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key_here')  # Use env var for production

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'smalldatasf' and password == 'smalldatasf':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Try again.'
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Handle sidebar view
    view = request.args.get('view', '')
    content = ''
    if view == '1':
        content = 'Sidebar Option 1 Content'
    elif view == '2':
        content = 'Sidebar Option 2 Content'
    elif view == '3':
        content = 'Sidebar Option 3 Content'
    elif view == '4':
        content = 'Sidebar Option 4 Content'
    elif view == '5':
        content = 'Sidebar Option 5 Content'
    elif view == '6':
        content = 'Sidebar Option 6 Content'
    # By default content = '' (blank div)
    return render_template('dashboard.html', content=content)

@app.route('/api/content')
def api_content():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    view = request.args.get('view', '')

    if view == '1':
        try:
            resp = requests.post('https://becca.omniapp.co/embed/sso/generate-url', json=OMNIAPP_PARAMS_1)
            if resp.ok:
                data = resp.json()
                if 'url' in data:
                    return jsonify({'iframe': True, 'url': data['url']})
                else:
                    return jsonify({'content': 'No URL found in API response.'}), 502
            else:
                return jsonify({'content': f'Error fetching content from external API. Status: {resp.status_code}'}), 502
        except Exception as e:
            return jsonify({'content': f'API request failed: {str(e)}'}), 500
    elif view == '2':
        try:
            resp = requests.post('https://becca.omniapp.co/embed/sso/generate-url', json=OMNIAPP_PARAMS_2)
            if resp.ok:
                data = resp.json()
                if 'url' in data:
                    return jsonify({'iframe': True, 'url': data['url']})
                else:
                    return jsonify({'content': 'No URL found in API response.'}), 502
            else:
                return jsonify({'content': f'Error fetching content from external API. Status: {resp.status_code}'}), 502
        except Exception as e:
            return jsonify({'content': f'API request failed: {str(e)}'}), 500
    elif view == '3':
        return jsonify({'iframe': True, 'url': 'https://docs.omni.co/docs/ai'})
    elif view == '4':
        return jsonify({'iframe': True, 'url': 'https://docs.omni.co/docs/embed/external-embedding/setting-up-the-infrastructure'})
    elif view == '5':
        return jsonify({'content': '<div class="blobbies-content"><h1>Blobby Repo</h1><p>Check out the amazing 200+ Blobby project on GitHub!</p><a href="https://github.com/RichardCzechowski/all-the-blobbies/tree/main/blobbies-slack" target="_blank" class="blobbies-link">View Blobbies on GitHub →</a></div>'})
    elif view == '6':
        return jsonify({'iframe': True, 'url': 'https://docs.google.com/presentation/d/160T_OU-vHXqBywDrxz7qwDhZ9F_l3ijxExqKyvp_tQc/edit?usp=sharing'})
    else:
        return jsonify({'content': content_map.get(view, '')})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Production configuration for Render
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
