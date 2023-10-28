import sqlite3
import os
import email
import re

# Define a function to extract email details from an EML file
def extract_spf_result(eml_file):
    with open(eml_file, 'r', encoding='utf-8', errors='ignore') as file:
        email_data = email.message_from_file(file)
        spf_headers = email_data.get_all('Received-SPF')
        dkim_headers = email_data.get_all('Authentication-Results-Original')

        # Extract client-ip, SPF result, and DKIM result
        client_ip = spf_result = dkim_result = None
        if spf_headers:
            last_spf_header = spf_headers[-1]
            client_ip_match = re.search(r'client-ip=([\d.]+)', last_spf_header)
            spf_result_match = re.search(r'\b(pass|fail)\b', last_spf_header, re.I)

            if client_ip_match:
                client_ip = client_ip_match.group(1)
            if spf_result_match:
                spf_result = spf_result_match.group(0).lower()

        if dkim_headers:
            last_dkim_header = dkim_headers[-1]
            dkim_result_match = re.search(r'dkim=([a-zA-Z]+)', last_dkim_header)

            if dkim_result_match:
                dkim_result = dkim_result_match.group(1)

        return {
            'spf_result': spf_result,
            'dkim_result': dkim_result,
            'client-ip': client_ip
        }

    return None


def extract_email_details(eml_file):
    with open(eml_file, 'r', encoding='utf-8', errors='ignore') as file:
        email_data = email.message_from_file(file)
        from_address = email_data.get('From')
        to_address = email_data.get('To')
        subject = email_data.get('Subject')
        email_body = email_data.get_payload()
        return from_address, to_address, subject, email_body

# Create database function
def create_database():
    # Create an SQLite database or connect to an existing one
    conn = sqlite3.connect('email_database.sqlite')

    # Drop to tables
    conn.execute('DROP TABLE IF EXISTS emails')

    cursor = conn.cursor()

    # Create a table to store email details
    cursor.execute('''
        CREATE TABLE emails (
            email_address TEXT PRIMARY KEY,
            from_address TEXT,
            domain_name TEXT,
            email_body TEXT,
            spf_result TEXT,
            dkim_result TEXT,
            client_ip TEXT
        )
    ''')

    return conn, cursor

def close_database(conn):
    # Commit changes and close the database connection
    conn.commit()
    conn.close()

def populate_database(eml_folder, cursor):
# Loop through EML files in the folder
    for root, _, files in os.walk(eml_folder):
        for filename in files:
            if filename.endswith('.eml'):
                eml_path = os.path.join(root, filename)
                
                # Extract email details
                from_address, to_address, _, email_body = extract_email_details(eml_path)

                # if email_body is a list then join it and make it a string
                if isinstance(email_body, list):
                    email_body = ''.join(map(str, email_body))
                                
                # Extract domain name from the sender's email address
                domain_name = re.search('@([\w.-]+)', from_address).group(1) if from_address else None
                domain_name = domain_name or ''

                # Extract SPF result
                spf = extract_spf_result(eml_path)
                spf_result = spf['spf_result']
                dkim_result = spf['dkim_result']
                client_ip = spf['client-ip']

                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO emails (email_address, from_address, domain_name, email_body, spf_result, dkim_result, client_ip)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (to_address, from_address, domain_name, email_body, spf_result, dkim_result, client_ip))
                except sqlite3.Error as e:
                    print("SQLite error:", e)
                    ''' print("to_address:", to_address)
                    print("from_address:", from_address)
                    print("client_ip:", client_ip)
                    print("domain_name:", domain_name)
                    print("email_body:", email_body)
                    print("spf_result:", spf_result)
                    print("dkim_result:", dkim_result)
                    '''


# Define a folder containing EML files
eml_folder = './2023-10-05'
conn, cursor = create_database()
populate_database(eml_folder, cursor)
close_database(conn)

