# Small Data SF Flask App

A Flask application for building an AI Data App!

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your secrets:
   ```bash
   cp .env.example .env
   # Edit .env with your actual secrets
   ```

3. Run the app:
   ```bash
   python app.py
   ```

**Note:** The `.env` file is gitignored and contains your local secrets. Never commit it to GitHub!

## Deploy to Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set these environment variables in Render:
   - `OMNI_EMBED_SECRET`: Your OmniApp embed secret
   - `FLASK_SECRET_KEY`: A random secret key for sessions
   - `FLASK_ENV`: Set to `production`

4. Render will automatically detect the `Procfile` and deploy with gunicorn

## Security Notes

- Never commit secrets to git
- Use environment variables for all sensitive data
- Rotate secrets regularly
- Add your Render domain to OmniApp's authorized origins for iframe embedding
