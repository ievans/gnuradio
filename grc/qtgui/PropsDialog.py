from PyQt4.QtGui import *
from PyQt4.QtCore import Qt

from Constants import MIN_DIALOG_WIDTH, MIN_DIALOG_HEIGHT

def get_title_label(title):
    """
    Get a title label for the params window.
    The title will be bold, underlined, and left justified.
    
    Args:
        title: the text of the title
    
    Returns:
        a Qt widget
    """
    label = QLabel('\n<b><span underline="low">%s</span>:</b>\n'%title)
    #hbox = QHBoxLayout()
    #hbox.addWidget(label)
    #return hbox
    return label

def debug_trace():
    '''Set a tracepoint in the Python debugger that works with Qt'''
    from PyQt4.QtCore import pyqtRemoveInputHook
    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()

class PropsDialog(QDialog):
    """
    A dialog to set block parameters, view errors, and view documentation.
    """

    def __init__(self, block, parent = None):
        """
        Properties dialog contructor.
        
        Args:
            block: a block instance
        """
        super(PropsDialog, self).__init__(parent)
        self._hash = 0
        self._block = block

        LABEL_SPACING = 7
        self.setMinimumWidth(MIN_DIALOG_WIDTH)
        self.setMinimumHeight(MIN_DIALOG_HEIGHT)
        self.setWindowTitle('Properties: %s' % block.get_name())

        layout = QVBoxLayout(self)
        #layout.addWidget(self.datetime)

        self._params_box_widget = QWidget()
        #self._params_box_widget.layout.setStyleSheet("margin: 0px; padding: 0px;")

        self._params_box = QVBoxLayout()
        self._params_box.addWidget(get_title_label('Parameters'))
        self._input_object_params = list()

        for param in self._block.get_params():
            if param.get_hide() == 'all': continue
            io_param = param.get_input(self._handle_changed)
            self._input_object_params.append(io_param)
            print 'added ' + str(io_param)
            self._params_box.addWidget(io_param)

        self._params_box_widget.setLayout(self._params_box)
        layout.addWidget(self._params_box_widget)

        # Error messages
        self._error_box_widget = QWidget()
        self._error_box = QVBoxLayout()

        self._error_messages_text_display = QTextEdit()
        self._error_messages_text_display.setReadOnly(True)
        messages = '\n\n'.join(self._block.get_error_messages())
        self._error_messages_text_display.setText(messages)

        self._error_box.addWidget(get_title_label('Error Messages'))
        self._error_box.addWidget(self._error_messages_text_display)
        self._error_box_widget.setLayout(self._error_box)

        self._error_box_widget.setVisible(not self._block.is_valid())

        layout.addWidget(self._error_box_widget)

        # Docs for the block
        # self._docs_box = err_box = gtk.VBox()
        # self._docs_text_display = TextDisplay()
        # self._docs_box.pack_start(gtk.Label(), False, False, LABEL_SPACING)
        # self._docs_box.pack_start(get_title_label('Documentation'), False)
        # self._docs_box.pack_start(self._docs_text_display, False)

        self._docs_box = QVBoxLayout()
        self._docs_box_widget = QWidget()
        self._docs_text_display = QTextEdit()
        self._docs_text_display.setReadOnly(True)
        self._docs_text_display.setText(self._block.get_doc())
        self._docs_box.addWidget(get_title_label('Documentation'))
        self._docs_box.addWidget(self._docs_text_display)

        self._docs_box_widget.setLayout(self._docs_box)
        self._docs_box_widget.setVisible(len(self._block.get_doc()))

        layout.addWidget(self._docs_box_widget)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)
    
    @staticmethod
    def run(block, parent = None):
        dialog = PropsDialog(block, parent)
        result = dialog.exec_()
        return result == QDialog.Accepted

    def _handle_changed(self, *args):
        """
        A change occured within a param:
        Rewrite/validate the block and update the gui.
        """
        #update for the block
        #self._block.rewrite()
        #self._block.validate()
        #self._update_gui()
        pass
