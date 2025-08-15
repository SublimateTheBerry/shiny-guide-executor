import os

# --- Helper function to chunk a list ---
def chunk_list(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

# --- Directory Setup ---
# Correctly determine the project root, assuming this script is in 'Files'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
protocol_dir = os.path.join(project_root, 'Splitted-By-Protocol')
sub_dir = os.path.join(project_root, 'Sub')

os.makedirs(protocol_dir, exist_ok=True)
os.makedirs(sub_dir, exist_ok=True)

# --- File Paths ---
vmess_file = os.path.join(protocol_dir, 'vmess.txt')
vless_file = os.path.join(protocol_dir, 'vless.txt')
trojan_file = os.path.join(protocol_dir, 'trojan.txt')
ss_file = os.path.join(protocol_dir, 'ss.txt')
ssr_file = os.path.join(protocol_dir, 'ssr.txt')
all_configs_file = os.path.join(project_root, 'All_Configs_Sub.txt')

# --- Clear Old Files ---
for f in [vmess_file, vless_file, trojan_file, ss_file, ssr_file]:
    if os.path.exists(f):
        open(f, "w").close()

if os.path.exists(sub_dir):
    for f in os.listdir(sub_dir):
        os.remove(os.path.join(sub_dir, f))

# --- Read and Categorize Proxies ---
vless_list, vmess_list, trojan_list, ss_list, ssr_list = [], [], [], [], []

if os.path.exists(all_configs_file):
    with open(all_configs_file, 'r', encoding='utf-8') as f:
        for line in f:
            config = line.strip()
            if not config:
                continue
            if config.startswith("vless://"): vless_list.append(config)
            elif config.startswith("vmess://"): vmess_list.append(config)
            elif config.startswith("trojan://"): trojan_list.append(config)
            elif config.startswith("ss://"): ss_list.append(config)
            elif config.startswith("ssr://"): ssr_list.append(config)

# --- Write Categorized Files (optional but good practice) ---
with open(vless_file, "w", encoding='utf-8') as f: f.write("\n".join(vless_list))
with open(vmess_file, "w", encoding='utf-8') as f: f.write("\n".join(vmess_list))
with open(trojan_file, "w", encoding='utf-8') as f: f.write("\n".join(trojan_list))
with open(ss_file, "w", encoding='utf-8') as f: f.write("\n".join(ss_list))
with open(ssr_file, "w", encoding='utf-8') as f: f.write("\n".join(ssr_list))

# --- Create Subscription Files ---
file_counter = 1
all_proxies = [vless_list, vmess_list, trojan_list, ss_list, ssr_list]

# Determine the number of "perfect" groups
min_len = min(len(p) for p in all_proxies) if all_proxies else 0

# 1. Create "perfect" groups
for i in range(min_len):
    proxy_group = [
        vless_list[i],
        vmess_list[i],
        trojan_list[i],
        ss_list[i],
        ssr_list[i],
    ]
    file_path = os.path.join(sub_dir, f"Sub{file_counter:04d}.txt")
    with open(file_path, "w", encoding='utf-8') as f:
        f.write("\n".join(proxy_group))
    file_counter += 1

# 2. Collect leftovers
leftovers = []
leftovers.extend(vless_list[min_len:])
leftovers.extend(vmess_list[min_len:])
leftovers.extend(trojan_list[min_len:])
leftovers.extend(ss_list[min_len:])
leftovers.extend(ssr_list[min_len:])

# 3. Create groups from leftovers
if leftovers:
    for chunk in chunk_list(leftovers, 5):
        file_path = os.path.join(sub_dir, f"Sub{file_counter:04d}.txt")
        with open(file_path, "w", encoding='utf-8') as f:
            f.write("\n".join(chunk))
        file_counter += 1

print(f"Successfully created {file_counter - 1} subscription files in '{sub_dir}'")
