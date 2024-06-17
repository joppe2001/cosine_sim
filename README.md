To execute the following steps, open your terminal and navigate to the `backend` directory:

```bash
cd backend
```

Next, install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

Once the dependencies are installed, start the training process by executing the following command:

```bash
python -m training.train
```

To execute the following steps, open your terminal and navigate to the `backend` directory:

```bash
cd backend
```
Next, install the required dependencies by running the following command:
```bash
pip install -r requirements.txt
```
Once the dependencies are installed, start the training process by executing the following command:
```bash
python -m training.train
```

before starting the server make sure that ssl certs are installed either using brew ( macos ) or https://github.com/FiloSottile/mkcert ( windows )
```bash
mkcert localhost # macos
mkcert -install # windows
```

After the training is complete, start the server by running the following command:

```bash
mkcert localhost # ( or mkcert -install for windows )
python -m server.app
```

Then navigate to the /recommend route from the backend server.

Make sure to change the model version in `app.py` if you haven't already. Locate the following lines of code for data loading:

```python
df = load_from_local("models/model1/dataframe.pkl")
cosine_sim = load_from_local("models/model1/cosine_similarity_matrix.pkl")
```

Now, navigate to the `frontend` directory by executing the following command:
```bash
cd ../frontend
```

Run the installer for the packages ( choose one )
```bash
bun install
yarn
npm install
pnpm install
```

Finally, start the development server using your preferred package manager. For example, if you are using `bun`, run the following command:
```bash
bun dev
yarn dev
npm run dev
pnpm run dev
```