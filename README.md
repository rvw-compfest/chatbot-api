## How to run

1. Create conda envs pake python 3.10.12, activate terus install dependencies `pip install -r requirements.txt`

2. Install ollama & pull model

```sh
curl -fsSL https://ollama.com/install.sh | sh

ollama pull aya
```

3. Run populate.ipynb

4. test pake test.ipynb, set `persist_directory` ke direktori db.

## Test API

1. cd ke `./api`

2. Run `flask --app main --debug run` di terminal

3. Send request pake Postman pake question buat bodynya.

```json
{
  "question": "Apa saja hak dan kewenangan dari Komisi Yudisial?"
}
```
