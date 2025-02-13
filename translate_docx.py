#!/usr/bin/env python3
import sys
import argparse
import requests

def translate_file(src_lang, tgt_lang, input_path, model, tags, prompt, base_url):
    """
    Translate the contents of a file using the translation API.

    Parameters:
        src_lang (str): Source language code.
        tgt_lang (str): Target language code.
        input_path (str): Path to the input file.
        model (str): Model identifier.
        tags (bool): Whether to send the file with XML tags.
        prompt (str or None): Optional prompt for the translation.
        base_url (str): Base URL for the translation API.

    Returns:
        bytes: The translated content on success.
    """
    url = f"{base_url}/{model}"

    # Read the file content as binary data.
    try:
        with open(input_path, 'rb') as f:
            content = f.read()
    except Exception as e:
        sys.exit(f"Error reading file '{input_path}': {e}")

    if tags:
        files = {
            'input_text': (input_path, content, 'text/xml')
        }
        data = {"src": src_lang, "tgt": tgt_lang}
        if prompt:
            data["prompt"] = prompt
        response = requests.post(url, files=files, data=data)
    else:
        data = {"input_text": content, "src": src_lang, "tgt": tgt_lang}
        if prompt:
            data["prompt"] = prompt
        response = requests.post(url, data=data)

    if response.status_code == 200:
        return response.content
    else:
        error_msg = f"Error: {response.status_code} - {response.text}"
        sys.stderr.write(error_msg + "\n")
        sys.exit(error_msg)

def main():
    parser = argparse.ArgumentParser(
        description="Translate a file using a translation API."
    )
    parser.add_argument("input_file",
                        help="Path to the input file to translate")
    parser.add_argument("--src", default="en",
                        help="Source language code (default: en)")
    parser.add_argument("--tgt", default="fr",
                        help="Target language code (default: fr)")
    parser.add_argument("--model", default="aya-expanse-8b",
                        help="Model identifier aya-expanse-8b")
    parser.add_argument("--tags", action="store_true",
                        help="Wrap the file content with XML tags.")
    parser.add_argument("--prompt", default=None,
                        help="Optional prompt for the translation.")
    parser.add_argument("--base-url", default="https://quest.ms.mff.cuni.cz/llmtranslate-1/api/v2/models",
                        help="Base URL for the translation API (default: https://quest.ms.mff.cuni.cz/llmtranslate-1/api/v2/models)")
    parser.add_argument("--output", "-o", default=None,
                        help="Path to the output file. Defaults to 'translated_<input_file>'.")

    args = parser.parse_args()

    translated_content = translate_file(
        src_lang=args.src,
        tgt_lang=args.tgt,
        input_path=args.input_file,
        model=args.model,
        tags=args.tags,
        prompt=args.prompt,
        base_url=args.base_url
    )

    output_file = args.output if args.output else f"translated_{args.input_file}"
    try:
        with open(output_file, 'wb') as out_file:
            out_file.write(translated_content)
        print(f"Translation saved to '{output_file}'")
    except Exception as e:
        sys.exit(f"Error writing to output file '{output_file}': {e}")

if __name__ == "__main__":
    main()

