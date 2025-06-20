from client import AngelClient
from config import SUBSCRIBE_ACTION_PAYLOAD, UNSUBSCRIBE_ACTION_PAYLOAD, get_websocket_headers, generate_tokens
import websocket
import asyncio
from threading import Thread
import time
import json
import struct

class SmartWebSockets(object):
    ROOT_WEBSOCKET_URI = "wss://smartapisocket.angelone.in/smart-stream"
    HEART_BEAT_MESSAGE = "ping"
    HEART_BEAT_INTERVAL = 30  
    LITTLE_ENDIAN_BYTE_ORDER = "<"
    
    # Constants for binary data parsing
    QUOTE = 1
    SNAP_QUOTE = 2
    DEPTH = 3

    SUBSCRIPTION_MODE_MAP = {
        QUOTE: "QUOTE",
        SNAP_QUOTE: "SNAP_QUOTE",
        DEPTH: "DEPTH"
    }
    
    def __init__(self):
        self.client = AngelClient()
        self.headers = get_websocket_headers()
        self.wsapp = None
        self.ws_thread = None
        self.heartbeat_thread = None
        self.is_connected = False
        try:
            token_data = generate_tokens()
            self.headers['Authorization'] = token_data[0]
            self.headers['x-feed-token'] = token_data[1]
        except Exception as e:
            print("Error generating tokens:", e)
            
    def _on_open(self, wsapp):
        print("Websocket Opened!")
        self.is_connected = True
        wsapp.send(self.HEART_BEAT_MESSAGE)
        self.subscribe(wsapp, SUBSCRIBE_ACTION_PAYLOAD)
        
    def _on_error(self, wsapp, error):
        print("Error occurred:", error)
        self.is_connected = False
        
    def _on_close(self, wsapp, close_status_code, close_msg):
        print("WebSocket connection closed:", close_msg if close_msg else "No message")
        self.is_connected = False
        self.unsubscribe(wsapp, UNSUBSCRIBE_ACTION_PAYLOAD)
    
    def _on_message(self, wsapp, message):
        try:
            if isinstance(message, bytes):
                parsed_data = self._parse_binary_data(message)
                if parsed_data:  # Only print if parsing was successful
                    print(json.dumps(parsed_data, indent=4))
            else:
                print(f"Received text message: {message}")
        except Exception as e:
            print(f"An unexpected error occurred in on_message: {e}")

    def _on_ping(self, wsapp, message):
        print("Ping received")
        wsapp.send(self.HEART_BEAT_MESSAGE)
    
    def _on_pong(self, wsapp, message):
        print("Pong received")
        
    def _heartbeat_loop(self):
        """Send periodic heartbeat messages to keep connection alive"""
        while self.is_connected:
            try:
                if self.wsapp and self.is_connected:
                    print(f"Sending heartbeat: {self.HEART_BEAT_MESSAGE}")
                    self.wsapp.send(self.HEART_BEAT_MESSAGE)
                time.sleep(self.HEART_BEAT_INTERVAL)
            except Exception as e:
                print(f"Error sending heartbeat: {e}")
                break
        
    def _run_websocket(self):
        self.wsapp = websocket.WebSocketApp(
            self.ROOT_WEBSOCKET_URI,
            header=self.headers,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_ping=self._on_ping,
            on_pong=self._on_pong
        )
        self.wsapp.run_forever()

    async def connect(self):
        try:
            # Start WebSocket connection
            self.ws_thread = Thread(target=self._run_websocket)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            # Wait for connection to establish
            await asyncio.sleep(2)
            
            # Start heartbeat thread
            self.heartbeat_thread = Thread(target=self._heartbeat_loop)
            self.heartbeat_thread.daemon = True
            self.heartbeat_thread.start()
            
            return "WebSocket connection initiated with heartbeat"
        except Exception as e:
            print("Error connecting to websocket:", e)
            raise e

    async def disconnect(self):
        self.is_connected = False
        if self.wsapp:
            self.wsapp.close()
        if self.ws_thread and self.ws_thread.is_alive():
            self.ws_thread.join(timeout=1)
        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            self.heartbeat_thread.join(timeout=1)
            
            
    def subscribe(self, wsapp, payload):
        try:
            wsapp.send(json.dumps(payload))
            print("Successfully Subscribed")
        except Exception as e:
            print("Error while Subscribing: ", e)
    
    def unsubscribe(self, wsapp, payload):
        try:
            wsapp.send(json.dumps(payload))
            print("Successfully Unsubscribed")
        except Exception as e:
            print("Error while Unsubscribing: ", e)
            
            
    def _parse_binary_data(self, binary_data):
        try:
            parsed_data = {
                "subscription_mode": self._unpack_data(binary_data, 0, 1, byte_format="B")[0],
                "exchange_type": self._unpack_data(binary_data, 1, 2, byte_format="B")[0],
                "token": self._parse_token_value(binary_data[2:27]),
                "sequence_number": self._unpack_data(binary_data, 27, 35, byte_format="q")[0],
                "exchange_timestamp": self._unpack_data(binary_data, 35, 43, byte_format="q")[0],
                "last_traded_price": self._unpack_data(binary_data, 43, 51, byte_format="q")[0]
            }
            
            parsed_data["subscription_mode_val"] = self.SUBSCRIPTION_MODE_MAP.get(parsed_data["subscription_mode"])

            if parsed_data["subscription_mode"] in [self.QUOTE, self.SNAP_QUOTE] and len(binary_data) >= 123:
                parsed_data["last_traded_quantity"] = self._unpack_data(binary_data, 51, 59, byte_format="q")[0]
                parsed_data["average_traded_price"] = self._unpack_data(binary_data, 59, 67, byte_format="q")[0]
                parsed_data["volume_trade_for_the_day"] = self._unpack_data(binary_data, 67, 75, byte_format="q")[0]
                parsed_data["total_buy_quantity"] = self._unpack_data(binary_data, 75, 83, byte_format="d")[0]
                parsed_data["total_sell_quantity"] = self._unpack_data(binary_data, 83, 91, byte_format="d")[0]
                parsed_data["open_price_of_the_day"] = self._unpack_data(binary_data, 91, 99, byte_format="q")[0]
                parsed_data["high_price_of_the_day"] = self._unpack_data(binary_data, 99, 107, byte_format="q")[0]
                parsed_data["low_price_of_the_day"] = self._unpack_data(binary_data, 107, 115, byte_format="q")[0]
                parsed_data["closed_price"] = self._unpack_data(binary_data, 115, 123, byte_format="q")[0]

            if parsed_data["subscription_mode"] == self.SNAP_QUOTE and len(binary_data) >= 379:
                parsed_data["last_traded_timestamp"] = self._unpack_data(binary_data, 123, 131, byte_format="q")[0]
                parsed_data["open_interest"] = self._unpack_data(binary_data, 131, 139, byte_format="q")[0]
                parsed_data["open_interest_change_percentage"] = self._unpack_data(binary_data, 139, 147, byte_format="q")[0]
                parsed_data["upper_circuit_limit"] = self._unpack_data(binary_data, 347, 355, byte_format="q")[0]
                parsed_data["lower_circuit_limit"] = self._unpack_data(binary_data, 355, 363, byte_format="q")[0]
                parsed_data["52_week_high_price"] = self._unpack_data(binary_data, 363, 371, byte_format="q")[0]
                parsed_data["52_week_low_price"] = self._unpack_data(binary_data, 371, 379, byte_format="q")[0]
                best_5_buy_and_sell_data = self._parse_best_5_buy_and_sell_data(binary_data[147:347])
                parsed_data["best_5_buy_data"] = best_5_buy_and_sell_data["best_5_sell_data"]
                parsed_data["best_5_sell_data"] = best_5_buy_and_sell_data["best_5_buy_data"]

            if parsed_data["subscription_mode"] == self.DEPTH and len(binary_data) >= 443:
                parsed_data.pop("sequence_number", None)
                parsed_data.pop("last_traded_price", None)
                parsed_data.pop("subscription_mode_val", None)
                parsed_data["packet_received_time"]=self._unpack_data(binary_data, 35, 43, byte_format="q")[0]
                depth_data_start_index = 43
                depth_20_data = self._parse_depth_20_buy_and_sell_data(binary_data[depth_data_start_index:])
                parsed_data["depth_20_buy_data"] = depth_20_data["depth_20_buy_data"]
                parsed_data["depth_20_sell_data"] = depth_20_data["depth_20_sell_data"]

            return parsed_data
        except Exception as e:
            print(f"Could not parse binary packet of length {len(binary_data)}. Error: {e}")
            return None
    
    def _unpack_data(self, binary_data, start, end, byte_format="I"):
        """
            Unpack Binary Data to the integer according to the specified byte_format.
            This function returns the tuple
        """
        return struct.unpack(self.LITTLE_ENDIAN_BYTE_ORDER + byte_format, binary_data[start:end])
    
    def _parse_token_value(self, binary_packet):
        token = ""
        for i in range(len(binary_packet)):
            if chr(binary_packet[i]) == '\x00':
                return token
            token += chr(binary_packet[i])
        return token

    def _parse_best_5_buy_and_sell_data(self, binary_data):

        def split_packets(binary_packets):
            packets = []

            i = 0
            while i < len(binary_packets):
                packets.append(binary_packets[i: i + 20])
                i += 20
            return packets

        best_5_buy_sell_packets = split_packets(binary_data)

        best_5_buy_data = []
        best_5_sell_data = []

        for packet in best_5_buy_sell_packets:
            each_data = {
                "flag": self._unpack_data(packet, 0, 2, byte_format="H")[0],
                "quantity": self._unpack_data(packet, 2, 10, byte_format="q")[0],
                "price": self._unpack_data(packet, 10, 18, byte_format="q")[0],
                "no of orders": self._unpack_data(packet, 18, 20, byte_format="H")[0]
            }

            if each_data["flag"] == 0:
                best_5_buy_data.append(each_data)
            else:
                best_5_sell_data.append(each_data)

        return {
            "best_5_buy_data": best_5_buy_data,
            "best_5_sell_data": best_5_sell_data
        }

    def _parse_depth_20_buy_and_sell_data(self, binary_data):
        depth_20_buy_data = []
        depth_20_sell_data = []

        for i in range(20):
            buy_start_idx = i * 10
            sell_start_idx = 200 + i * 10

            # Parse buy data
            buy_packet_data = {
                "quantity": self._unpack_data(binary_data, buy_start_idx, buy_start_idx + 4, byte_format="i")[0],
                "price": self._unpack_data(binary_data, buy_start_idx + 4, buy_start_idx + 8, byte_format="i")[0],
                "num_of_orders": self._unpack_data(binary_data, buy_start_idx + 8, buy_start_idx + 10, byte_format="h")[0],
            }

            # Parse sell data
            sell_packet_data = {
                "quantity": self._unpack_data(binary_data, sell_start_idx, sell_start_idx + 4, byte_format="i")[0],
                "price": self._unpack_data(binary_data, sell_start_idx + 4, sell_start_idx + 8, byte_format="i")[0],
                "num_of_orders": self._unpack_data(binary_data, sell_start_idx + 8, sell_start_idx + 10, byte_format="h")[0],
            }

            depth_20_buy_data.append(buy_packet_data)
            depth_20_sell_data.append(sell_packet_data)

        return {
            "depth_20_buy_data": depth_20_buy_data,
            "depth_20_sell_data": depth_20_sell_data
        }
    
        
        
        
        