from textual.widgets import Static

class StaticFooter(Static):

    DEFAULT_CSS = """
    StaticFooter {
        background: $accent;
        color: $text;
        dock: bottom;
        height: 1;
    }
    StaticFooter > .footer--highlight {    
        background: $accent-darken-1;         
    }

    StaticFooter > .footer--highlight-key {        
        background: $secondary;                
        text-style: bold;         
    }

    StaticFooter > .footer--key {
        text-style: bold;        
        background: $accent-darken-2;        
    }
    """
