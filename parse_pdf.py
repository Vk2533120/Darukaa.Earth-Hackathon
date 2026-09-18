import re
import zlib

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()

    # Find all compressed streams
    streams = re.findall(b'stream[\r\n]+(.*?)[\r\n]+endstream', pdf_data, re.DOTALL)
    
    extracted = []
    
    for stream in streams:
        try:
            # We assume it's FlateDecode (zlib). Strip any leading white space.
            decompressed = zlib.decompress(stream)
            # Find basic text blocks like: (Some text) Tj or (Some text)
            texts = re.findall(b'\((.*?)\)', decompressed)
            for t in texts:
                try:
                    extracted.append(t.decode('utf-8', errors='ignore'))
                except:
                    pass
        except Exception:
            pass
            
    return "\n".join(extracted)

print(extract_text_from_pdf('Darukaa___FullStack_Hackathon_(1)_revised_613627 (1).pdf')[:3000])
