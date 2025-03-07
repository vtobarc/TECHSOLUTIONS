import os

def remove_null_bytes(directory):
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            with open(filepath, 'rb') as f:
                content = f.read()
            if b'\x00' in content:
                print(f"Cleaning {filepath}")
                clean_content = content.replace(b'\x00', b'')
                with open(filepath, 'wb') as f:
                    f.write(clean_content)

remove_null_bytes('E:/App_Tech/Tech/')
