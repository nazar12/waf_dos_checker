# WAF and DoS Checker Extension for Burp Suite

This Burp Suite extension allows you to insert custom payloads for bypassing Web Application Firewalls (WAF) and testing Denial of Service (DoS) vulnerabilities by inserting large amounts of data into HTTP requests.
![Illustration of WAF and DoS Checker Extension](./Dos.webp)
## Features

- Insert WAF Bypass payloads of sizes ranging from 8 KB to 1024 KB, including custom sizes.
- Insert DoS payloads of sizes ranging from 1 MB to 5 MB, including custom sizes.
- Replaces the selected part of the request with the payload or inserts it at the end if no selection is made.
- Remembers the previously selected size for each type of payload.

## Installation

1. **Download Jython**:
   - Download Jython from the [official website](https://www.jython.org/downloads.html) and install it.

2. **Configure Burp Suite to use Jython**:
   - Open Burp Suite and navigate to `Extender` > `Options`.
   - In the `Python Environment` section, specify the path to the Jython JAR file.

3. **Add the Extension**:
   - Download the `waf_dos_checker.py` file from this repository.
   - Open Burp Suite and navigate to `Extender` > `Extensions`.
   - Click `Add`, select `Python` as the extension type, and load the downloaded `waf_dos_checker.py` file.

## Usage

1. **Open an HTTP request in Burp Suite's message editor**.
2. **Right-click to open the context menu**.
3. **Select either `Insert WAF Bypass Data` or `Insert DoS Payload`**.
4. **Choose the payload size** from the dropdown or enter a custom size and select the unit (KB or MB), then click `OK`.

The selected payload will replace the highlighted portion of the request or be inserted at the end if no portion is highlighted.

## Code Explanation

### Main Class: `BurpExtender`

Implements the `IBurpExtender`, `IContextMenuFactory`, and `IHttpListener` interfaces.

#### Methods:

- **`registerExtenderCallbacks`**: 
  - Registers the extension with Burp Suite and sets up the context menu and HTTP listener.
  - Initializes output streams for logging.

- **`createMenuItems`**:
  - Creates the context menu items for inserting WAF Bypass and DoS payloads.

- **`insert_waf`**:
  - Calls `insert_payload` with parameters specific to WAF Bypass.

- **`insert_dos`**:
  - Calls `insert_payload` with parameters specific to DoS.

- **`insert_payload`**:
  - Displays a dialog to select the payload size or enter a custom size and unit (KB or MB).
  - Inserts the generated payload into the selected part of the request or at the end if no selection is made.

- **`processHttpMessage`**:
  - Currently not used but implemented for potential future use.

### Payload Sizes:

- **WAF Bypass**: 8 KB, 16 KB, 32 KB, 64 KB, 128 KB, 1024 KB, and custom sizes.
- **DoS**: 1 MB, 2 MB, 3 MB, 4 MB, 5 MB, and custom sizes.

### Exception Handling:

- Any errors during the payload insertion are caught and logged to the stderr stream.

## Example

1. **Insert WAF Bypass Payload**:
    - Select a part of the request, right-click, choose `Insert WAF Bypass Data`, and select a size (e.g., 128 KB) or enter a custom size and select the unit (KB).

2. **Insert DoS Payload**:
    - Select a part of the request, right-click, choose `Insert DoS Payload`, and select a size (e.g., 3 MB) or enter a custom size and select the unit (MB).

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.




