import os
import base64
from itertools import zip_longest

# --- Directory Setup ---
ptt = os.path.abspath(os.path.join(os.getcwd(), '..'))
protocol_dir = os.path.join(ptt, 'Splitted-By-Protocol')
sub_dir = os.path.join(ptt, 'Sub')

os.makedirs(protocol_dir, exist_ok=True)
os.makedirs(sub_dir, exist_ok=True)

# --- File Paths ---
vmess_file = os.path.join(protocol_dir, 'vmess.txt')
vless_file = os.path.join(protocol_dir, 'vless.txt')
trojan_file = os.path.join(protocol_dir, 'trojan.txt')
ss_file = os.path.join(protocol_dir, 'ss.txt')
ssr_file = os.path.join(protocol_dir, 'ssr.txt')
all_configs_file = os.path.join(ptt, 'All_Configs_Sub.txt')

# --- Clear Old Files ---
for f in [vmess_file, vless_file, trojan_file, ss_file, ssr_file]:
    open(f, "w").close()

for f in os.listdir(sub_dir):
    os.remove(os.path.join(sub_dir, f))


# --- Read and Categorize Proxies ---
vless_list = []
vmess_list = []
trojan_list = []
ss_list = []
ssr_list = []

if os.path.exists(all_configs_file):
    with open(all_configs_file, 'r', encoding='utf-8') as f:
        for line in f:
            config = line.strip()
            if not config:
                continue
            if config.startswith("vless://"):
                vless_list.append(config)
            elif config.startswith("vmess://"):
                vmess_list.append(config)
            elif config.startswith("trojan://"):
                trojan_list.append(config)
            elif config.startswith("ss://"):
                ss_list.append(config)
            elif config.startswith("ssr://"):
                ssr_list.append(config)

# --- Write Categorized Files ---
with open(vless_file, "w", encoding='utf-8') as f:
    f.write("\n".join(vless_list))
with open(vmess_file, "w", encoding='utf-8') as f:
    f.write("\n".join(vmess_list))
with open(trojan_file, "w", encoding='utf-8') as f:
    f.write("\n".join(trojan_list))
with open(ss_file, "w", encoding='utf-8') as f:
    f.write("\n".join(ss_list))
with open(ssr_file, "w", encoding='utf-8') as f:
    f.write("\n".join(ssr_list))


# --- Create Mixed Subscription Files ---
grouped_proxies = list(zip(vless_list, vmess_list, trojan_list, ss_list, ssr_list))

for i, proxy_group in enumerate(grouped_proxies):
    # Format number with leading zeros (e.g., 0001, 0002)
    file_path = os.path.join(sub_dir, f"Sub{i + 1:04d}.txt")
    with open(file_path, "w", encoding='utf-8') as f:
        # proxy_group is a tuple of 5 proxies
        f.write("\n".join(proxy_group))

print(f"Successfully created {len(grouped_proxies)} subscription files in '{sub_dir}'")
