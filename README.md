# Hello World Motion Lab

A beginner-friendly Streamlit app for styling a name and exploring continuous browser animations.

## Files
- `app.py` — complete self-contained application
- `requirements.txt` — minimal, unpinned dependency list

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Create a GitHub repository, for example `hello-world-motion-lab`.
2. Upload `app.py` and `requirements.txt` to the repository root.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Select **Create app**, choose your repository and branch, and set the main file path to `app.py`.
5. Deploy. Streamlit installs the package listed in `requirements.txt`.

The animations run inside the HTML component's browser frame using `requestAnimationFrame`; the Python script does not repeatedly rerun to animate.
