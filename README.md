# lindat_client
Example client for Lindat Translator API for LLM-based MT.

Basic translation:
```
echo "This is a test." | python lindat_client.py --src cs --tgt en --base-url "$URL"/api/v2/models 
```

Translation with markup tags handled outside the translation model:
```
echo "This is a test." | python lindat_client.py --src cs --tgt en --tags --base-url "$URL"/api/v2/models                                 
```

Translation of .docx document:
```
python translate_docx.py  --base-url "$URL"/llmtranslate-1/api/v2/models  document.docx
```
Custom prompt (you can use variables {src}, {tgt} and {text}, which are filled into the prompt template on server side):
```
echo "This is a test." | python lindat_client.py --src cs --tgt en --prompt "Translate the following text from {src} into {tgt}, and explain the translation for each word. Source text: {text}" --base-url "$URL"/api/v2/models 

```
