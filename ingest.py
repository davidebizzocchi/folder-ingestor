from pathlib import Path
from cat.looking_glass.stray_cat import StrayCat
from cat.mad_hatter.decorators import hook, tool

@tool()
def store_file_from_dir(tool_input, cat: StrayCat):
    """Load the documents, carica i documenti. Input is alway None.."""
    
    plugin_path = Path(cat.mad_hatter.get_plugin().path)
    settings = cat.mad_hatter.get_plugin().load_settings()

    dir_path: Path = plugin_path / settings["directory"]
    file_stored_names = []

    if not dir_path.is_dir():
        return f"{settings['directory']} not exists in plugin directory"

    if settings["deep_search"]:
        files = dir_path.rglob("*")
    else:
        files = dir_path.glob("*")

    for file in files:
        if not file.is_file():
            continue
        
        file_content = file.read_text()
        filename = "myfiles" / file.relative_to(dir_path)

        for point in cat.memory.vectors.declarative.get_all_points():
            if point.payload["metadata"]["source"] == str(filename):
                # cat.send_notification(f"{f.name} already exists")
                return

        docs = cat.rabbit_hole.string_to_docs(cat, file_content, "testo")
        cat.rabbit_hole.store_documents(cat, docs, filename, metadata={"automatic_search": {"file_name": filename}})

        cat.send_chat_message(f"file: {filename}")
        file_stored_names.append(filename)

    return "l'utente vuole sapere quali documenti sono stati caricati:" ", ".join(f"file: {file}" for file in file_stored_names)
    