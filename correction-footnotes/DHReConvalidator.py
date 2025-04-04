import glob
import re


##################

# path to current XML files
xml_path = '/Users/patrickhelling/Documents/DHd2024-BoA-main/Korrektur-Fußnoten/neu2/'

# path for edited XML files (please make the empty folder!)
new_path = '/Users/patrickhelling/Documents/DHd2024-BoA-main/Korrektur-Fußnoten/neu/'

#################

# definition of strings/chars to be replaced (if regular expression needed)
rexo = re.compile(r'\u006f\u0308', re.UNICODE)
rexa = re.compile(r'\u0061\u0308', re.UNICODE)
rexu = re.compile(r'\u0075\u0308', re.UNICODE)
bbad2 = re.compile(r'\u2010', re.UNICODE)
bbad = re.compile(r'\u2011', re.UNICODE)
sbad = re.compile(r'\u202f', re.UNICODE)
tit = re.compile(r'''(<title type="full">
                <title type="main">.*[A-Za-z])(</title>
                <title type="sub">.*</title>
            </title>)''', re.M)

# publication statement
pub = re.compile(r'''<publicationStmt>
            <publisher>Name, Institution</publisher>
            <address>
                <addrLine>Street</addrLine>
                <addrLine>City</addrLine>
                <addrLine>Country</addrLine>
                <addrLine>Name</addrLine>
            </address>
        </publicationStmt>''', re.M)
pub_rep = '''<publicationStmt>
                <publisher>Culture and Computation Lab</publisher>
                <address>
                    <addrLine>Université du Luxembourg</addrLine>
                    <addrLine>2, Avenue de l'Université</addrLine>
                    <addrLine>L-4365 Esch-sur Alzette</addrLine>
                    <addrLine>Luxembourg</addrLine>
                </address>
                <publisher>Luxembourg Centre for Contemporary and Digital History</publisher>
                <address>
                    <addrLine>Université du Luxembourg</addrLine>
                    <addrLine>2, Avenue de l'Université</addrLine>
                    <addrLine>L-4365 Esch-sur Alzette</addrLine>
                    <addrLine>Luxembourg</addrLine>
                </address>
                <publisher>Trier Center for Digital Humanities</publisher>
                <address>
                    <addrLine>Universität Trier</addrLine>  
                    <addrLine>Universitätsring 15</addrLine>
                    <addrLine>54296 Trier</addrLine>
                    <addrLine>Deutschland</addrLine>
                </address>
            </publicationStmt>'''


#################


# add xml file type specification to path
path = xml_path + '*.xml'
files = [file for file in glob.glob(path)]

# iterate over all files
for file in files:
    # get file name
    file_name = file.split('/')[-1].split('.')[0]
    with open(file, 'r') as f, open(''.join([new_path,file_name,'.xml']), 'w') as out:
        # read file
        doc = f.read()
        
        # add xml:id to TEI declaration
        doc = doc.replace('<TEI xmlns="http://www.tei-c.org/ns/1.0">', f'<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="{file_name}">')
        
        # replace list attributes
        doc = doc.replace('<list rend="numbered">', '<list type="ordered">')
        doc = doc.replace('<list rend="bulleted">', '<list type="unordered">')
        
        # replace English
        doc = doc.replace('<head>Bibliography</head>', '<head>Bibliographie</head>')
        
        # replace bad characters (regex)
        doc = re.sub(bbad, '-', doc)
        doc = re.sub(tit, r'''\1.\2''', doc)
        doc = re.sub(rexo, 'ö', doc)
        doc = re.sub(rexa, 'ä', doc)
        doc = re.sub(bbad2, '-', doc)
        doc = re.sub(rexu, 'ü', doc)
        doc = re.sub(sbad, '', doc)

        # add publication institute
        doc = re.sub(pub, pub_rep, doc)

        # move footnotes to end
        ftn_matches = re.findall(r'(<note place="foot" xml:id="ftn\d+" n="\d+">(\n|.)*?</note>)', doc)
        ftn_matches_alt = re.findall(r'(<note xml:id="ftn\d+" place="foot" n="\d+">(\n|.)*?</note>)', doc)
        if ftn_matches_alt:
            ftn_section = '<back>\n<div type="notes">'
            for ftn in ftn_matches_alt:
                ftn = ftn[0].replace('place="foot"', 'rend="footnote text"')
                ftn = re.sub(r'<p.*?>', '', ftn)
                ftn = ftn.replace('</p>', '')
                ftn_section += ('\n' + ftn)
            else:
                ftn_section += '</div>'
            doc_sub = re.sub(r'(\n\s+<note xml:id="(ftn\d+)" place="foot" n="(\d+)">(\n|.)*?</note>)', r'<ref n="\3" target="\2"/>', doc)
            doc_final = re.sub(r'<back>', ftn_section, doc_sub)
            out.write(doc_final)
        elif ftn_matches:
            ftn_section = '<back>\n<div type="notes">'
            for ftn in ftn_matches:
                ftn = ftn[0].replace('place="foot"', 'rend="footnote text"')
                ftn = re.sub(r'<p.*?>', '', ftn)
                ftn = ftn.replace('</p>', '')
                ftn_section += ('\n' + ftn)
            else:
                ftn_section += '</div>'
            doc_sub = re.sub(r'(\n\s+<note place="foot" xml:id="(ftn\d+)" n="(\d+)">(\n|.)*?</note>)', r'<ref n="\3" target="\2"/>', doc)
            doc_final = re.sub(r'<back>', ftn_section, doc_sub)
            out.write(doc_final)
        else:
            out.write(doc)
            
