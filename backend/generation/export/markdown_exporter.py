def export_markdown(markdown: str, output_path: str) -> str:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    return output_path
