import pandas as pd
import os

data = [
    {
        'Name of material': 'Matplotlib',
        'Version / identifier': '3.8.4',
        'RRID': 'SCR_008624',
        'Comments': 'Figure rendering; open source (https://matplotlib.org)'
    },
    {
        'Name of material': 'NumPy',
        'Version / identifier': '1.26.4',
        'RRID': 'SCR_008633',
        'Comments': 'Numerical arrays; open source (https://numpy.org)'
    },
    {
        'Name of material': 'openpyxl',
        'Version / identifier': '3.1.2',
        'RRID': 'Not applicable',
        'Comments': 'Spreadsheet output for submitted tables; open source (https://openpyxl.readthedocs.io)'
    },
    {
        'Name of material': 'pandas',
        'Version / identifier': '2.2.2',
        'RRID': 'SCR_018214',
        'Comments': 'Tabular data handling; open source (https://pandas.pydata.org)'
    },
    {
        'Name of material': 'Pillow',
        'Version / identifier': '10.3.0',
        'RRID': 'SCR_026047',
        'Comments': 'Image loading for ground-truth verification; open source (https://python-pillow.org)'
    },
    {
        'Name of material': 'Python',
        'Version / identifier': '3.13.0',
        'RRID': 'SCR_008394',
        'Comments': 'Analysis environment; open source (https://www.python.org)'
    },
    {
        'Name of material': 'SciPy',
        'Version / identifier': '1.13.1',
        'RRID': 'SCR_008058',
        'Comments': 'Exact binomial intervals and tests, connected-component labeling; open source (https://scipy.org)'
    },
    {
        'Name of material': 'Vision-Language Model Annotator',
        'Version / identifier': 'Google Gemini 3.1 / 3.5 Flash Lite',
        'RRID': 'SCR_024982',
        'Comments': 'Image annotation accessed programmatically Nov 2026 via Google AI Studio API (gemini-3.1-flash-lite, gemini-3.5-flash-lite), prompt: "Count the dark blobs in this image. Reply with a single integer and nothing else.", temperature 1.0, max tokens 16 (https://ai.google.dev)'
    }
]

df = pd.DataFrame(data)

for target_dir in ['submission/Paper_Tables', 'submission/Tables', 'Tables']:
    os.makedirs(target_dir, exist_ok=True)
    csv_path = os.path.join(target_dir, 'Table_of_Materials.csv')
    xlsx_path = os.path.join(target_dir, 'Table_of_Materials.xlsx')
    df.to_csv(csv_path, index=False, encoding='utf-8')
    df.to_excel(xlsx_path, index=False)
    print(f'Successfully wrote {csv_path} and {xlsx_path}')
