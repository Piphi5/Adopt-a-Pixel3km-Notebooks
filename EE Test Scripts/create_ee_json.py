import json
import sys
import base64


def make_json(json_text):
    content = base64.b64decode(json_text).decode()
    with open("ee-credentials.json", "w") as f:
        f.write(content)


if __name__ == "__main__":
    make_json(sys.argv[1])
