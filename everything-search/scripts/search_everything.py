#!/usr/bin/env python3
"""
Everything Search Native Tool
Directly connects to local voidtools Everything native HTTP server (127.0.0.1:18080)
to provide sub-millisecond full-disk file search.
"""

import sys
import json
import urllib.parse
import urllib.request
import argparse
import os

DEFAULT_PORT = 18080

def search_everything(query, count=10, port=DEFAULT_PORT):
    params = {
        "search": query,
        "json": "1",
        "count": str(count),
        "path_column": "1",
        "size_column": "1",
        "date_modified_column": "1"
    }
    url = f"http://127.0.0.1:{port}/?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = []
            for item in data.get("results", []):
                name = item.get("name", "")
                path = item.get("path", "")
                full_path = os.path.join(path, name) if path else name
                results.append({
                    "name": name,
                    "path": path,
                    "full_path": full_path,
                    "type": item.get("type", "file"),
                    "size": item.get("size"),
                    "date_modified": item.get("date_modified")
                })
            return {
                "total_results": data.get("totalResults", 0),
                "returned_count": len(results),
                "items": results
            }
    except Exception as e:
        return {
            "error": f"Failed to connect to Everything on 127.0.0.1:{port}: {str(e)}",
            "hint": "Please make sure Everything is running and HTTP server is enabled on port 18080 (Tools > Options > HTTP Server)."
        }

def main():
    parser = argparse.ArgumentParser(description="Query local voidtools Everything search engine")
    parser.add_argument("query", help="Search query (e.g., ext:ioc, *.SLDPRT, datasheet)")
    parser.add_argument("-n", "--count", type=int, default=10, help="Maximum number of results to return")
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT, help="Everything HTTP port (default: 18080)")

    args = parser.parse_args()
    res = search_everything(args.query, args.count, args.port)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
