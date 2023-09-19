# utils.py

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    return "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in filename)
