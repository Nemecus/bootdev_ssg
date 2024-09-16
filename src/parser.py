import re
import os

from textnode import *
from blockparser import *

def text_to_textnodes(text):
    node_list = [TextNode(text, text_type_text)]
    node_list = split_nodes_delimiter(node_list, "**", text_type_bold)
    node_list = split_nodes_delimiter(node_list, "*", text_type_italic)
    node_list = split_nodes_delimiter(node_list, "`", text_type_code)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []

        text_split = old_node.text.split(delimiter)
        total_split = len(text_split)
        if total_split % 2 == 0:
            raise ValueError("Invalid Markdown")
        for i in range(total_split):
            if text_split[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(text_split[i], text_type_text))
            else:
                split_nodes.append(TextNode(text_split[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def  extract_markdown_images(text):
    image_criteria = r"!\[(.*?)\]\((.*?)\)"
    image_matches = re.findall(image_criteria, text)
    return image_matches

def extract_markdown_links(text):
    link_criteria = r"(?<!!)\[(.*?)\]\((.*?)\)"
    link_matches = re.findall(link_criteria, text)
    return link_matches

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")