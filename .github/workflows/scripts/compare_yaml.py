import yaml, sys, os
from collections import OrderedDict

def get_keys(yaml_content, prefix=''):
    keys = []
    if isinstance(yaml_content, dict):
        for k, v in yaml_content.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.append(full_key)
            if isinstance(v, (dict, list)):
                keys.extend(get_keys(v, full_key))
    elif isinstance(yaml_content, list):
        for i, item in enumerate(yaml_content):
            if isinstance(item, (dict, list)):
                keys.extend(get_keys(item, f"{prefix}[{i}]"))
    return keys

def main():
    old_content = {}
    new_content = yaml.safe_load(open(sys.argv[1]))

    if os.path.exists(sys.argv[2]):
        with open(sys.argv[2], 'r') as f:
            old_content = yaml.safe_load(f) or {}

    old_keys = set(get_keys(old_content))
    new_keys = set(get_keys(new_content))

    # Generate change markers
    added = [f"+ {k}" for k in new_keys - old_keys]
    removed = [f"- {k}" for k in old_keys - new_keys]
    modified = [f"# {k}" for k in old_keys & new_keys]

    print("\n".join(sorted(added + removed + modified)))

if __name__ == "__main__":
    main()