from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# Connection ID for connectionRoles
CONNECTION_ID = os.environ.get("OMNI_CONNECTION_ID", "66d0e61f-d910-4fa4-80b6-f52a0fa798d0")

# Configurable placeholder params for OmniApp API
OMNIAPP_PARAMS_1 = {
    "contentPath": "/dashboards/nyc-311",
    "externalId": "smalldatasf@omni.co",
    "name": "Small Data SF",
    "secret": os.environ.get("OMNI_EMBED_SECRET", "your_omniapp_embed_secret_here"),  # Fallback for local dev
    "customThemeId": "97216b2d-0970-4582-aaa6-aa66f082cfe9",
    "connectionRoles": json.dumps({CONNECTION_ID: "RESTRICTED_QUERIER"}),
    # "userAttributes": "%7B%22shop_id%22%3A%22123%22%7D",  # URL-encoded JSON: {"shop_id":"123"}
}

OMNIAPP_PARAMS_2 = {
    "contentPath": "/dashboards/nyc-rideshare",
    "externalId": "smalldatasf@omni.co",
    "name": "Small Data SF",
    "secret": os.environ.get("OMNI_EMBED_SECRET", "your_omniapp_embed_secret_here"),  # Fallback for local dev
    "customThemeId": "8e2a99c1-89e9-428e-8a8c-436e1e22cf06",
    "connectionRoles": json.dumps({CONNECTION_ID: "RESTRICTED_QUERIER"}),
    # "userAttributes": "%7B%22shop_id%22%3A%22123%22%7D",  # URL-encoded JSON: {"shop_id":"123"}
}

OMNIAPP_PARAMS_3 = {
    "contentPath": "/chat",
    "externalId": "smalldatasf@omni.co",
    "name": "Small Data SF",
    "secret": os.environ.get("OMNI_EMBED_SECRET", "your_omniapp_embed_secret_here"),  # Fallback for local dev
    "connectionRoles": json.dumps({CONNECTION_ID: "RESTRICTED_QUERIER"}),
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
    elif view == '7':
        content = 'Sidebar Option 7 Content'
    elif view == '8':
        content = 'Sidebar Option 8 Content'
    # By default content = '' (blank div)
    return render_template('dashboard.html', content=content)

@app.route('/api/content')
def api_content():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    view = request.args.get('view', '')

    if view == '1':
        try:
            resp = requests.post('https://becca-embed.omniapp.co/embed/sso/generate-url', json=OMNIAPP_PARAMS_1)
            if resp.ok:
                try:
                    data = resp.json()
                    if 'url' in data and isinstance(data['url'], str) and data['url'].startswith('http'):
                        return jsonify({'iframe': True, 'url': data['url']})
                    else:
                        return jsonify({'content': ''}), 502
                except (ValueError, KeyError):
                    return jsonify({'content': ''}), 502
            else:
                return jsonify({'content': ''}), 502
        except Exception:
            return jsonify({'content': ''}), 500
    elif view == '2':
        try:
            resp = requests.post('https://becca-embed.omniapp.co/embed/sso/generate-url', json=OMNIAPP_PARAMS_2)
            if resp.ok:
                try:
                    data = resp.json()
                    if 'url' in data and isinstance(data['url'], str) and data['url'].startswith('http'):
                        return jsonify({'iframe': True, 'url': data['url']})
                    else:
                        return jsonify({'content': ''}), 502
                except (ValueError, KeyError):
                    return jsonify({'content': ''}), 502
            else:
                return jsonify({'content': ''}), 502
        except Exception:
            return jsonify({'content': ''}), 500
    elif view == '3':
        try:
            resp = requests.post('https://becca-embed.omniapp.co/embed/sso/generate-url', json=OMNIAPP_PARAMS_3)
            if resp.ok:
                try:
                    data = resp.json()
                    if 'url' in data and isinstance(data['url'], str) and data['url'].startswith('http'):
                        return jsonify({'iframe': True, 'url': data['url']})
                    else:
                        return jsonify({'content': ''}), 502
                except (ValueError, KeyError):
                    return jsonify({'content': ''}), 502
            else:
                return jsonify({'content': ''}), 502
        except Exception:
            return jsonify({'content': ''}), 500
    elif view == '4':
        return jsonify({'iframe': True, 'url': 'https://docs.omni.co/docs/connections/database/motherduck'})
    elif view == '5':
        return jsonify({'iframe': True, 'url': 'https://docs.omni.co/docs/ai'}) 
    elif view == '6':
         return jsonify({'iframe': True, 'url': 'https://docs.omni.co/docs/embed/external-embedding/setting-up-the-infrastructure'})
    elif view == '7':
         return jsonify({'content': '<div class="blobbies-content"><h1>💻 GitHub Repositories</h1><div class="repo-links"><div class="repo-item"><h2>👋 All The Blobbies</h2><p>Check out the amazing 200+ Blobby project on GitHub!</p><a href="https://github.com/RichardCzechowski/all-the-blobbies/tree/main/blobbies-slack" target="_blank" class="blobbies-link">View Blobbies on GitHub →</a></div><div class="repo-item"><h2>🎨 Themes & Chart Palettes</h2><p>Repository containing Dashboard Themes and Chart Palettes</p><a href="https://github.com/becca-omni/themes-and-chart-palettes" target="_blank" class="blobbies-link">View Repo on GitHub →</a></div><div class="repo-item"><h2>🚀 Small Data SF</h2><p>Code used to deploy the app we\'re using for the session</p><a href="https://github.com/becca-omni/small-data-sf" target="_blank" class="blobbies-link">View Repo on GitHub →</a></div></div></div>'})
    elif view == '8':
        return jsonify({'iframe': True, 'url': 'https://docs.google.com/presentation/d/160T_OU-vHXqBywDrxz7qwDhZ9F_l3ijxExqKyvp_tQc/edit?usp=sharing'})
    elif view == '9':
        return jsonify({'iframe': True, 'url': 'https://forms.gle/jSvvndqZz9TqMpNs6'})
    else:
        return jsonify({'content': ''})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Production configuration for Render
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
