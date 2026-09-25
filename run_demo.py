#!/usr/bin/env python3
import json
from research.model import load_summary,validate_bundle
print(json.dumps(load_summary(),indent=2,ensure_ascii=False))
print("bundle_validation:","PASS" if validate_bundle() else "FAIL")
