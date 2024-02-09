def log(string, type="DEBUG"):
    allowed_types = ["DEBUG", "INFO", "WARNING", "ERROR"]
    print(f"{type.upper() if type.upper() in allowed_types else 'OTHER'} \t> {string}")