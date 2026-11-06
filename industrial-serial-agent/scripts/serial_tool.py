#!/usr/bin/env python3
"""
Industrial Serial Communication & Diagnostic Tool
Built on industry-standard pyserial (3.5k+ stars) to provide robust, non-blocking
COM port interaction, automated device probing, and firmware log capture.
"""

import sys
import time
import json
import argparse

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print(json.dumps({"error": "pyserial not installed. Run 'pip install pyserial'"}))
    sys.exit(1)

def list_ports():
    ports = serial.tools.list_ports.comports()
    results = []
    for p in ports:
        results.append({
            "device": p.device,
            "description": p.description,
            "hwid": p.hwid,
            "vid": f"0x{p.vid:04X}" if p.vid else None,
            "pid": f"0x{p.pid:04X}" if p.pid else None,
            "manufacturer": p.manufacturer
        })
    return {"total_ports": len(results), "ports": results}

def send_and_receive(port, baudrate=115200, data="PING\r\n", timeout=2.0, is_hex=False):
    try:
        ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
    except serial.SerialException as e:
        return {
            "success": False,
            "error": f"Failed to open port {port}: {str(e)}",
            "hint": "The COM port might be in use by VOFA+, MobaXterm, or another terminal. Please close them first."
        }

    try:
        if is_hex:
            payload = bytes.fromhex(data.replace(" ", ""))
        else:
            payload = data.encode('utf-8', errors='replace')

        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(payload)
        ser.flush()

        # Wait and read response
        start_time = time.time()
        rx_bytes = bytearray()
        while time.time() - start_time < timeout:
            if ser.in_waiting > 0:
                chunk = ser.read(ser.in_waiting)
                rx_bytes.extend(chunk)
                time.sleep(0.05)
            else:
                time.sleep(0.02)

        rx_text = rx_bytes.decode('utf-8', errors='replace')
        return {
            "success": True,
            "port": port,
            "baudrate": baudrate,
            "sent_bytes": len(payload),
            "received_bytes": len(rx_bytes),
            "response_text": rx_text,
            "response_hex": rx_bytes.hex(' ') if rx_bytes else ""
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        ser.close()

def capture_log(port, baudrate=115200, duration=3.0):
    try:
        ser = serial.Serial(port=port, baudrate=baudrate, timeout=1.0)
    except serial.SerialException as e:
        return {
            "success": False,
            "error": f"Failed to open port {port}: {str(e)}",
            "hint": "Check if VOFA+ or MobaXterm is occupying this COM port."
        }

    try:
        ser.reset_input_buffer()
        start = time.time()
        log_bytes = bytearray()

        while time.time() - start < duration:
            if ser.in_waiting > 0:
                log_bytes.extend(ser.read(ser.in_waiting))
            time.sleep(0.05)

        log_text = log_bytes.decode('utf-8', errors='replace')
        return {
            "success": True,
            "port": port,
            "baudrate": baudrate,
            "duration_sec": duration,
            "received_bytes": len(log_bytes),
            "log": log_text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        ser.close()

def main():
    parser = argparse.ArgumentParser(description="Industrial Serial CLI for AI Agents")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List available COM ports")

    # send
    send_parser = subparsers.add_parser("send", help="Send data to serial port and read response")
    send_parser.add_argument("port", help="COM port name (e.g. COM3)")
    send_parser.add_argument("data", help="Data to send")
    send_parser.add_argument("-b", "--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    send_parser.add_argument("-t", "--timeout", type=float, default=2.0, help="Timeout in seconds")
    send_parser.add_argument("--hex", action="store_true", help="Send as hex string")

    # capture
    cap_parser = subparsers.add_parser("capture", help="Capture serial log stream for N seconds")
    cap_parser.add_argument("port", help="COM port name (e.g. COM3)")
    cap_parser.add_argument("-b", "--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    cap_parser.add_argument("-d", "--duration", type=float, default=3.0, help="Duration to listen in seconds")

    args = parser.parse_args()

    if args.command == "list":
        res = list_ports()
    elif args.command == "send":
        res = send_and_receive(args.port, args.baud, args.data, args.timeout, args.hex)
    elif args.command == "capture":
        res = capture_log(args.port, args.baud, args.duration)
    else:
        res = {"error": "Invalid command"}

    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
