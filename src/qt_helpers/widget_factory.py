from dataclasses import field
from typing import (
    Any,
    Callable,
    List,
    Type,
    TypeVar,
    Union,
    Tuple,
    Optional,
    cast,
)

from PySide6.QtWidgets import QWidget


# Define a type variable for widgets
W = TypeVar("W", bound=QWidget)

# Define a type for widget options
WidgetOptionsType = Optional[Union[str, List[str], Tuple[str, List[str]]]]


def _create_widget[W](
    widget_class: Type[W],
    widget_options: WidgetOptionsType = None,
    *args: Any,
    **kwargs: Any,
) -> W:
    """
    Internal function to create a widget with name and classes.

    This is used by make_widget to create the actual widget instance.
    """
    # Create the widget instance
    widget = widget_class(*args, **kwargs)

    # Cast to QWidget to ensure type checking recognizes the widget methods
    qwidget = cast(QWidget, widget)

    # Process widget options based on type
    if widget_options is not None:
        if isinstance(widget_options, str):
            # Just the name
            qwidget.setObjectName(widget_options)
        elif isinstance(widget_options, list):
            # Just the classes
            qwidget.setProperty("class", f"|{'|'.join(widget_options)}|")
        elif isinstance(widget_options, tuple) and len(widget_options) == 2:
            # Both name and classes
            name, classes = widget_options
            if name:
                qwidget.setObjectName(name)
            if classes:
                qwidget.setProperty("class", f"|{'|'.join(classes)}|")

    return widget


def make_widget[W](
    widget_class: Type[W],
    widget_options: WidgetOptionsType = None,
    *args: Any,
    **kwargs: Any,
) -> W:
    """
    Creates a factory for a widget that can be used as a dataclass field default.

    This function creates a dataclass field with a default_factory that, when called,
    creates a widget with the specified name, classes, and other parameters.

    Args:
        widget_class: The widget class to instantiate
        widget_options: Widget options in one of these formats:
            - str: Just the widget name
            - List[str]: CSS classes to apply
            - Tuple[str, List[str]]: Both name and classes
        *args: Additional positional arguments to pass to the widget constructor
        **kwargs: Additional keyword arguments to pass to the widget constructor

    Returns:
        A dataclass field with a default_factory that creates the widget

    Example:
        # In a dataclass:
        class MyWidget(QWidget):
            # Create a label with just a name
            label1: QLabel = make_widget(QLabel, "lblTitle", "Hello World")

            # Create a label with just classes
            label2: QLabel = make_widget(QLabel, ["info", "large"], "Information")

            # Create a button with both name and classes
            button: QPushButton = make_widget(
                QPushButton,
                ("btnSubmit", ["primary", "large"]),
                "Submit",
                clicked=on_submit
            )
    """
    # Create a factory function that will create the widget
    factory_fn: Callable[[], W] = lambda: _create_widget(
        widget_class, widget_options, *args, **kwargs
    )

    # Return a dataclass field with the factory function
    return field(default_factory=factory_fn)
