# Can save file

> https://github.com/SkyrimScriptingBeta/PapyrusPad/issues/2

## What We've Done So Far

We've established a solid foundation for file saving functionality:

1. **Filesystem Interface**: Created a comprehensive `IFileSystem` interface that defines all necessary file operations:
   - Reading and writing text files
   - Checking file existence
   - File and directory management
   - Path manipulation

2. **Memory Implementation**: Implemented a `MemoryFileSystem` class that provides an in-memory implementation of the filesystem interface, which is useful for testing.

3. **Document Model**: Created a `TextDocument` class that represents a text document with:
   - Content management
   - Modification tracking
   - Save functionality that uses the filesystem interface

4. **Save Action**: Implemented a `SaveAction` class that:
   - Gets the active document
   - Checks if it has a path
   - Calls the document's save method
   - Shows appropriate error messages

5. **Tests**: Created comprehensive tests for the save functionality:
   - Testing saving with an active document
   - Testing saving with no active document
   - Testing saving a document with no path
   - Testing saving with a save failure

6. **Dependency Injection**: Set up a dependency injection system that allows components to request dependencies like the filesystem.

## What's Done

- ✅ Filesystem interface design
- ✅ In-memory filesystem implementation
- ✅ Document model with save functionality
- ✅ Save action with basic error handling
- ✅ Unit tests for save functionality
- ✅ Dependency injection for filesystem and dialog services

## What's Remaining

1. **Real Filesystem Implementation**: We need to create a real filesystem implementation that saves files to disk using Qt's file handling classes or Python's standard library.

2. **Save As Functionality**: We need to implement a "Save As" action that shows a file dialog to let users choose where to save files.

3. **Open File Functionality**: We need to implement an "Open" action that shows a file dialog to let users open existing files.

4. **Recent Files Management**: We should track recently opened files for quick access.

5. **File Change Detection**: We should detect when files are changed outside the application and prompt the user to reload.

6. **Unsaved Changes Prompt**: We should prompt the user to save unsaved changes when closing a document or the application.

7. **Production Configuration**: Update the production container to use the real filesystem implementation instead of the memory implementation.

## Recommended Next Steps

1. **Create a Qt Filesystem Implementation**: Implement `IFileSystem` using Qt's file handling classes (QFile, QDir):
   ```python
   class QtFileSystem(IFileSystem):
       @override
       def read_text(self, path: str) -> str:
           file = QFile(path)
           if not file.open(QIODevice.ReadOnly | QIODevice.Text):
               raise FileNotFoundError(f"Could not open file: {path}")
           
           text_stream = QTextStream(file)
           content = text_stream.readAll()
           file.close()
           return content
       
       @override
       def write_text(self, path: str, content: str) -> None:
           file = QFile(path)
           if not file.open(QIODevice.WriteOnly | QIODevice.Text):
               raise IOError(f"Could not write to file: {path}")
           
           text_stream = QTextStream(file)
           text_stream << content
           file.close()
   ```

2. **Implement Save As Action**: Create a new action that shows a file dialog:
   ```python
   @action("Save As", shortcut="Ctrl+Shift+S", tooltip="Save the document with a new name")
   class SaveAsAction(QAction, IAction):
       @override
       def action(self, checked: bool, document_collection: IDocumentCollection = Depends[IDocumentCollection], 
                  filesystem: IFileSystem = Depends[IFileSystem], dialog_service: IDialogService = Depends[IDialogService]):
           # Get active document
           document = document_collection.get_active()
           if not document:
               dialog_service.show_message(DialogOptions(title="Save Error", message="No document is currently active"))
               return
               
           # Show file dialog
           file_dialog = QFileDialog()
           file_dialog.setAcceptMode(QFileDialog.AcceptSave)
           file_dialog.setNameFilter("Text files (*.txt);;All files (*)")
           
           if file_dialog.exec() == QDialog.Accepted:
               selected_files = file_dialog.selectedFiles()
               if selected_files:
                   path = Path(selected_files[0])
                   document.path = path
                   
                   # Save the document
                   success = document.save(filesystem)
                   if not success:
                       dialog_service.show_message(DialogOptions(title="Save Error", 
                                                   message=f"Failed to save document: {document.name}"))
   ```

3. **Update Production Container**: Replace the memory filesystem with the Qt filesystem in production:
   ```python
   class ProductionContainer(containers.DeclarativeContainer):
       """Production container with real implementations."""
   
       application = providers.Singleton(Application)
       document_collection = providers.Singleton(DocumentCollection)
       filesystem = providers.Singleton(QtFileSystem)  # Use Qt filesystem instead of memory
       dialog_service = providers.Singleton(QtDialogService)
   ```

4. **Add to File Menu**: Update the file menu to include the Save As action:
   ```python
   @menu()
   class FileMenu(QMenu):
       _text = "File"
       save_action: SaveAction = make(SaveAction)
       save_as_action: SaveAsAction = make(SaveAsAction)  # Add Save As action
       quit_action: QuitAction = make(QuitAction)
   ```

These steps will give us a functional file saving system that persists files to disk and allows users to choose where to save them.
