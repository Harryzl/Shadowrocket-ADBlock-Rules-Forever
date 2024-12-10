import json
import requests

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad responses
    return response.text

def parse_file(file_content):
    # Initialize the JSON structure
    rules_json = {
        "version": 2,
        "rules": [
            {
                "domain": [],
                "domain_suffix": [],
                "domain_regex": [],
                "ip_cidr": [],
                "invert": False
            },
            {
              "type": "logical",
              "mode": "and",
              "rules": [],
              "invert": False
            }
        ]
    }

    # Split the file content into lines
    lines = file_content.strip().split('\n')

    # Iterate over each line
    for line in lines:
        line = line.strip()
        if line.startswith('DOMAIN-SUFFIX,'):
            # Extract domain suffix
            domain_suffix = line.split(',')[1].strip()
            rules_json["rules"][0]["domain_suffix"].append(domain_suffix)
        elif line.startswith('DOMAIN,'):
            # Extract domain
            domain = line.split(',')[1].strip()
            rules_json["rules"][0]["domain"].append(domain)
        elif line.startswith('URL-REGEX,'):
            # Extract URL regex pattern
            url_regex = line.split(',', 1)[1].strip().strip('"')
            rules_json["rules"][0]["domain_regex"].append(url_regex)
        elif line.startswith('IP-CIDR,'):
            # Extract IP CIDR
            ip_cidr = line.split(',')[1].strip()
            rules_json["rules"][0]["ip_cidr"].append(ip_cidr)

    return rules_json

def save_json_to_file(json_data, filename):
    with open('../'+filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

def main():
    url = "https://raw.githubusercontent.com/GMOogway/shadowrocket-rules/master/sr_proxy_list.module"
    
    # Download the file content
    file_content = download_file(url)
    
    # Parse the file content
    parsed_json = parse_file(file_content)
    
    # Save the parsed JSON to a file
    save_json_to_file(parsed_json, 'proxy_list.json')

    url2 = "https://harryzl.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_ad_only.conf"
    
    # Download the file content
    file_content2 = download_file(url2)
    
    # Parse the file content
    parsed_json2 = parse_file(file_content2)
    
    # Save the parsed JSON to a file
    save_json_to_file(parsed_json2, 'reject_list.json')
    
    print(f"JSON data has been saved to proxy_list.json")

if __name__ == "__main__":
    main()
