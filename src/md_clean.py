#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from Alfred import Items as Items
from Alfred import Tools as Tools
from MyNotes import Search


def write_summary(md_notes_list, tag):
    """
    Write list of md notes with tag into tmp summary.md

    Args:
        md_notes_list (list): List of Notes containg tag name
        tag (str): Name of the tag

    Returns:
        str: path to summary.md file
    """
    cache_dir = Tools.getCacheDir()
    cache_file_path = os.path.join(cache_dir, "summary.md")
    if os.path.exists(cache_file_path):
        os.remove(cache_file_path)
    content_list = ["### MD Notes with tag: {}".format(tag)]
    for el in md_notes_list:
        content_list.append("* [{0}]({1}) `{2}`".format(el['title'], el['path'], el['filename']))
    content = "\n".join(content_list)
    with open(cache_file_path, "w") as f:
        f.write(content)
    return cache_file_path


# create MD search object
md_search = Search()

# Load Env variables
query = Tools.getArgv(1) if len(Tools.getArgv(1)) > 2 else ""
if query is not "" and not(query.startswith("#")):
    query = "#{}".format(query)


# Get Search config with AND and OR
search_terms, search_type = md_search.get_search_config(query)

# create WF object
wf = Items()

# exec search if search terms were entered
if len(search_terms) > 0:
    sorted_file_list = md_search.notes_search(search_terms, search_type)
    matches = len(sorted_file_list)
    file_pathes = [f['path'] for f in sorted_file_list]
    arg_string = "|".join(file_pathes)
    summary_file = write_summary(sorted_file_list, query)
    if matches > 0:
        wf.setItem(
            title="Batch delete {0} notes with tag {1}".format(matches, query),
            subtitle=u"\u23CE to delete ALL notes and corresponding Assets. THIS CANNOT BE UNDONE!",
            arg=arg_string
        )
        wf.setIcon(m_path='icons/delete.png', m_type='image')
        wf.addItem()
        wf.setItem(
            title="Preview affected MD Notes",
            subtitle=u"Preview of affected md notes. \u21E7 for Quicklook, \u23CE to open. NOTES ARE NOT DELETED!",
            type='file',
            arg=summary_file
        )
        wf.setIcon(m_path='icons/clipboard.png', m_type='image')
        wf.addItem()
    else:
        wf.setItem(
            title="MD notes not found with tag: {}".format(query),
            subtitle="Try another tag name",
            valid=False
        )
        wf.addItem()
else:
    wf.setItem(
        title="Enter a tag name",
        subtitle="tag name with or without leading #",
        valid=False
    )
    wf.addItem()
wf.write()
