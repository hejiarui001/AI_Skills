#!/usr/bin/env python3
"""
Zotero Local Database CLI
Allows AI agents to query the local Zotero SQLite library in read-only mode,
retrieve metadata, and locate local PDF attachments for full-text analysis.
"""

import os
import sys
import json
import sqlite3
import argparse

# Default Zotero paths on Windows
DEFAULT_ZOTERO_DIR = os.path.expanduser(r"~\Zotero")
DB_PATH = os.path.join(DEFAULT_ZOTERO_DIR, "zotero.sqlite")
STORAGE_DIR = os.path.join(DEFAULT_ZOTERO_DIR, "storage")

def get_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Zotero SQLite database not found at {DB_PATH}")
    # Always open in read-only mode to prevent database locks or corruption
    uri = f"file:{DB_PATH.replace(os.sep, '/')}?mode=ro"
    return sqlite3.connect(uri, uri=True)

def search_items(query, limit=10):
    conn = get_connection()
    cur = conn.cursor()
    search_pattern = f"%{query}%"

    sql = """
    SELECT DISTINCT items.itemID, items.key, itemDataValues.value AS title
    FROM items
    JOIN itemData ON items.itemID = itemData.itemID
    JOIN fields ON itemData.fieldID = fields.fieldID
    JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
    WHERE fields.fieldName = 'title'
      AND items.itemID NOT IN (SELECT itemID FROM deletedItems)
      AND itemDataValues.value LIKE ?
    LIMIT ?
    """
    cur.execute(sql, (search_pattern, limit))
    matches = cur.fetchall()

    results = []
    for item_id, key, title in matches:
        # Check attached PDF
        pdf_sql = """
        SELECT items.key, itemAttachments.path
        FROM itemAttachments
        JOIN items ON itemAttachments.itemID = items.itemID
        WHERE (itemAttachments.parentItemID = ? OR itemAttachments.itemID = ?)
          AND itemAttachments.contentType = 'application/pdf'
        """
        cur.execute(pdf_sql, (item_id, item_id))
        pdf_rows = cur.fetchall()
        pdf_files = []
        for p_key, p_path in pdf_rows:
            if p_path:
                rel = p_path.replace("storage:", "")
                full = os.path.join(STORAGE_DIR, p_key, rel)
                if os.path.exists(full):
                    pdf_files.append(full)

        results.append({
            "itemID": item_id,
            "key": key,
            "title": title,
            "pdf_paths": pdf_files
        })

    conn.close()
    return results

def get_item_details(item_id):
    conn = get_connection()
    cur = conn.cursor()

    # Get all fields
    sql = """
    SELECT fields.fieldName, itemDataValues.value
    FROM itemData
    JOIN fields ON itemData.fieldID = fields.fieldID
    JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
    WHERE itemData.itemID = ?
    """
    cur.execute(sql, (item_id,))
    fields = dict(cur.fetchall())

    # Get creators (authors)
    creator_sql = """
    SELECT creatorData.firstName, creatorData.lastName, creatorTypes.creatorType
    FROM itemCreators
    JOIN creators ON itemCreators.creatorID = creators.creatorID
    JOIN creatorData ON creators.creatorDataID = creatorData.creatorDataID
    JOIN creatorTypes ON itemCreators.creatorTypeID = creatorTypes.creatorTypeID
    WHERE itemCreators.itemID = ?
    ORDER BY itemCreators.orderIndex
    """
    cur.execute(creator_sql, (item_id,))
    creators = [{"name": f"{first} {last}".strip(), "role": role} for first, last, role in cur.fetchall()]

    # Get tags
    tags_sql = """
    SELECT tags.name
    FROM itemTags
    JOIN tags ON itemTags.tagID = tags.tagID
    WHERE itemTags.itemID = ?
    """
    cur.execute(tags_sql, (item_id,))
    tags = [r[0] for r in cur.fetchall()]

    # Get PDF attachments
    pdf_sql = """
    SELECT items.key, itemAttachments.path
    FROM itemAttachments
    JOIN items ON itemAttachments.itemID = items.itemID
    WHERE (itemAttachments.parentItemID = ? OR itemAttachments.itemID = ?)
      AND itemAttachments.contentType = 'application/pdf'
    """
    cur.execute(pdf_sql, (item_id, item_id))
    pdf_files = []
    for p_key, p_path in cur.fetchall():
        if p_path:
            rel = p_path.replace("storage:", "")
            full = os.path.join(STORAGE_DIR, p_key, rel)
            if os.path.exists(full):
                pdf_files.append(full)

    conn.close()
    return {
        "itemID": item_id,
        "fields": fields,
        "creators": creators,
        "tags": tags,
        "pdf_paths": pdf_files
    }

def list_recent(limit=10):
    conn = get_connection()
    cur = conn.cursor()

    sql = """
    SELECT items.itemID, items.key, itemDataValues.value AS title, items.dateModified
    FROM items
    JOIN itemData ON items.itemID = itemData.itemID
    JOIN fields ON itemData.fieldID = fields.fieldID
    JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
    WHERE fields.fieldName = 'title'
      AND items.itemID NOT IN (SELECT itemID FROM deletedItems)
    ORDER BY items.dateModified DESC
    LIMIT ?
    """
    cur.execute(sql, (limit,))
    rows = cur.fetchall()
    conn.close()
    return [{"itemID": r[0], "key": r[1], "title": r[2], "dateModified": r[3]} for r in rows]

def main():
    parser = argparse.ArgumentParser(description="Zotero Local SQLite CLI for AI Agents")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search
    search_parser = subparsers.add_parser("search", help="Search items by title")
    search_parser.add_argument("query", help="Keyword to search in title")
    search_parser.add_argument("--limit", type=int, default=10, help="Max results")

    # Get
    get_parser = subparsers.add_parser("get", help="Get full item metadata and PDF paths")
    get_parser.add_argument("item_id", type=int, help="Item ID")

    # Recent
    recent_parser = subparsers.add_parser("recent", help="List recent items")
    recent_parser.add_argument("--limit", type=int, default=10, help="Max results")

    args = parser.parse_args()

    try:
        if args.command == "search":
            res = search_items(args.query, args.limit)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "get":
            res = get_item_details(args.item_id)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.command == "recent":
            res = list_recent(args.limit)
            print(json.dumps(res, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
