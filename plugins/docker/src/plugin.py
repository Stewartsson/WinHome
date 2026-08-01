import sys
import json
import os
import tempfile
from pathlib import Path

def deep_merge(dict1, dict2):
    """Recursively deep merge dict2 into dict1."""
    for key, value in dict2.items():
        if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
            deep_merge(dict1[key], value)
        else:
            dict1[key] = value
    return dict1

def get_config_path():
    """Resolve cross-platform Docker config path."""
    return Path.home() / ".docker" / "config.json"

def main():
    input_data = sys.stdin.read().strip()
    
    # 1. Empty stdin returns JSON error
    if not input_data:
        print(json.dumps({"error": "Empty stdin"}))
        sys.exit(1)

    try:
        request = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON format: {str(e)}"}))
        sys.exit(1)

    request_id = request.get("requestId")
    action = request.get("action")
    args = request.get("args", {})

    # 2. check_installed bare bool
    if action == "check_installed":
        print("true")
        return

    if action == "apply":
        settings = args.get("settings", {})
        dry_run = args.get("dryRun", False)
        
        config_path = get_config_path()
        existing_data = {}
        
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except Exception:
                pass  # Fallback to empty dict if corrupted
                
        if "compose" not in existing_data or not isinstance(existing_data["compose"], dict):
            existing_data["compose"] = {}
            
        # 3. Deep-merge compose settings
        deep_merge(existing_data["compose"], settings)
        
        if not dry_run:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 4. Atomic writes via tempfile.mkstemp + os.replace
            fd, temp_path = tempfile.mkstemp(dir=config_path.parent, text=True)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=2)
                    # 5. POSIX trailing newlines
                    f.write("\n")
                os.replace(temp_path, config_path)
            except Exception as e:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                print(json.dumps({"requestId": request_id, "error": str(e)}))
                sys.exit(1)

        # 6. Protocol compliance: No success/data fields
        print(json.dumps({"requestId": request_id}))
        return

    print(json.dumps({"requestId": request_id, "error": f"Unknown action: {action}"}))
    sys.exit(1)

if __name__ == "__main__":
    main()
  
