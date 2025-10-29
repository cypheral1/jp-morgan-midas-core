#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class IncentivesHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/incentive':
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            try:
                transaction = json.loads(post_data.decode('utf-8'))
                print(f"Received request: {transaction}")  # Debug print
                
                # Try to get amount from different possible formats
                amount = 0.0
                if isinstance(transaction, dict):
                    if 'amount' in transaction:
                        amount = float(transaction['amount'])
                    elif 'senderId' in transaction and 'recipientId' in transaction and 'amount' in transaction:
                        amount = float(transaction['amount'])
                
                # Calculate incentive (5% of amount, rounded to 2 decimals)
                incentive = round(amount * 0.05, 2)
                print(f"Calculated incentive: {incentive}")  # Debug print
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {'amount': incentive}
                print(f"Sending response: {response}")  # Debug print
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            except Exception as e:
                print(f"Error processing request: {e}")  # Debug print
                pass
        
        self.send_response(400)
        self.end_headers()

def run_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), IncentivesHandler)
    print(f'Mock incentives API listening on http://0.0.0.0:{port}/incentive')
    server.serve_forever()

if __name__ == '__main__':
    run_server()