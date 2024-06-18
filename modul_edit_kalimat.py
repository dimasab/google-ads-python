import re

def fungsi_edit_kalimat(judulraw):
    paksa_kapital = ['SSD', 'HDD', 'RAM', 'SDRAM', 'ROM', 'GTX', 'RTX', 'FHD', 'HD', 'VGA', 'GB', 'TB', 'IPS', 'OHS', 'RGB', 'SRGB', 'USB', 'PCB', 'PC', 'TV', 'AMD', 'UHD', 'MSI', 'HP', 'US', 'SKU', 'SD', 'TUF', 'CPU', 'GPU', 'SIM', '2GB', '4GB', '6GB', '8GB', '16GB', '32GB', '64GB', '128GB', '256GB', '512GB', '1TB', '2TB', 'AI', 'NFC', 'GT', 'ROG', 'DDR', 'DDR3', 'DDR4', 'DDR5', 'GDDR', 'GDDR3', 'GDDR4', 'GDDR5', 'DIMM', 'SODIMM', 'III', 'II']
    
    paksa_kecil_depan = ['I3', 'I5', 'I7', 'I9', 'IPHONE', 'IOS', 'IPAD']
    
    abaikan = ['NVME', 'PCIE', 'MACOS', 'IN', 'UP', 'TO', 'S/D']
    
    arrayhapusteks = [ # define the following words with regex, for later use in the function below
        r'\bl+a+p+t+o+p+\b',
        r'\bn+o+t+e+b+o+o+k+\b',
        r'\bt+e+r+m+u+r+a+h+\b', 
        r'\bm+u+r+a+h+\b', 
        r'\bt+e+r+l+a+r+i+s+\b',
        r'\bo+b+r+a+l+\b',
        r'\bj+u+a+l+\b',
        r'\be+l+e+g+a+n+t+\b',
        r'\be+l+e+g+a+n+\b',
        r'\bb+e+s+t+\b',
        r'\bs+e+l+l+e+r+\b',
        r'\bh+a+r+g+a+\b',
        r'\bb+a+n+g+e+t+\b',
        r'\bk+o+n+d+i+s+i+\b',
        r'\bm+a+s+i+h+\b',
        r'\bp+r+o+m+o+\b',
        r'\bi+m+u+t+\b',
        r'\bb+u+a+t+\b',
        r'\bp+a+l+i+n+g+\b',
        r'\bs+a+n+g+a+t+\b',
        r'\bl+e+b+i+h+\b',
        r'\bd+a+r+i+n+g+\b',
        r'\bs+i+k+a+t+\b',
        r'\bb+o+s+k+u+\b',
        r'\bo+l+s+h+o+p+\b',
        r'\bb+a+n+d+e+l+\b',
        r'\bl+e+m+b+u+r+\b',
        r'\bk+u+l+i+a+h+a+n+\b',
        r'\bk+u+l+i+a+h+\b',
        r'\bk+e+r+j+a+a+n+\b',
        r'\bp+e+k+e+r+j+a+\b',
        r'\bk+e+r+j+a+\b',
        r'\bk+a+n+t+o+r+a+n+\b',
        r'\bk+a+n+t+o+r+\b',
        r'\bp+e+l+a+j+a+r\b',
        r'\bu+n+t+u+k+\b',
        r'\bh+a+n+y+a+\b',
        r'\bc+o+c+o+k+\b',
        r'\bd+a+n+\b',
        r'\bu+t+k+\b',
        r'\bo+n+l+i+n+e+\b',
        r'\bb+e+r+g+a+r+a+n+s+i+\b',
        r'\bt+e+r+b+a+i+k+\b',
        r'\bf+l+a+s+h\b',
        r'\bh+o+t+\b',
        r'\bb+i+g+\b',
        r'\bb+i+g+g+e+r+\b',
        r'\bs+a+l+e\b',
        r'\bl+e+p+t+o+p+\b',
        r'\bb+i+s+n+i+s+\b',
        r'\bs+i+a+p+\b',
        r'\be+d+i+t+i+n+g+\b',
        r'\bp+a+k+a+i+\b',
        r'\b1+j+u+t+a+a+n+\b',
        r'\b2+j+u+t+a+a+n+\b',
        r'\b3+j+u+t+a+a+n+\b',
        r'\b4+j+u+t+a+a+n+\b',
        r'\b5+j+u+t+a+a+n+\b',
        r'\b6+j+u+t+a+a+n+\b',
        r'\b7+j+u+t+a+a+n+\b',
        r'\b8+j+u+t+a+a+n+\b',
        r'\b9+j+u+t+a+a+n+\b',
        r'\b1+j+u+t+a+-+a+n+\b',
        r'\b2+j+u+t+a+-+a+n+\b',
        r'\b3+j+u+t+a+-+a+n+\b',
        r'\b4+j+u+t+a+-+a+n+\b',
        r'\b5+j+u+t+a+-+a+n+\b',
        r'\b6+j+u+t+a+-+a+n+\b',
        r'\b7+j+u+t+a+-+a+n+\b',
        r'\b8+j+u+t+a+-+a+n+\b',
        r'\b9+j+u+t+a+-+a+n+\b',
        r'\b1+ j+u+t+a+a+n+\b',
        r'\b2+ j+u+t+a+a+n+\b',
        r'\b3+ j+u+t+a+a+n+\b',
        r'\b4+ j+u+t+a+a+n+\b',
        r'\b5+ j+u+t+a+a+n+\b',
        r'\b6+ j+u+t+a+a+n+\b',
        r'\b7+ j+u+t+a+a+n+\b',
        r'\b8+ j+u+t+a+a+n+\b',
        r'\b9+ j+u+t+a+a+n+\b',
        r'\b1+ j+u+t+a+-+a+n+\b',
        r'\b2+ j+u+t+a+-+a+n+\b',
        r'\b3+ j+u+t+a+-+a+n+\b',
        r'\b4+ j+u+t+a+-+a+n+\b',
        r'\b5+ j+u+t+a+-+a+n+\b',
        r'\b6+ j+u+t+a+-+a+n+\b',
        r'\b7+ j+u+t+a+-+a+n+\b',
        r'\b8+ j+u+t+a+-+a+n+\b',
        r'\b9+ j+u+t+a+-+a+n+\b',
        r'\bj+u+t+a+a+n+\b',
        r'\bj+u+t+a+\b',
        r'\bb+a+g+u+s+\b',
        r'\bl+e+l+e+t+\b',
        r'\ba+n+t+i+\b',
        r'\bf+r+e+e+\b',
        r'\bu+p+g+r+a+d+e+\b',
        r'\bs+e+n+i+l+a+i+\b',
        r'\bm+o+s+u+e+\b',
        r'\bb+e+r+k+e+l+a+s+\b',
        r'\bk+e+r+e+n+\b',
        r'\bt+e+k+n+o+ k+i+t+a+\b',
        r'\bb+i+s+a+\b',
        r'\bd+i+l+i+p+a+t+\b',
        r'\bt+e+r+b+a+r+u+\b',
        r'\bb+a+r+u+\b',
        r'\bm+u+n+g+i+l+\b',
        r'\bt+e+r+j+a+n+g+k+a+u+\b',
        r'\bi+n+s+t+a+n+t+\b',
        r'\bi+n+s+t+a+n+\b',
        r'\bg+o+j+e+k+\b',
        r'\bg+r+a+b+\b',
        r'\bs+a+m+e+d+a+y+\b',
        r'\bs+a+m+e+ d+a+y+\b',
        r'\bv+a+r+i+a+s+i+\b',
        r'\b1+\ +t+a+h+u+n+\b',
        r'\b2+\ +t+a+h+u+n+\b',
        r'\b1+\ +b+u+l+a+n+\b',
        r'\b2+\ +b+u+l+a+n+\b',
        r'\b1+t+a+h+u+n+\b',
        r'\b2+t+a+h+u+n+\b',
        r'\b1+b+u+l+a+n+\b',
        r'\b2+b+u+l+a+n+\b',
        r'\bt+a+h+u+n+\b',
        r'\bb+u+l+a+n+\b',
        r'\b1+\ +t+h+n+\b',
        r'\b2+\ +t+h+n+\b',
        r'\b1+\ +b+l+n+\b',
        r'\b2+\ +b+l+n+\b',
        r'\b1+t+h+n+\b',
        r'\b2+t+h+n+\b',
        r'\b1+b+l+n+\b',
        r'\b2+b+l+n+\b',
        r'\bt+h+n+\b',
        r'\bb+l+n+\b',
        r'\bo+k+\b',
        r'\bs+e+r+i+\b',
        r'\bl+e+n+g+k+a+p+\b',
        r'\bi+s+t+i+m+e+w+a+\b',
        r'\bn+g+e+b+u+t+\b',
        r'\bm+a+l+a+n+g+\b',
        r'\bb+e+r+k+u+a+l+i+t+a+s+\b',
        r'\bb+e+r+k+w+a+l+i+t+a+s+\b',
        r'\bs+e+p+e+c+i+a+l+\b',
        r'\bs+e+p+e+s+i+a+l+\b',
        r'\bd+e+a+l+\b',
        r'\be+v+e+r+\b',
        r'\bc+n+c+i+n+t+e+l+\b',
        r'\bc+n+c+a+m+d+\b',
        r'\bc+n+c+\b',
        r'\bh+a+n+d+p+h+o+n+e+\b',
        r'\bs+m+a+r+t+p+h+o+n+e+\b',
        r'\bb+a+t+e+r+a+i+\b',
        r'\bb+a+t+t+e+r+y+\b',
        r'\bb+a+t+e+r+r+y+\b',
        r'\bb+a+t+e+r+y+\b',
        r'\bs+e+g+e+l+\b',
        r'\bl+i+k+e+\b',
        r'\bn+e+w+\b',
        r'\bl+i+k+e+n+e+w+\b',
        r'\ba+s+l+i+\b',
        r'\b1+0+0+\%+\b',
        r'\bn+o+\ +m+i+n+u+s+\b',
        r'\bn+o+m+i+n+u+s+\b',
        r'\bm+u+l+u+s+1+0+0+\%+\b',
        r'\bd+i+p+a+k+e+\b',
        r'\bd+i+p+a+k+a+i+\b',
        r'\bb+e+b+e+r+a+p+a+\b',
        r'\bs+e+l+a+m+a+\b',
        r'\bm+e+w+a+h+\b',
        r'\bm+o+u+s+\b',
        r'\bk+u+r+i+r+\b',
        r'\bl+a+u+n+c+h+\b',
        r'\ba+r+r+i+v+a+l+\b',
        r'\be+x+c+l+u+s+i+v+e+\b',
        r'\be+k+s+k+l+u+s+i+f+\b',
        r'\br+e+c+o+m+m+e+n+d+e+d+\b',
        r'\br+e+c+o+m+m+e+n+d+\b',
        r'\br+e+k+o+m+e+n+d+e+d+\b',
        r'\br+e+k+o+m+e+n+\b',
        r'\bb+a+n+y+a+k+\b',
        r'\bl+a+y+a+r+\b',
        r'\bs+e+n+t+u+h+\b',
        r'\bm+e+m+o+r+i+\b',
        r'\bk+o+m+p+u+t+e+r+\b',
        r'\bo+r+i+\b',
        r'\bd+e+n+g+a+n+\b',
        r'\bp+a+k+e+t+\b',
        r'\bb+a+r+a+n+g+\b',
        r'\bm+e+r+i+a+h+\b',
        r'\bb+e+l+a+j+a+r+\b',
        r'\bl+a+y+a+k+\b',
        r'\bs+e+k+o+l+a+h+\b',
        r'\bd+e+s+a+i+n+\b',
        r'\bc+u+m+a+\b',
        r'\bm+u+l+t+i+t+a+s+k+i+n+g+\b',
        r'\br+i+n+g+a+n+\b',
        r'\bw+a+r+n+a+\b',
        r'\bi+t+e+m+\b',
        r'\br+u+g+i+\b',
        r'\be+k+o+n+o+m+i+s+\b',
        r'\bk+e+n+c+a+n+g+\b',
        r'\bc+u+c+i+\b',
        r'\bg+u+d+a+n+g+\b',
        r'\bu+j+i+a+n+\b',
        r'\bu+s+a+h+a+\b',
        r'\bm+a+h+a+s+i+s+w+a+\b',
        r'\ba+n+a+k+\b',
        r'™+',
        r'®+',
        r'[^\x00-\x7F]+', 
        r'\【.*?\】',
    ]

    # Remove undesired texts
    for regex in arrayhapusteks:
        judulraw = re.sub(regex, '', judulraw, flags=re.IGNORECASE)

    judulraw = re.sub(r'\bgenerasi\b', 'gen', judulraw, flags=re.IGNORECASE)  # Change 'generasi' to 'gen'
    judulraw = re.sub(r'\s+', ' ', judulraw)  # Replace multiple spaces with one space

    # Remove spaces before punctuation
    judulraw = re.sub(r'\s+,', ',', judulraw)
    judulraw = re.sub(r'\s+\.', '.', judulraw)

    # Spacing around brackets
    judulraw = re.sub(r'\(\s+', '(', judulraw)
    judulraw = re.sub(r'\s+\)', ')', judulraw)
    judulraw = re.sub(r'\[\s+', '[', judulraw)
    judulraw = re.sub(r'\s+\]', ']', judulraw)

    # Add space before and after brackets
    judulraw = re.sub(r'\(', ' (', judulraw)
    judulraw = re.sub(r'\)', ') ', judulraw)
    judulraw = re.sub(r'\[', ' [', judulraw)
    judulraw = re.sub(r'\]', '] ', judulraw)

    judulraw = re.sub(r'\-+\s+\-+\s+\-+', '-', judulraw)

    untuksisaan = [
        r'\- (?:\- ){1,}',  # adalah - - dan - - - dan seterusnya
        r'/ (?:/ ){1,}',   # adalah / / dan / / / dan seterusnya
        r'\. (?:\. ){1,}',  # adalah . . dan . . . dan seterusnya
        r', (?:, ){1,}',    # adalah , , dan , , , dan seterusnya
        r'\| (?:\| ){1,}',  # adalah | | dan | | | dan seterusnya
        r'\(+\ +\)+',    # adalah ( )
        r'\[+\ +\]+',    # adalah [ ]
        r'\{+\ +\}+',    # adalah { }
        r'\-\-+',       # adalah -- dan seterusnya
        r'\/\/+',       # adalah // dan seterusnya
        r'\.\.+',       # adalah .. dan seterusnya
        r'\,\,+',       # adalah ,, dan seterusnya
        r'\|\|+',       # adalah || dan seterusnya
        r'\(+\)+',      # adalah () dan seterusnya
        r'\[+\]+',      # adalah [] dan seterusnya
        r'\{+\}+',      # adalah {} dan seterusnya
        r'\&+',         # adalah &
        r'\#+',         # adalah #
        r'\!+',         # adalah !
        r'\?+',         # adalah ?
        r'\s+',         # adalah satu spasi (atau lebih)
    ]

    for _ in range(10):  # Repeat ten times
        for regex in untuksisaan:
            judulraw = re.sub(regex, ' ', judulraw)

    judulraw = re.sub(r'\bbukan\b', 'BUKAN', judulraw, flags=re.IGNORECASE)
    judulraw = re.sub(r'\bnot\b', 'NOT', judulraw, flags=re.IGNORECASE)

    judulraw = judulraw.split(' BUKAN ')[0].split(' NOT ')[0]

    for _ in range(10):  # Repeat ten times
        judulraw = judulraw.strip('/-|.,')

    judulraw_split = [re.sub(r'[^a-zA-Z0-9]', '', word.upper()) for word in judulraw.split()]
    judulraw_words = judulraw.split()
    array_kata_unik = []
    array_kata_unik_KAPITAL = []

    for i in range(len(judulraw_split)):
        checker_sekarang = judulraw_split[i]
        
        if ((checker_sekarang not in array_kata_unik_KAPITAL or len(checker_sekarang) < 3) and checker_sekarang not in abaikan):
            array_kata_unik_KAPITAL.append(checker_sekarang)
            
            if checker_sekarang not in paksa_kapital and not any(char.isdigit() for char in checker_sekarang):
                judulraw_words[i] = judulraw_words[i].capitalize()
            elif checker_sekarang in paksa_kapital:
                judulraw_words[i] = judulraw_words[i].upper()
            elif checker_sekarang in paksa_kecil_depan:
                judulraw_words[i] = judulraw_words[i].lower()

            array_kata_unik.append(judulraw_words[i])

    return ' '.join(array_kata_unik)