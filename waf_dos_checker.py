from burp import IBurpExtender, IContextMenuFactory, IHttpListener, IRequestInfo, IContextMenuInvocation, IParameter
from javax.swing import JMenuItem, JLabel, JTextField, JOptionPane, JPanel, JFrame, JComboBox
import javax.swing as swing
from java.util import ArrayList
from java.io import ByteArrayOutputStream, PrintWriter

class BurpExtender(IBurpExtender, IContextMenuFactory, IHttpListener):
    previous_size_dos = None
    previous_size_waf = None

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("WAF and DoS Checker")
        callbacks.registerContextMenuFactory(self)
        callbacks.registerHttpListener(self)
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        self._stderr = PrintWriter(callbacks.getStderr(), True)
        self._stdout.println("WAF and DoS Checker extension loaded")
    
    def createMenuItems(self, invocation):
        self.context = invocation
        menu_list = ArrayList()
        if self.context.getInvocationContext() == IContextMenuInvocation.CONTEXT_MESSAGE_EDITOR_REQUEST:
            menu_list.add(JMenuItem("Insert WAF Bypass Data", actionPerformed=self.insert_waf))
            menu_list.add(JMenuItem("Insert DoS Payload", actionPerformed=self.insert_dos))
        return menu_list

    def insert_waf(self, event):
        self.insert_payload(event, "WAF Bypass Data", self.previous_size_waf, "waf")

    def insert_dos(self, event):
        self.insert_payload(event, "DoS Payload", self.previous_size_dos, "dos")

    def insert_payload(self, event, dialog_title, previous_size, payload_type):
        try:
            message = self.context.getSelectedMessages()[0]
            request = message.getRequest()
            selection_bounds = self.context.getSelectionBounds()

            options_panel = JPanel()
            options_panel.setLayout(swing.BoxLayout(options_panel, swing.BoxLayout.Y_AXIS))

            if payload_type == "dos":
                sizes = [str(i) + " MB" for i in range(1, 6)] + ["Custom"]
            else:
                sizes = [str(size) + " KB" for size in [8, 16, 32, 64, 128, 1024]] + ["Custom"]

            dropdown = JComboBox(sizes)
            
            custom_size_field = JTextField(10)
            custom_size_label = JLabel("Custom size:")
            unit_dropdown = JComboBox(["KB", "MB"])

            custom_size_field.setVisible(False)
            custom_size_label.setVisible(False)
            unit_dropdown.setVisible(False)

            def update_custom_field_visibility(event):
                is_custom_selected = dropdown.getSelectedItem() == "Custom"
                custom_size_label.setVisible(is_custom_selected)
                custom_size_field.setVisible(is_custom_selected)
                unit_dropdown.setVisible(is_custom_selected)
                if is_custom_selected:
                    custom_size_field.requestFocus()
                swing.SwingUtilities.getWindowAncestor(options_panel).pack()

            dropdown.addActionListener(update_custom_field_visibility)

            if previous_size:
                dropdown.setSelectedItem(previous_size)

            options_panel.add(dropdown)
            options_panel.add(custom_size_label)
            options_panel.add(custom_size_field)
            options_panel.add(unit_dropdown)

            frame = JFrame()
            dialog = JOptionPane.showConfirmDialog(frame, options_panel, "Select {} Size Multiplier".format(dialog_title), JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE)
            
            if dialog == JOptionPane.OK_OPTION:
                selected_size = dropdown.getSelectedItem()
                if selected_size == "Custom":
                    try:
                        custom_size = int(custom_size_field.getText())
                        unit = unit_dropdown.getSelectedItem()
                        if unit == "MB":
                            if payload_type == "dos":
                                payload = '1' * (custom_size * 1024 * 1024)
                            else:
                                JOptionPane.showMessageDialog(None, "Invalid unit for WAF Bypass.")
                                return
                        elif unit == "KB":
                            if payload_type == "dos":
                                payload = '1' * (custom_size * 1024)
                            elif payload_type == "waf":
                                payload = 'w' * (custom_size * 1024)
                            else:
                                JOptionPane.showMessageDialog(None, "Invalid unit for payload type.")
                                return
                        selected_size = "{} {}".format(custom_size, unit)
                    except ValueError:
                        JOptionPane.showMessageDialog(None, "Please enter a valid number for custom size.")
                        return
                else:
                    if "MB" in selected_size:
                        size_mb = int(selected_size.split()[0])
                        payload = '1' * (size_mb * 1024 * 1024)
                    else:
                        size_kb = int(selected_size.split()[0])
                        if payload_type == "dos":
                            payload = '1' * (size_kb * 1024)
                        elif payload_type == "waf":
                            payload = 'w' * (size_kb * 1024)

                request_str = self._helpers.bytesToString(request)
                if selection_bounds:
                    start, end = selection_bounds
                    new_request_str = request_str[:start] + payload + request_str[end:]
                else:
                    insertion_point = len(request_str)
                    new_request_str = request_str[:insertion_point] + payload + request_str[insertion_point:]

                new_request = self._helpers.stringToBytes(new_request_str)
                message.setRequest(new_request)
                self._stdout.println("Injected {} of size {} into request".format(dialog_title, selected_size))
                self._stdout.println("Payload size in bytes: {}".format(len(payload)))
        except Exception as e:
            self._stderr.println("Error: {}".format(e))

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        pass
