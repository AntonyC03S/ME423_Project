import network
import socket
import time

WIFI_LIST = [
    ("CP-IoT-Secure", "..."),
    ("...", "..."),
]

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("Already connected:", wlan.ifconfig())
        return wlan

    for ssid, password in WIFI_LIST:
        print("Trying Wi-Fi:", ssid)
        wlan.disconnect()
        time.sleep(1)
        wlan.connect(ssid, password)

        for _ in range(10):
            if wlan.isconnected():
                print("Connected to:", ssid)
                print("IP address:", wlan.ifconfig()[0])
                return wlan
            print(".", end="")
            time.sleep(1)

        print()
        print("Failed:", ssid)

    return None

wlan = connect_wifi()

if wlan is None or not wlan.isconnected():
    print("Could not connect to any Wi-Fi")
    raise SystemExit

ip = wlan.ifconfig()[0]

html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Controller Pad</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f4f4f4;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    .app {
      background: white;
      padding: 24px;
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.12);
      width: 340px;
      text-align: center;
    }
    h1 {
      margin-top: 0;
      font-size: 24px;
    }
    .coords {
      display: flex;
      gap: 12px;
      justify-content: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }
    .coords label {
      display: flex;
      flex-direction: column;
      font-size: 14px;
      text-align: left;
    }
    .coords input {
      margin-top: 6px;
      padding: 8px;
      width: 100px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-size: 16px;
    }
    .controller {
      display: grid;
      grid-template-columns: 70px 70px 70px;
      grid-template-rows: 70px 70px 70px;
      gap: 10px;
      justify-content: center;
      margin: 20px 0;
    }
    .empty { visibility: hidden; }
    button {
      border: none;
      border-radius: 12px;
      background: #1f6feb;
      color: white;
      font-size: 24px;
      cursor: pointer;
      transition: transform 0.1s ease, background 0.2s ease;
    }
    button:hover { background: #1557b0; }
    button:active { transform: scale(0.96); }
    .position-box {
      margin-top: 16px;
      padding: 14px;
      background: #eef4ff;
      border-radius: 12px;
      font-size: 18px;
      font-weight: bold;
    }
    .actions {
      margin-top: 14px;
    }
    .actions button {
      font-size: 16px;
      padding: 10px 16px;
      background: #444;
    }
    .actions button:hover {
      background: #222;
    }
  </style>
</head>
<body>
  <div class="app">
    <h1>Controller Pad</h1>

    <div class="coords">
      <label>
        X Coordinate
        <input type="number" id="xInput" value="0" />
      </label>
      <label>
        Y Coordinate
        <input type="number" id="yInput" value="0" />
      </label>
    </div>

    <div class="controller">
      <div class="empty"></div>
      <button onclick="move('up')">↑</button>
      <div class="empty"></div>

      <button onclick="move('left')">←</button>
      <button onclick="resetPosition()">•</button>
      <button onclick="move('right')">→</button>

      <div class="empty"></div>
      <button onclick="move('down')">↓</button>
      <div class="empty"></div>
    </div>

    <div class="position-box" id="positionDisplay">
      Position: (0, 0)
    </div>

    <div class="actions">
      <button onclick="applyCoordinates()">Set X / Y</button>
    </div>
  </div>

  <script>
    let x = 0;
    let y = 0;

    const xInput = document.getElementById('xInput');
    const yInput = document.getElementById('yInput');
    const positionDisplay = document.getElementById('positionDisplay');

    function updateDisplay() {
      xInput.value = x;
      yInput.value = y;
      positionDisplay.textContent = `Position: (${x}, ${y})`;
    }

    function move(direction) {
      if (direction === 'up') y += 1;
      if (direction === 'down') y -= 1;
      if (direction === 'left') x -= 1;
      if (direction === 'right') x += 1;
      updateDisplay();
    }

    function applyCoordinates() {
      x = Number(xInput.value) || 0;
      y = Number(yInput.value) || 0;
      updateDisplay();
    }

    function resetPosition() {
      x = 0;
      y = 0;
      updateDisplay();
    }

    xInput.addEventListener('input', applyCoordinates);
    yInput.addEventListener('input', applyCoordinates);

    updateDisplay();
  </script>
</body>
</html>

""" 

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen(1)

print("Web server running at http://%s" % ip)

while True:
    client, client_addr = server.accept()
    print("Client connected from", client_addr)
    request = client.recv(1024)

    client.send(b"HTTP/1.1 200 OK\r\n")
    client.send(b"Content-Type: text/html\r\n")
    client.send(b"Connection: close\r\n\r\n")
    client.send(html.encode())

    client.close()