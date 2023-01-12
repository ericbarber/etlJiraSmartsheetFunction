import chardet

with open("jobs.json", "rb") as f:
    result = chardet.detect(f.read())
    # result gives a dict containing encoding name and confidence
    encoding = result['encoding']
    print(encoding)
